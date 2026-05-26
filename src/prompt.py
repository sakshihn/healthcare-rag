def build_prompt(question, chunks):
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"[Source {i+1} | PMID: {chunk['pmid']}]\n{chunk['text']}"
        )
    context = "\n\n".join(context_parts)

    system_prompt = """You are a medical research assistant.
You answer questions using ONLY the provided research abstracts.
Rules you must follow:
- Only use information from the provided sources
- Always cite which source number you used: (Source 1), (Source 2) etc
- If the sources don't contain enough information, say so honestly
- Never make up medical information
- Keep answers clear and factual
- Do not recommend treatments to individuals"""

    user_message = f"""Here are the relevant research abstracts:

{context}

Question: {question}

Answer using only the above sources and cite them."""

    return system_prompt, user_message


def format_sources(chunks):
    lines = []
    for i, chunk in enumerate(chunks):
        lines.append(
            f"Source {i+1}: PMID {chunk['pmid']} "
            f"(similarity: {chunk['similarity']})"
        )
    return "\n".join(lines)