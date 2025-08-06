#!/bin/bash
#SBATCH --partition amdgpufast
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 1
#SBATCH --mem-per-cpu 96G
#SBATCH --gres gpu:1
#SBATCH --time 4:00:00
#SBATCH --job-name openwebui
#SBATCH --output logs/openwebui.%j.out

# Load required modules
ml Python/3.12.3-GCCcore-13.3.0
ml CUDA/12.6.0
ml OpenSSL/3

# Activate virtual environment
source /mnt/personal/ullriher/venvs/aug25/bin/activate

# Load environment variables
if [ -f ".env" ]; then
    source .env
fi

# Set up SSL certificate if needed
export SSL_CERT_FILE=~/ollama.crt

# Get hostname for external access
HOSTNAME=$(hostname -s)
echo "Running on host: $HOSTNAME"

# Find available ports
OLLAMA_PORT=$(shuf -i 20000-40000 -n 1)
while lsof -i TCP:$OLLAMA_PORT &>/dev/null; do
    OLLAMA_PORT=$(shuf -i 20000-40000 -n 1)
done

WEBUI_PORT=$(shuf -i 20000-40000 -n 1)
while lsof -i TCP:$WEBUI_PORT &>/dev/null || [ $WEBUI_PORT -eq $OLLAMA_PORT ]; do
    WEBUI_PORT=$(shuf -i 20000-40000 -n 1)
done

echo "Ollama will run on port: $OLLAMA_PORT"
echo "Open WebUI will run on port: $WEBUI_PORT"

# Export environment variables
export OLLAMA_HOST="http://$HOSTNAME:$OLLAMA_PORT"
export OLLAMA_BASE_URL="http://$HOSTNAME:$OLLAMA_PORT"

# Create logs directory if it doesn't exist
mkdir -p logs

# Create Docker volumes for persistence
docker volume create ollama-data 2>/dev/null || true
docker volume create openwebui-data 2>/dev/null || true

# Start Ollama container
echo "Starting Ollama container..."
docker run -d \
    --name ollama-${SLURM_JOB_ID} \
    --rm \
    --gpus all \
    -v ollama-data:/root/.ollama \
    -p ${OLLAMA_PORT}:11434 \
    ollama/ollama:latest > logs/ollama-container.${SLURM_JOB_ID}.log 2>&1

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
sleep 10
until curl -s http://$HOSTNAME:$OLLAMA_PORT > /dev/null 2>&1; do
    echo "Waiting for Ollama..."
    sleep 5
done
echo "Ollama is ready!"

# Start Open WebUI container
echo "Starting Open WebUI container..."
docker run -d \
    --name openwebui-${SLURM_JOB_ID} \
    --rm \
    -v openwebui-data:/app/backend/data \
    -p ${WEBUI_PORT}:8080 \
    -e OLLAMA_BASE_URL=http://$HOSTNAME:$OLLAMA_PORT \
    --add-host=host.docker.internal:host-gateway \
    ghcr.io/open-webui/open-webui:main > logs/openwebui-container.${SLURM_JOB_ID}.log 2>&1

# Wait for Open WebUI to be ready
echo "Waiting for Open WebUI to be ready..."
sleep 15
until curl -s http://$HOSTNAME:$WEBUI_PORT > /dev/null 2>&1; do
    echo "Waiting for Open WebUI..."
    sleep 5
done

# Log access information
echo "================================================================" | tee -a logs/openwebui.${SLURM_JOB_ID}.out
echo "🚀 Services are ready!" | tee -a logs/openwebui.${SLURM_JOB_ID}.out
echo "================================================================" | tee -a logs/openwebui.${SLURM_JOB_ID}.out
echo "📱 Open WebUI: http://$HOSTNAME:$WEBUI_PORT" | tee -a logs/openwebui.${SLURM_JOB_ID}.out
echo "🤖 Ollama API: http://$HOSTNAME:$OLLAMA_PORT" | tee -a logs/openwebui.${SLURM_JOB_ID}.out
echo "================================================================" | tee -a logs/openwebui.${SLURM_JOB_ID}.out

# Save connection info to files for easy access
echo "http://$HOSTNAME:$WEBUI_PORT" > logs/openwebui-url.${SLURM_JOB_ID}.log
echo "http://$HOSTNAME:$OLLAMA_PORT" > logs/ollama-url.${SLURM_JOB_ID}.log

# Function to cleanup containers on exit
cleanup() {
    echo "🧹 Cleaning up containers..."
    docker stop ollama-${SLURM_JOB_ID} openwebui-${SLURM_JOB_ID} 2>/dev/null || true
    echo "✅ Cleanup complete"
}

# Set trap to cleanup on script exit
trap cleanup EXIT

# Keep containers running and monitor logs
echo "🔄 Monitoring services... (Press Ctrl+C to stop)"
echo "📋 Container logs will be shown below:"
echo "================================================================"

# Monitor both containers
docker logs -f ollama-${SLURM_JOB_ID} &
docker logs -f openwebui-${SLURM_JOB_ID} &

# Wait for user interruption or job time limit
wait