from typing import List, Tuple

def build_mcp_prompt(
    query: str,
    results: List[Tuple[object, float]],
    system_instruction: str = "You are a legal compliance expert. Respond ONLY based on the provided context. If you don’t know the answer, say so."
) -> str:
    """
    Build a structured MCP (Model Context Protocol) prompt.
    Each result is a tuple (QdrantPoint, score).
    """
    context_blocks = []

    for idx, (res, score) in enumerate(results):
        payload = res.payload
        block = f"""### SOURCE {idx+1}
Source: {payload.get("source", "N/A")}
Article: {payload.get("article_id", "N/A")} - {payload.get("title", "N/A")}
Score: {score:.4f}

{payload.get("full_text", "[No full text available]")}
"""
        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    full_prompt = f"""{system_instruction}

### CONTEXT
{context}

### QUESTION
{query}

### ANSWER
"""
    return full_prompt