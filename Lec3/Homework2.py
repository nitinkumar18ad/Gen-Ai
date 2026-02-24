import requests
from transformers import pipeline

API_KEY = "1004b339048c7ad34bfd819e1f1990cb5a98aa68b3f37779f4e4f43217a0c50f"

# Load small model
generator = pipeline("text-generation", model="distilgpt2")

def search_google(query):
    url = "https://serpapi.com/search.json"

    params = {
        "q": query,
        "api_key": API_KEY,
        "engine": "google"
    }

    response = requests.get(url, params=params)
    data = response.json()

    snippets = []

    if "organic_results" in data:
        for result in data["organic_results"][:3]:
            snippets.append(result.get("snippet", ""))

    return " ".join(snippets)


def generate_answer(context, query):
    prompt = f"Answer the question based on context:\nContext: {context}\nQuestion: {query}\nAnswer:"
    
    result = generator(prompt, max_length=150, num_return_sequences=1)
    
    return result[0]['generated_text']


def chatbot():
    print("AI Chatbot (Google + AI) started!\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            break

        context = search_google(query)
        answer = generate_answer(context, query)

        print("\nBot:\n", answer)


if __name__ == "__main__":
    chatbot()