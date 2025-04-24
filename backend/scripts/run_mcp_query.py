


import subprocess
from mcp_builder import build_mcp_prompt
from query_chunks import search_legal_chunks, rerank_by_keywords

def run_llama3(prompt: str) -> str:
    # Call local LLaMA 3 model using Ollama
    process = subprocess.Popen(
        ["ollama", "run", "llama3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output, error = process.communicate(input=prompt)
    return output.strip()

if __name__ == "__main__":
    print(" Welcome to Compliance Assistant (powered by LLaMA 3 + MCP + Qdrant)")
    print("Type 'exit' to quit.\n")

    while True:
        query = input(" Enter your compliance question: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        source = input(" Filter by source (e.g. GDPR, ISO27001) or press Enter: ").strip() or None
        if source:
            source = source.upper().replace(" ", "_")

        raw_results, _ = search_legal_chunks(query, top_k=6, source_filter=source)

        print("⏳ Reranking results...", end="", flush=True)
        reranked = rerank_by_keywords(raw_results, query)
        print(" done.")

        if not reranked:
            print("⚠️ No results found. Try without source filter or recheck chunking.\n")
            continue

        # Build prompt with top 4 context blocks
        top_results = reranked[:4]
        prompt = build_mcp_prompt(query, top_results)

        # Run local LLM with MCP prompt
        response = run_llama3(prompt)

        # Print clean final output
        print("\n Answer:")
        print(response)

        print("\n Sources used:")
        for idx, (r, _) in enumerate(top_results, 1):
            p = r.payload
            print(f"Source {idx}: {p.get('source')} — Article: {p.get('article_id')} ({p.get('title')})")

        print("\n" + "-" * 100 + "\n")
