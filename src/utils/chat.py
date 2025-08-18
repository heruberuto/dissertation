import os, re
from typing import Any, Dict, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

PROMPT_SEPARATOR = "\n# user message"
PROMPT_TEMPLATES = {}


def load_md_prompts(prompt_category: str) -> Dict[str, str]:
    global PROMPT_TEMPLATES
    if prompt_category not in PROMPT_TEMPLATES:
        prompt_templates = {}
        folder = os.path.join(os.path.dirname(__file__), "../../prompts", prompt_category)
        for filename in os.listdir(folder):
            if filename.endswith(".md"):
                with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                    prompts = re.split(PROMPT_SEPARATOR, f.read(), flags=re.IGNORECASE)
                    messages = [("system", prompts[0].strip())]
                    if len(prompts) == 2:
                        messages.append(("user", prompts[1].strip()))
                    prompt_templates[filename.replace(".md", "")] = ChatPromptTemplate.from_messages(messages)
        PROMPT_TEMPLATES[prompt_category] = prompt_templates
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
