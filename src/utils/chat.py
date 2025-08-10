import os
from typing import Any, Dict, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


PROMPT_TEMPLATES = {}


def load_md_prompts(prompt_category: str) -> Dict[str, str]:
    """
    Load Markdown prompts from a folder.

    Args:
        folder (str): The folder containing the Markdown files.

    Returns:
        Dict[str, str]: A dictionary mapping file names to their contents.
    """
    global PROMPT_TEMPLATES
    if prompt_category not in PROMPT_TEMPLATES:
        prompts = {}
        folder = os.path.join(os.path.dirname(__file__), "../../prompts", prompt_category)
        for filename in os.listdir(folder):
            if filename.endswith(".system.md") or filename.endswith(".user.md"):
                # pair system prompts with user prompts
                id, role = filename.split(".")[:2]
                if id not in prompts:
                    prompts[id] = {}
                with open(os.path.join(folder, filename), "r") as f:
                    prompts[id][role] = f.read()

        prompt_templates = {}
        for id, roles in prompts.items():
            prompt_templates[id] = ChatPromptTemplate.from_messages(
                [("system", roles.get("system", "").strip()), ("user", roles.get("user", "").strip())]
            )
        if prompt_category not in PROMPT_TEMPLATES:
            PROMPT_TEMPLATES[prompt_category] = {}
        PROMPT_TEMPLATES[prompt_category].update(prompt_templates)
    return PROMPT_TEMPLATES[prompt_category]


def get_prompt(category: str, name: str = None, values: dict = None) -> Optional[ChatPromptTemplate]:
    if name is None:
        category, name = category.split("/")

    prompt = load_md_prompts(category).get(name, None)
    if values:
        prompt = prompt.format_messages(**values)
    return prompt


def chat_factory(
    model_name: str, temperature: float = 0.0, output_structure: Any = None, backend: str = None, **kwargs
):
    if backend is None:
        if ":" in model_name:
            backend = "ollama"
        elif "gpt" in model_name:
            backend = "openai"
        else:  # default to ollama
            backend = "ollama"

    if backend == "ollama":
        return ChatOllama(model_name, temperature=temperature, **kwargs)
    elif backend == "openai":
        result = ChatOpenAI(model_name=model_name, temperature=temperature, **kwargs)
        if output_structure is not None:
            result = result.with_structured_output(output_structure)
        return result

    return None
