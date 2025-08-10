"""
Chat module: provides a simple interface for interacting with OpenAI's chat API. It includes the SimpleJSONChat class, which facilitates sending messages and receiving responses from the API in a structured JSON format. Additionally, the module contains a utility function, pretty_print, for formatting long strings of text with line breaks for improved readability.

Classes:
    SimpleJSONChat: Simplistic class to handle communication with OpenAI's chat API, abstracting away the sending of prompts and receiving of responses.

Functions:
    pretty_print(text: str, break_line_at: int = 90) -> str: Pretty prints a given text with line breaks at specified intervals.
"""

import openai
import json
import os
from typing import Any, Dict, List, Optional, Union
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama


class SimpleJSONChat:
    def __init__(
        self,
        system_prompt: Optional[str] = None,
        client: Optional[openai.OpenAI] = None,
        model: str = "gpt-5",
        temperature: float = 0.0,
        parse_output: bool = True,
        **openai_kwargs: Any,
    ) -> None:
        """
        Initialize a SimpleJSONChat object to interact with OpenAI's chat API.

        Args:
            system_prompt (Optional[str]): The initial prompt that sets the context for the conversation.
            client (Optional[openai.OpenAI]): An instance of the OpenAI API client.
            model (str): The model to be used for generating responses.
            temperature (float): Controls the randomness of the response. Lower values mean less random responses.
            parse_output (bool): If True, parse the output as JSON, otherwise return the raw string.
            **openai_kwargs: Additional keyword arguments to pass to the OpenAI API.
        """
        if client is None:
            client = openai.OpenAI()
        self.system_prompt = system_prompt
        self.client = client
        self.model = model
        self.temperature = temperature
        self.openai_kwargs = openai_kwargs
        self.parse_output = parse_output

    def __call__(
        self, user_prompts: Union[str, List[str]], system_prompt: Optional[str] = None
    ) -> Union[Dict[str, Any], str, List]:
        """
        Send a message to the OpenAI chat API and receive a response.

        Args:
            user_prompts (Union[str, List[str]]): The user's message or messages to send to the API.
            system_prompt (Optional[str]): An optional override for the initial system prompt.

        Returns:
            Union[Dict[str, Any], str, List]: The parsed JSON response if parse_output is True,
            the raw string response otherwise, or an empty list in case of an error.
        """
        if not isinstance(user_prompts, list):
            user_prompts = [user_prompts]
        if system_prompt is None:
            system_prompt = self.system_prompt

        messages = [{"role": "system", "content": system_prompt}]
        for user_prompt in user_prompts:
            messages.append({"role": "user", "content": user_prompt})

        response = self.client.chat.completions.create(
            model=self.model, temperature=self.temperature, messages=messages, **self.openai_kwargs
        )
        try:
            result = response.choices[0].message.content.replace("```json", "").replace("```", "")
            return json.loads(result) if self.parse_output else result
        except:
            print("Error parsing response from OpenAI chat API.\n", response.choices[0].message.content)
            return []

    def __repr__(self) -> str:
        """
        Return a string representation of the SimpleJSONChat object.

        Returns:
            str: A string representation of the object.
        """
        return f"SimpleJSONChat(system_prompt={self.system_prompt}, model={self.model}, temperature={self.temperature}, kwargs={self.openai_kwargs})"

    def __str__(self) -> str:
        """
        Return a string representation of the SimpleJSONChat object.

        Returns:
            str: A string representation of the object.
        """
        return self.__repr__()


