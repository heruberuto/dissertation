# Automated Fact Checking in Czech

This repository contains code and experiments for my dissertation on automated fact checking in the Czech language.

## Overview

The project focuses on developing and evaluating automated fact checking systems specifically designed for Czech text. This includes:

- **Dataset Development**: Creating and curating Czech fact checking datasets
- **Model Development**: Training and fine-tuning language models for Czech fact verification
- **Evaluation**: Comprehensive evaluation of fact checking performance on Czech content
- **Analysis**: Comparative studies of different approaches and methodologies

## Project Structure

- `src/` - Source code and utilities
  - `utils/` - Utility functions and classes (e.g., chat interfaces)
  - `prompts/` - Prompt templates and configurations
    - `claimify/` - Claimify prompts for claim extraction and evaluation, authored by [Metropolitansky & Larson (2025)](https://aclanthology.org/2025.acl-long.348/)
- `notebooks/` - Jupyter notebooks for experiments and analysis
- `script/` - SLURM job scripts and utility scripts for HPC deployment
- `logs/` - Job output and server logs
- `requirements.txt` - Python dependencies for ML/NLP tasks

## Technology Stack

- **Environment**: HPC clusters with SLURM job scheduling
- **ML Framework**: PyTorch with CUDA support, Transformers, LangChain
- **NLP Libraries**: spaCy, NLTK, sentence-transformers
- **Data Processing**: pandas, PyMuPDF, trafilatura
- **Search/Retrieval**: FAISS, rank-bm25
- **LLM Integration**: Ollama, OpenAI API, Hugging Face
- **Czech Language Focus**: Specialized for Czech text processing and fact-checking

## Research Focus

The dissertation addresses the challenges of automated fact checking in Czech, including:
- Language-specific linguistic patterns and structures
- Czech-specific misinformation patterns
- Evaluation metrics adapted for Czech language characteristics
- Cross-lingual transfer learning approaches

## Getting Started

See `CLAUDE.md` for detailed setup instructions including environment configuration and SLURM job submission.

## Credits and References

The Claimify prompts in `src/prompts/claimify/` are adapted from:

> Metropolitansky, Dasha and Larson, Jonathan. "Towards Effective Extraction and Evaluation of Factual Claims." *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*. Vienna, Austria: Association for Computational Linguistics, July 2025, pages 6996-7045. DOI: 10.18653/v1/2025.acl-long.348

```bibtex
@inproceedings{metropolitansky-larson-2025-towards,
    title = "Towards Effective Extraction and Evaluation of Factual Claims",
    author = "Metropolitansky, Dasha and Larson, Jonathan",
    editor = "Che, Wanxiang and Nabende, Joyce and Shutova, Ekaterina and Pilehvar, Mohammad Taher",
    booktitle = "Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2025",
    address = "Vienna, Austria",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.acl-long.348/",
    doi = "10.18653/v1/2025.acl-long.348",
    pages = "6996--7045",
    ISBN = "979-8-89176-251-0"
}

