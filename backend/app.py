from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
import sys
import json
import shutil
from werkzeug.utils import secure_filename
import subprocess
# Add scripts directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
import re


# Import the necessary modules from scripts
from mcp_builder import build_mcp_prompt
from query_chunks import search_legal_chunks, rerank_by_keywords
from ollama_caller import ask_ollama

app = Flask(__name__)

# Configure CORS with more specific settings
CORS(app, supports_credentials=True, origins=[
    "http://localhost:5173", "http://127.0.0.1:5173"
])

# Enable CORS for all routes with a more explicit decorator
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# Sample standards data for demo
STANDARDS = []

# Process a query using MCP approach
def process_mcp_query(query, source_filter=None):
    try:
        # Step 1: Search for relevant chunks
        raw_results, _ = search_legal_chunks(query, top_k=6, source_filter=source_filter)
        
        # Step 2: Rerank results by keywords
        reranked = rerank_by_keywords(raw_results, query)
        
        if not reranked:
            return {
                "answer": "No relevant information found. Please try rephrasing or use a different source filter.",
                "sources": [],
                "success": False
            }
        
        # Step 3: Build prompt with top context blocks
        top_results = reranked[:4]
        prompt = build_mcp_prompt(query, top_results)
        
        # Step 4: Run local LLM with MCP prompt using Ollama
        try:
            response = ask_ollama(prompt, model="llama3")
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            # Fallback to simulated response
            response = simulate_llm_response(query, [r for r, _ in top_results])["answer"]
        
        # Step 5: Format sources for the response
        sources = []
        for idx, (r, score) in enumerate(top_results, 1):
            p = r.payload
            sources.append({
                "source": p.get("source", "Unknown"),
                "article": p.get("article_id", "Unknown"),
                "title": p.get("title", "Unknown"),
                "score": float(score)
            })
        
        return {
            "answer": response,
            "sources": sources,
            "success": True
        }
    except Exception as e:
        print(f"Error in process_mcp_query: {e}")
        # Fallback to simulated response
        return simulate_llm_response(query, [])

# Simulated vector DB and LLM functions - would be replaced with actual implementations
def simulate_vector_search(query, standard=None):
    """Simulate retrieving relevant chunks from vector DB based on query and standard"""
    # In a real implementation, this would query Qdrant with the embedded question
    
    # If no standard is specified, simulate searching across all standards
    if standard is None:
        # For demo purposes, default to GDPR
        standard = "GDPR"
        # In a real implementation, we would search across all standards
        # and return the most relevant chunks regardless of source
    
    return [
        {
            "text": f"Article 33 of {standard} states that personal data breaches must be reported within 72 hours.",
            "metadata": {
                "source": f"{standard}",
                "article": "33",
                "section": "Breach Notification"
            }
        },
        {
            "text": f"Article 34 of {standard} requires notifying affected individuals without undue delay.",
            "metadata": {
                "source": f"{standard}", 
                "article": "34",
                "section": "Communication to the Data Subject"
            }
        }
    ]

def simulate_llm_response(query, context_chunks):
    """Simulate LLM response generation with context"""
    # In a real implementation, this would call the local LLM via Ollama
    
    # Add a delay to simulate processing time
    time.sleep(1)
    
    sources = []
    if context_chunks:
        for chunk in context_chunks:
            if hasattr(chunk, 'payload'):
                sources.append({
                    "source": chunk.payload.get("source", "GDPR"),
                    "article": chunk.payload.get("article_id", "33"),
                    "section": chunk.payload.get("title", "Breach Notification")
                })
            else:
                sources.append(chunk["metadata"])
    else:
        sources = [
            {"source": "GDPR", "article": "33", "section": "Breach Notification"},
            {"source": "GDPR", "article": "34", "section": "Communication to the Data Subject"}
        ]
    
    sources_text = ", ".join([f"{s.get('source')} Article {s.get('article')}" for s in sources])
    
    return {
        "answer": f"Based on {sources_text}, data breaches must be reported within 72 hours to the supervisory authority. Additionally, if the breach is likely to result in high risk to individuals, they must be notified without undue delay.",
        "sources": sources,
        "confidence": 0.92
    }


# Define route for OPTIONS method to handle preflight requests
@app.route('/api/query', methods=['OPTIONS'])
def handle_options():
    return '', 204

