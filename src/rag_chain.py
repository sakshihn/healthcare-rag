import sys
sys.path.append('src')

import os
import time
from dotenv import load_dotenv
from groq import Groq
from retriever import retrieve
from prompt import build_prompt, format_sources

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
MODEL = 'llama-3.3-70b-versatile'


def ask(question, n_chunks=5):
    start = time.time()

    print(f"\nQuestion: {question}")
    print("Retrieving relevant chunks...")
    chunks = retrieve(question, n_results=n_chunks)

    if not chunks:
        return {
            'answer': 'No relevant information found.',
            'sources': [],
            'sources_formatted': '',
            'latency': 0,
            'tokens': 0
        }

    avg_similarity = round(
        sum(c['similarity'] for c in chunks) / len(chunks), 3
    )
    top_similarity = round(chunks[0]['similarity'], 3)

    print(f"Found {len(chunks)} chunks (top similarity: {top_similarity})")
    print("Asking Groq...")

    system_prompt, user_message = build_prompt(question, chunks)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ],
        temperature=0.1,
        max_tokens=500
    )

    answer = response.choices[0].message.content
    latency = round(time.time() - start, 2)
    tokens = response.usage.total_tokens

    print(f"Done in {latency}s | tokens: {tokens}")


    return {
        'answer': answer,
        'sources': chunks,
        'sources_formatted': format_sources(chunks),
        'latency': latency,
        'tokens': tokens
    }


if __name__ == '__main__':
    result = ask("What is the role of metformin in diabetes treatment?")
    print("\n" + "="*60)
    print("ANSWER:")
    print(result['answer'])
    print("\nSOURCES:")
    print(result['sources_formatted'])