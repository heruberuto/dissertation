# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment Setup

This project is a Czech fact-checking research repository that runs on HPC clusters with SLURM job scheduling. The environment requires:

- Python 3.12.3 with specific ML libraries (see requirements.txt)
- CUDA 12.6.0 for GPU acceleration
- Ollama for local LLM inference
- Virtual environment at `/mnt/personal/ullriher/venvs/aug25/`

## Key Commands

### Development Environment
```bash
# Activate virtual environment
source /mnt/personal/ullriher/venvs/aug25/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set Python path for src modules
export PYTHONPATH=src:$PYTHONPATH
```

### SLURM Job Submission
```bash
# Submit Jupyter notebook job with GPU
sbatch script/_slurm_job.sh

# Submit job with Ollama server + Jupyter
sbatch script/_slurm_job_ollama.sh

# Submit job with Ollama + Open WebUI (web-based chat interface)
sbatch script/_slurm_job_openwebui.sh

# Get Jupyter notebook URL from logs
python script/jupyter_url.py

# Get Open WebUI and Ollama API URLs from logs
python script/openwebui_url.py
```

### Ollama Setup
```bash
# Install Ollama (custom installer for HPC)
bash script/ollama/install.sh

# Pull required models
ollama pull gpt-oss:20b
```

## Project Architecture

### Core Structure
- `notebooks/` - Jupyter notebooks for experiments and analysis
- `script/` - SLURM job scripts and utility scripts
- `logs/` - Job output and Ollama server logs
- `requirements.txt` - Python dependencies for ML/NLP tasks

### Technology Stack
- **ML Framework**: PyTorch with CUDA support, Transformers, LangChain
- **NLP Libraries**: spaCy, NLTK, sentence-transformers
- **Data Processing**: pandas, PyMuPDF (PDF processing), trafilatura (web scraping)
- **Search/Retrieval**: FAISS, rank-bm25
- **LLM Integration**: Ollama, OpenAI API, Hugging Face
- **Czech Language Focus**: Specialized for Czech text processing and fact-checking

### SLURM Configuration
- Uses AMD GPU partitions (`amdgpu`, `amdgpufast`)
- 96GB memory per CPU, single GPU allocation
- Jobs run with custom SSL certificates for secure communication
- Ollama server runs on random high ports (20000-40000) to avoid conflicts

### Development Workflow
1. Submit SLURM job to get compute resources with GPU
2. Access Jupyter notebook via generated URL or use Open WebUI for web-based chat
3. Use Ollama for local LLM inference alongside cloud APIs
4. Experiment with Czech language models and fact-checking datasets

### Available Interfaces
- **Jupyter Notebooks**: Traditional notebook environment for development and analysis
- **Open WebUI**: Modern web-based chat interface for interacting with Ollama models
- **Direct API**: Raw Ollama API access for programmatic usage

## Important Notes

- All development happens in Jupyter notebooks on HPC infrastructure
- The project focuses specifically on Czech language fact-checking
- Custom Ollama installation supports the HPC environment constraints
- Jobs automatically handle port conflicts and SSL certificate management
- Use `script/jupyter_url.py` to extract notebook URLs from SLURM logs
- Use `script/openwebui_url.py` to extract Open WebUI and Ollama API URLs
- Docker containers provide isolated environments for Ollama and Open WebUI services