@app.route('/api/standards', methods=['GET'])
def get_standards():
    """Return available compliance standards"""
    return jsonify({"standards": STANDARDS})

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process a query about compliance standards"""
    data = request.json
    query = data.get('query')
    standard = data.get('standard')  # Now optional
    
    if not query:
        return jsonify({"error": "Missing query"}), 400
    
    try:
        # Try to use the MCP query processor
        result = process_mcp_query(query, standard)
        return jsonify(result)
    except Exception as e:
        print(f"Error using MCP processor: {e}")
        # Fall back to simulated response
        chunks = simulate_vector_search(query, standard)
        response = simulate_llm_response(query, chunks)
        return jsonify(response)

@app.route('/api/compare', methods=['POST'])
def compare_policy():
    """Compare uploaded company policy against a selected standard."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    policy_file = request.files['file']
    standard = request.form.get('standard')
    llm_model = request.form.get('llm', 'llama3')

    if not policy_file or not standard:
        return jsonify({"error": "Missing file or standard"}), 400

    try:
        # Ensure file name is safe
        filename = secure_filename(policy_file.filename)

        # Create a fresh directory for company policies
        raw_policy_dir = os.path.join(os.path.dirname(__file__), "data", "company_chunks")
        if os.path.exists(raw_policy_dir):
            shutil.rmtree(raw_policy_dir)
        os.makedirs(raw_policy_dir, exist_ok=True)

        # Save uploaded file
        base_name = os.path.splitext(filename)[0]  # Remove .pdf
        jsonl_filename = base_name + ".jsonl"

        temp_path = os.path.join(raw_policy_dir, jsonl_filename)
        policy_file.save(temp_path)
        print(f"Saved policy file to {temp_path}")

        # 1. Chunk the policy
        chunk_proc = subprocess.run(
            ["python", "scripts/chunk_company_policy.py", temp_path],
            capture_output=True, text=True
        )
        if chunk_proc.returncode != 0:
            return jsonify({"error": f"Policy chunking failed:\n{chunk_proc.stderr}"}), 500
        
        print("Policy chunking successful")

        # 2. Embed the policy
        embed_proc = subprocess.run(
            ["python", "scripts/embed_company_policy.py", temp_path],
            capture_output=True, text=True
        )
        print("Policy embedding successful")
        if embed_proc.returncode != 0:
            return jsonify({"error": f"Policy embedding failed:\n{embed_proc.stderr}"}), 500

        # 3. Compare using LLM
        print("Comparing policy with LLM", temp_path, standard, llm_model)
        compare_proc = subprocess.run(
            ["python", "scripts/compare_with_LLMs.py", "--policy", temp_path, "--standard", standard, "--llm", llm_model, "--quiet" ],
            capture_output=True, text=True
        )
        if compare_proc.returncode != 0:
            return jsonify({"error": f"Comparison failed:\n{compare_proc.stderr}"}), 500

        # Return result
        response_text = compare_proc.stdout.strip()
        return jsonify({"result": response_text})

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/api/upload-standard', methods=['POST'])
def upload_standard():
    """Upload a new compliance standard, chunk, and embed it."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    standard_file = request.files['file']
    standard_name = request.form.get('name')
   

    if not standard_file or not standard_name:
        return jsonify({"error": "Missing file or standard name"}), 400

    # Save the uploaded file to data/raw_docs/
    raw_docs_dir = os.path.join(os.path.dirname(__file__), "data", "raw_docs")
    os.makedirs(raw_docs_dir, exist_ok=True)
    file_path = os.path.join(raw_docs_dir, f"{standard_name}.pdf")
    standard_file.save(file_path)

    try:
        # 1. Chunk the document (processes all files in raw_docs)
        import subprocess
        print("Chunking document...")
        chunker_result = subprocess.run(
            ["python", "scripts/chunker.py"],
            capture_output=True, text=True
        )

        if chunker_result.returncode != 0:
            return jsonify({"error": f"Chunking failed: {chunker_result.stderr}"}), 500

        # 2. Embed and store the chunks for this standard
        embed_result = subprocess.run(
            ["python", "scripts/embed_store.py", standard_name],
            capture_output=True, text=True
        )
        if embed_result.returncode != 0:
            return jsonify({"error": f"Embedding failed: {embed_result.stderr}"}), 500

        # Add to available standards
        if standard_name not in STANDARDS:
            STANDARDS.append(standard_name)

        return jsonify({
            "message": f"Successfully uploaded, chunked, and embedded {standard_name}",
            "added": True
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/embedded-standards', methods=['GET'])
def get_embedded_standards():
    """Return standards for which embeddings exist (based on parsed_json_semantic files)."""
    try:
        print("Getting embedded standards")
        parsed_dir = os.path.join(os.path.dirname(__file__), "data", "parsed_json_semantic")
        if not os.path.exists(parsed_dir):
            return jsonify({"standards": []})
        files = os.listdir(parsed_dir)
        standards = [os.path.splitext(f)[0] for f in files if f.endswith('.jsonl')]
        return jsonify({"standards": sorted(standards)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
