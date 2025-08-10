"""
Reproduce Claimify paper in steps:
1. input question and answer
2. split into sentences & create context
--- per sentence ---
3. selection: contains any verifiable context?
4. disambiguation (if yes): contains ambiguity that cannot be resolved?
5. decomposition (if no): decomposed into at least one claim?
6. output extracted claims

"""
# from langchain import open ai llm, chat prompt template etc
from utils.chat import load_md_prompts