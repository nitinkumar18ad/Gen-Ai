import requests
from transformers import pipeline

# 🔑 Replace with your SerpAPI key
API_KEY = "1004b339048c7ad34bfd819e1f1990cb5a98aa68b3f37779f4e4f43217a0c50f"

# ✅ Better model for question answering
generator = pipeline("text2text-generation", model="google/flan-t5-base")


# 🔎 Get data from Google
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

    # Collect top 3 results
    if "organic_results" in data:
        for result in data["organic_results"][:3]:
            snippet = result.get("snippet", "")
            if snippet:
                snippets.append(snippet)

    # Limit context to avoid noise
    context = " ".join(snippets)
    return context[:500]


# 🤖 Generate clear answer
def generate_answer(context, query):
    prompt = f"""
Answer the question clearly and only based on the given context.

Context:
{context}

Question:
{query}

Answer:
"""

    result = generator(
        prompt,
        max_length=150,
        do_sample=False   # deterministic output (more clear)
    )

    answer = result[0]["generated_text"].strip()

    return answer


# 💬 Chatbot loop
def chatbot():
    print("AI Chatbot (Google + AI) started!")
    print("Type 'exit' to quit\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            print("Bot: Goodbye!")
            break

        context = search_google(query)

        if not context:
            print("Bot: No relevant information found.")
            continue

        answer = generate_answer(context, query)

        print("\nBot:", answer, "\n")


# ▶️ Run chatbot
if __name__ == "__main__":
    chatbot()