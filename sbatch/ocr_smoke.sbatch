#!/usr/bin/env bash
#SBATCH --job-name=ocr-smoke
#SBATCH --partition=sched_mit_sloan_gpu_r8
#SBATCH --gres=gpu:a100:2
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --time=01:00:00
#SBATCH --output=/orcd/home/002/eeshan/philosophy/handoffs/ocr_logs/smoke_%j.out
#SBATCH --error=/orcd/home/002/eeshan/philosophy/handoffs/ocr_logs/smoke_%j.err

set -euo pipefail

module purge
module load gcc/12.2.0 cuda/12.9.1 cudnn/9.8.0.87-cuda12 miniforge/25.11.0-0

export HF_HOME=/orcd/scratch/orcd/009/eeshan/hf_cache
export TRANSFORMERS_CACHE="$HF_HOME"
export VLLM_CACHE_ROOT=/orcd/scratch/orcd/009/eeshan/cache/vllm
export TORCH_HOME=/orcd/scratch/orcd/009/eeshan/cache/torch
export TOKENIZERS_PARALLELISM=false
export PYTHONUNBUFFERED=1

source /orcd/scratch/orcd/009/eeshan/venvs/ocr/bin/activate

# Default to Bhāskara p. 50 unless overridden.
PDF="${PDF_PATH:-/orcd/home/002/eeshan/philosophy/materials/primary_texts/sanskrit/_replaced/bhaskara_brahma_sutra_bhasya_dvivedi_1915_archive.pdf}"
PAGE="${PAGE_INDEX:-50}"
OUT="${OUT_DIR:-/orcd/home/002/eeshan/philosophy/tmp/ocr_smoke/bhaskara_p${PAGE}}"

mkdir -p "$OUT"

# Launch vLLM servers in background — Qwen on GPUs 0-1, InternVL on GPUs 2-3.
CUDA_VISIBLE_DEVICES=0,1 vllm serve Qwen/Qwen2.5-VL-72B-Instruct-AWQ \
  --tensor-parallel-size 2 --port 8000 --quantization awq \
  > "$OUT/vllm_qwen.log" 2>&1 &
QWEN_PID=$!
CUDA_VISIBLE_DEVICES=2,3 vllm serve OpenGVLab/InternVL2_5-78B-AWQ \
  --tensor-parallel-size 2 --port 8001 --quantization awq \
  > "$OUT/vllm_internvl.log" 2>&1 &
INTERN_PID=$!
trap "kill $QWEN_PID $INTERN_PID 2>/dev/null || true" EXIT

# Wait until both servers are responsive (≤ 6 min).
for engine in 8000 8001; do
  for i in $(seq 1 72); do
    if curl -sf "http://127.0.0.1:${engine}/v1/models" > /dev/null; then
      echo "[ready] vLLM port $engine after ${i}*5s"
      break
    fi
    sleep 5
  done
done

python -m philosophy_ocr.cli ocr-page \
  --pdf "$PDF" \
  --page "$PAGE" \
  --out "$OUT" \
  --tensor-parallel 2

cp "$OUT/page_${PAGE}_agreement.md" \
   "/orcd/home/002/eeshan/philosophy/tmp/ocr_smoke/page_$(printf %04d $PAGE)_agreement.md" \
   2>/dev/null || true