class LangChainJSONChat:
    def __init__(
        self,
        prompt: ChatPromptTemplate,
        llm: Optional[Any] = None,
        model: str = "gpt-5",
        temperature: float = 0.0,
        parse_output: bool = True,
        **llm_kwargs: Any,
    ) -> None:
        """
        Initialize a LangChainJSONChat to interact via LangChain with a ChatPromptTemplate.

        Args:
            prompt (ChatPromptTemplate): A ChatPromptTemplate with variables to be formatted at call time.
            llm (Optional[Any]): A LangChain ChatModel instance. If None, ChatOpenAI will be created.
            model (str): The model name passed to ChatOpenAI if llm is None.
            temperature (float): Temperature for the model.
            parse_output (bool): If True, parse the output as JSON.
            **llm_kwargs: Additional keyword args forwarded to ChatOpenAI.
        """
        self.prompt = prompt
        self.parse_output = parse_output
        self.model = model
        self.temperature = temperature
        self.llm_kwargs = llm_kwargs
        self.llm = llm or ChatOpenAI(model=model, temperature=temperature, **llm_kwargs)

    def __call__(self, variables: Dict[str, Any]) -> Union[Dict[str, Any], str, List]:
        """
        Invoke the LangChain pipeline with a dict of variables for the prompt.

        Args:
            variables (Dict[str, Any]): Variables to format the ChatPromptTemplate.

        Returns:
            Union[Dict[str, Any], str, List]: Parsed JSON if parse_output else raw string; [] on parse error.
        """
        if not isinstance(variables, dict):
            raise TypeError("variables must be a dict")
        messages = self.prompt.format_messages(**variables)
        response = self.llm.invoke(messages)
        content = getattr(response, "content", str(response))
        try:
            cleaned = content.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned) if self.parse_output else content
        except Exception:
            print("Error parsing response from LangChainJSONChat.\n", content)
            return []

    def __repr__(self) -> str:
        return f"LangChainJSONChat(model={self.model}, temperature={self.temperature}, llm_kwargs={self.llm_kwargs})"

    def __str__(self) -> str:
        return self.__repr__()


def pretty_print(text: str, break_line_at: int = 90) -> str:
    """
    Pretty print a given text by inserting line breaks at specified intervals.

    Args:
        text (str): The text to be pretty printed.
        break_line_at (int): The maximum line length before inserting a line break.

    Returns:
        str: The pretty printed text.
    """
    words = text.split(" ")
    lines = []
    for word in words:
        if len(lines) == 0:
            lines.append(word)
        elif len(lines[-1]) + len(word) + 1 <= break_line_at:
            lines[-1] += " " + word
        else:
            lines.append(word)

    return "\n".join(lines)


PROMPT_TEMPLATES = {}


def load_md_prompts(prompt_category: str, prompt_name: str = None) -> Dict[str, str]:
    """
    Load Markdown prompts from a folder.

    Args:
        folder (str): The folder containing the Markdown files.

    Returns:
        Dict[str, str]: A dictionary mapping file names to their contents.
    """
    global PROMPT_TEMPLATES
    if prompt_category not in PROMPT_TEMPLATES or (
        prompt_name is not None and prompt_name not in PROMPT_TEMPLATES[prompt_category]
    ):
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
    if prompt_name is None:
        return PROMPT_TEMPLATES[prompt_category]
    if prompt_name in PROMPT_TEMPLATES[prompt_category]:
        return PROMPT_TEMPLATES[prompt_category][prompt_name]
    return None


def get_prompt(
    prompt_name: str, prompt_category: str = None, values: dict = None
) -> Optional[ChatPromptTemplate]:
    if prompt_category is None:
        prompt_category, prompt_name = prompt_name.split("/")

    prompt = load_md_prompts(prompt_category, prompt_name)
    if values:
        prompt = prompt.format(**values)
    return prompt


def chat_factory(model_name: str, temperature: float = 0.0, output_structure: Any = None, **kwargs):
    if ":" in model_name:
        return ChatOllama(model_name, temperature=temperature, **kwargs)
    elif "gpt" in model_name:
        result = ChatOpenAI(model_name=model_name, temperature=temperature, **kwargs)
        if output_structure is not None:
            result = result.with_structured_output(output_structure)
        return result

    return None
