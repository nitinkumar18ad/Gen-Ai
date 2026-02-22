import os 
import torch

os.environ["HF_TOKEN"] ="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" 

model_name = "bert-base-uncased"

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(model_name)

print(tokenizer("Hello,how are you?"))
print(tokenizer.get_vocab())

input_tokens = tokenizer("Hello,how are you")["input_ids"]
print(input_tokens)

from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16
)

from transformers import pipeline
gen_pipeline = pipeline("text-generation",model=model, tokenizer=tokenizer)

gen_pipeline("Hey there", max_new_tokens=15)