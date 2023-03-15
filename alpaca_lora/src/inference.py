# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import torch
from llama_model import LLaMA
import argparse
import logging

logger = logging.getLogger(__name__)


@torch.no_grad()
def generate(alpaca):
    
    prompts = [
        "tell a story about Sleeping Beauty, please.",
        "write a e-mail to congratulate Lee and mention that you are exited about meeting all of them in person.",
        "what is an alpaca? how is it different form a llama?",
    ]

    # load from files
    # prompts = open("alpaca_lora/scripts/test.src").readlines()

    eval_kwargs = dict(beam=1, sampling=True, sampling_topp=0.95, temperature=0.8)
    for prompt in prompts:
        print("-----" * 20)
        print("Question: {}".format(prompt))
        output = alpaca.sample([prompt], **eval_kwargs)[0][0]
        print("Alpaca Answer:\n{}".format(output))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model-dir",
        required=True,
        type=str,
        default="alpaca_lora",
        help="path containing model file and src_dict.txt",
    )
    parser.add_argument(
        "--model-file",
        default="checkpoint_best.pt",
        help="where in model_dir are weights saved",
    )
    parser.add_argument(
        "--llama-model-inf",
        default="checkpoint_best.pt",
        help="where in model_dir are weights saved",
    )
    parser.add_argument("--bpe",)
    parser.add_argument("--sentencepiece-model")
    args = parser.parse_args()
    
    kwargs = {
        "user_dir": "alpaca_lora/src", 
        "llama_model_inf": args.llama_model_inf,
        "bpe": args.bpe,
        "sentencepiece_model": args.sentencepiece_model,
    }
    alpaca = LLaMA.from_pretrained(
        model_name_or_path=args.model_dir,
        checkpoint_file=args.model_file,
        **kwargs,
    )
    alpaca = alpaca.eval()
    if torch.cuda.is_available():
        alpaca = alpaca.cuda().half()
    
    generate(alpaca)


if __name__ == "__main__":
    main()