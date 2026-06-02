def build_prompt(question, chunks, chat_history=None):
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
- Do not recommend treatments to individuals
- Consider previous questions in the conversation for context"""

    history_text = ""
    if chat_history:
        history_text = "\n\nPrevious conversation:\n"
        for msg in chat_history[-4:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content'][:200]}\n"

    user_message = f"""Here are the relevant research abstracts:

{context}
{history_text}
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