#!/usr/bin/env bash
#SBATCH --job-name=ocr-skt
#SBATCH --partition=sched_mit_sloan_gpu_r8
#SBATCH --gres=gpu:a100:4
#SBATCH --cpus-per-task=32
#SBATCH --mem=256G
#SBATCH --time=23:50:00
#SBATCH --output=/orcd/home/002/eeshan/philosophy/handoffs/ocr_logs/%x_%j.out
#SBATCH --error=/orcd/home/002/eeshan/philosophy/handoffs/ocr_logs/%x_%j.err
#SBATCH --signal=B:USR1@300

set -euo pipefail

module purge
module load gcc/12.2.0 cuda/12.9.1 cudnn/9.8.0.87-cuda12 miniforge/25.11.0-0

export HF_HOME=/orcd/pool/008/eeshan/ocr/hf_cache
export TRANSFORMERS_CACHE="$HF_HOME"
export VLLM_CACHE_ROOT=/orcd/pool/008/eeshan/ocr/cache_vllm
export TORCH_HOME=/orcd/pool/008/eeshan/ocr/cache_torch
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=8

source /orcd/pool/008/eeshan/ocr/venvs/ocr/bin/activate

PDF="${PDF_PATH:?PDF_PATH must be set}"
OUT="${OUT_DIR:?OUT_DIR must be set}"

mkdir -p "$OUT"

python -m philosophy_ocr.cli ocr-book \
  --pdf "$PDF" \
  --out "$OUT" \
  --vllm-port 8000 \
  --tensor-parallel 2 \
  --resume
