"""

Core pipeline implementation for the Claimify claim extraction system.
Implements the multi-stage pipeline as described in the Claimify paper.
Uses structured outputs for improved reliability.

Based on the implementation by Adam Gustavsson:
https://github.com/AdamGustavsson/ClaimsMCP/blob/main/pipeline.py
"""

import nltk
import os
import sys
import logging
from typing import Dict, List, Tuple, Union
from utils.chat import get_prompt
from models.claimify import SelectionResponse, DisambiguationResponse, DecompositionResponse


def ensure_nltk_data():
    """Ensure NLTK punkt tokenizer data is downloaded."""
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        print("Downloading NLTK punkt tokenizer data...")
        try:
            nltk.download("punkt_tab")
        except:
            # Fallback to older punkt if punkt_tab fails
            nltk.download("punkt")


def split_into_sentences(text: str) -> List[str]:
    """
    Splits a block of text into sentences, handling paragraphs and lists.
    This replicates the methodology from Appendix C.1 of the Claimify paper.

    Args:
        text: The input text to split

    Returns:
        A list of sentence strings
    """
    ensure_nltk_data()

    sentences = []
    # First, split by newlines to handle paragraphs and list items
    paragraphs = text.split("\n")
    for para in paragraphs:
        if para.strip():  # Avoid empty paragraphs
            # Then, use NLTK's sentence tokenizer on each paragraph
            sentences.extend(nltk.sent_tokenize(para))
    return sentences


def create_context_for_sentence(
    sentences: List[str],
    index: int,
    p: int,  # Number of preceding sentences
    f: int,  # Number of following sentences
) -> str:
    start = max(0, index - p)
    end = min(len(sentences), index + f + 1)

    context_sentences = sentences[start:end]

    return "\n".join(context_sentences)


def run_selection_stage(chat, question: str, excerpt: str, sentence: str) -> Tuple[str, str]:
    prompt = get_prompt(
        "claimify", "selection", {"question": question, "excerpt": excerpt, "sentence": sentence}
    )
    structured_response = chat.invoke(prompt)

    if not structured_response:
        return "error", None

    return parse_structured_selection_output(structured_response, sentence)


def parse_structured_selection_output(response: SelectionResponse, original_sentence: str) -> Tuple[str, str]:
    try:
        if response.final_submission == "Contains a specific and verifiable proposition":
            if response.sentence_with_only_verifiable_information:
                if response.sentence_with_only_verifiable_information.lower() == "remains unchanged":
                    return "verifiable", original_sentence
                elif response.sentence_with_only_verifiable_information.lower() == "none":
                    return "unverifiable", None
                else:
                    return "verifiable", response.sentence_with_only_verifiable_information
            else:
                return "verifiable", original_sentence
        else:
            return "unverifiable", None
    except Exception as e:
        return "error", None


def run_disambiguation_stage(chat, question: str, excerpt: str, sentence: str) -> Tuple[str, str]:
    prompt = get_prompt(
        "claimify", "disambiguation", {"question": question, "excerpt": excerpt, "sentence": sentence}
    )
    response = chat.invoke(prompt)

    if not response:
        return "error", None
    if response.decontextualized_sentence:
        if response.decontextualized_sentence == "Cannot be decontextualized":
            return "unresolvable", None
        else:
            return "resolved", response.decontextualized_sentence
    else:
        return "unresolvable", None


def run_decomposition_stage(chat, question: str, excerpt: str, sentence: str) -> List[str]:
    """
    Executes the Decomposition stage of the Claimify pipeline using structured outputs.

    Args:
        llm_client: The LLM client to use
        question: The question/context for the text
        excerpt: The context excerpt
        sentence: The sentence to process

    Returns:
        A list of extracted claim strings
    """
    structured_response = chat.invoke(
        get_prompt(
            "claimify", "decomposition", {"question": question, "excerpt": excerpt, "sentence": sentence}
        )
    )

    if not structured_response:
        return []

    return [claim.text for claim in structured_response.final_claims]


