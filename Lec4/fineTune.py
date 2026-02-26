import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling
)

# ==============================
# 1. DATASET (ADD MORE FOR BETTER RESULTS)
# ==============================

data = [
    {"input": "What is AI?", "output": "Artificial Intelligence is the simulation of human intelligence in machines."},
    {"input": "What is Python?", "output": "Python is a high-level programming language used for many applications."},
    {"input": "Explain DBMS", "output": "DBMS is a software system used to store, manage and retrieve data efficiently."},
    {"input": "What is Machine Learning?", "output": "Machine Learning is a subset of AI that enables systems to learn from data."},
    {"input": "What is JavaScript?", "output": "JavaScript is a programming language mainly used for web development."}
]

# Better instruction format
def format_data(example):
    return {
        "text": f"### Instruction:\n{example['input']}\n\n### Response:\n{example['output']}"
    }

formatted_data = [format_data(x) for x in data]
dataset = Dataset.from_list(formatted_data)

# ==============================
# 2. LOAD MODEL
# ==============================

model_name = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # important

model = AutoModelForCausalLM.from_pretrained(model_name)

# ==============================
# 3. TOKENIZATION
# ==============================

def tokenize_function(example):
    tokens = tokenizer(
        example["text"],
        padding="max_length",
        truncation=True,
        max_length=128
    )
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# ==============================
# 4. TRAINING SETUP
# ==============================

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=10,
    per_device_train_batch_size=2,
    logging_steps=5,
    save_steps=50,
    learning_rate=5e-5,
    fp16=torch.cuda.is_available()
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator
)

# ==============================
# 5. TRAIN MODEL
# ==============================

print("Training started...")
trainer.train()

# ==============================
# 6. SAVE MODEL
# ==============================

model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")

print("Model saved!")

# ==============================
# 7. CHAT FUNCTION (FIXED)
# ==============================

def chat():
    print("\n🤖 Chatbot ready! Type 'exit' to stop.\n")

    tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_model")
    model = AutoModelForCausalLM.from_pretrained("./fine_tuned_model")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        input_text = f"### Instruction:\n{user_input}\n\n### Response:\n"

        inputs = tokenizer(
            input_text,
            return_tensors="pt",
            padding=True,
            truncation=True
        )

        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],  # FIX
            max_length=150,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            repetition_penalty=1.2,     # reduce repetition
            no_repeat_ngram_size=3,     # avoid loops
            pad_token_id=tokenizer.eos_token_id
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Clean output
        if "### Response:" in response:
            reply = response.split("### Response:")[-1].strip()
        else:
            reply = response

        print("Bot:", reply)


# ==============================
# 8. START CHAT
# ==============================

chat()