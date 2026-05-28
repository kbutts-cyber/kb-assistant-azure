from openai import AzureOpenAI
from config import get_openai_key, get_openai_endpoint

def get_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=get_openai_key(),
        azure_endpoint=get_openai_endpoint(),
        api_version="2024-02-01"
    )

def ask_question(question: str, context_chunks: list[dict]) -> str:
    """Send question + relevant context to Azure OpenAI and return the answer."""
    client = get_client()

    context = "\n\n".join([
        f"Source: {chunk['source']}\n{chunk['text']}"
        for chunk in context_chunks
    ])

    system_prompt = """You are a helpful knowledge base assistant. 
Answer questions using only the context provided below.
If the answer is not in the context, say so clearly.
Be concise and accurate."""

    user_message = f"""Context:
{context}

Question: {question}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=500,
        temperature=0.3
    )

    return response.choices[0].message.content