class ClaimifyPipeline:
    """
    Main pipeline class that orchestrates the multi-stage claim extraction process.
    Uses structured outputs for improved reliability.
    """

    def __init__(self, chat, question: str = "The user did not provide a question."):

        self.question = question

        # Set up logging
        self.setup_logging()

        self.chat_selection = chat.with_structured_output(SelectionResponse)
        self.chat_disambiguation = chat.with_structured_output(DisambiguationResponse)
        self.chat_decomposition = chat.with_structured_output(DecompositionResponse)

        if self.logger:
            self.logger.info("Structured outputs enabled for improved reliability")

    def setup_logging(self):
        """Set up logging for the pipeline."""
        log_enabled = os.getenv("LOG_LLM_CALLS", "true").lower() in ("true", "1", "yes")

        if not log_enabled:
            self.logger = None
            return

        self.logger = logging.getLogger("claimify.pipeline")
        self.logger.setLevel(logging.INFO)

        if self.logger.handlers:
            return

        # Determine log output - default to stderr for MCP compatibility
        log_output = os.getenv("LOG_OUTPUT", "stderr").lower()

        if log_output == "file":
            # Log to file - but handle read-only file systems gracefully
            try:
                log_file = os.getenv("LOG_FILE", "claimify_pipeline.log")
                handler = logging.FileHandler(log_file)
            except (OSError, PermissionError):
                # Fall back to stderr if file logging fails
                handler = logging.StreamHandler(sys.stderr)
        else:
            # Log to stderr (default) - won't interfere with MCP protocol on stdout
            handler = logging.StreamHandler(sys.stderr)

        # Set formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def run(self, text_to_process: str) -> List[str]:
        """
        Runs the full Claimify pipeline on a given text.

        Args:
            text_to_process: The input text to process

        Returns:
            A list of extracted claim strings
        """
        if not text_to_process.strip():
            return []

        all_claims = []
        sentences = split_into_sentences(text_to_process)

        if self.logger:
            self.logger.info(f"Processing {len(sentences)} sentences")

        for i, sentence in enumerate(sentences):
            if self.logger:
                self.logger.info(f"Processing sentence {i+1}/{len(sentences)}: {sentence[:100]}...")

            # Create context for the current sentence
            # Using a fixed context window as per the paper's experiments
            context_excerpt = create_context_for_sentence(sentences, i, p=5, f=5)

            # Stage 2: Selection
            selection_status, verifiable_sentence = run_selection_stage(
                self.chat_selection, self.question, context_excerpt, sentence
            )

            if self.logger:
                self.logger.info(f"SELECTION: Sentence {selection_status}")

            if selection_status != "verifiable":
                continue

            # Stage 3: Disambiguation
            disambiguation_status, clarified_sentence = run_disambiguation_stage(
                self.chat_disambiguation, self.question, context_excerpt, verifiable_sentence
            )

            if self.logger:
                self.logger.info(f"DISAMBIGUATION: Sentence {disambiguation_status}")

            if disambiguation_status != "resolved":
                continue

            # Stage 4: Decomposition
            extracted_claims = run_decomposition_stage(
                self.chat_decomposition, self.question, context_excerpt, clarified_sentence
            )

            if self.logger:
                self.logger.info(f"DECOMPOSITION: Extracted {len(extracted_claims)} claims")

            if extracted_claims:
                all_claims.extend(extracted_claims)

        # Return a de-duplicated list of claims
        unique_claims = list(dict.fromkeys(all_claims))

        if self.logger:
            self.logger.info(f"Pipeline completed: {len(unique_claims)} unique claims extracted")

        return unique_claims


class ClaimifyEvaluator:
    def __init__(self, pipeline: ClaimifyPipeline):
        self.pipeline = pipeline

    def run(self, text: str, question: str) -> Dict[str, Union[int, float]]:
        """
        Runs the evaluation on the given text and question.

        Args:
            text: The input text to process
            question: The question to ask about the text

        Returns:
            A dictionary containing evaluation metrics
        """
        expected_claims = []  # Define the expected claims based on the question
        return self.pipeline.evaluate(text, expected_claims)
