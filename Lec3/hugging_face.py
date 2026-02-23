import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ------------------ LOAD MODEL ------------------
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

model.eval()
torch.set_grad_enabled(False)

# ------------------ INPUT ------------------
prompt = "The capital of India is"

inputs = tokenizer(
    prompt,
    return_tensors="pt",
    padding=True,
    truncation=True
)

# Move to device
inputs = {k: v.to(device) for k, v in inputs.items()}

# ------------------ GENERATE ------------------
output_ids = model.generate(
    inputs["input_ids"],
    attention_mask=inputs["attention_mask"],   # IMPORTANT

    max_new_tokens=30,

    do_sample=True,
    temperature=0.8,
    top_k=50,
    top_p=0.9,

    repetition_penalty=1.3,
    no_repeat_ngram_size=3,

    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id
)

# ------------------ DECODE ------------------
output = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("\nOutput:\n", output)