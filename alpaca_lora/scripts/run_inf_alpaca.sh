#!/bin/bash
src=src
tgt=tgt

export CUDA_VISIBLE_DEVICES=4

data_dir=/opt/data/private/data/llama/llama_raw/inf/data-bin/
llama_dir=/opt/data/private/data/llama/7B/
lora_dir=/opt/data/private/ckpt/alpaca/lora/checkpoint3.pt
# lora_dir=/opt/data/private/ckpt/alpaca/parallel_lora/checkpoint3-model_part-0.pt
bpe_dir=/opt/data/private/data/llama/tokenizer.model
world_size=1


torchrun --master_port 29005 --nproc_per_node $world_size alpaca_lora/src/generate.py $data_dir \
    --user-dir alpaca_lora/src \
    --task llama_task \
    --lora-model-inf $lora_dir \
    --arch llama_7b \
    --lora-tuning \
    -s $src -t $tgt \
    --gen-subset test \
    --bpe 'sentencepiece' --sentencepiece-model $bpe_dir \
    --path $llama_dir/model.pt \
    --seed 1 \
    --required-batch-size-multiple 1 \
    --batch-size 1 \
    --beam 1 --sampling --sampling-topp 0.95 --temperature 0.8 \
