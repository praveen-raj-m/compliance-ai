#!/usr/bin/env python
import sys
import importlib
import subprocess
import os

# Check Python version
print(f"Python version: {sys.version}")
min_version = (3, 8)
if sys.version_info < min_version:
    print(f"⚠️ WARNING: Python {min_version[0]}.{min_version[1]} or higher is recommended")

# Required packages
required_packages = [
    "flask",
    "flask-cors",
    "qdrant-client",
    "sentence-transformers",
    "numpy", 
    "requests",
    "pypdf"
]

# Check if Ollama is installed
try:
    print("\nChecking for Ollama...")
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Ollama is installed: {result.stdout.strip()}")
    else:
        print(f"⚠️ Ollama seems to be installed but returned an error: {result.stderr}")
except FileNotFoundError:
    print("⚠️ Ollama is not installed or not in PATH. Please install Ollama from https://ollama.ai/")

# Check for required packages
print("\nChecking Python packages:")
missing_packages = []
for package in required_packages:
    try:
        importlib.import_module(package.replace("-", "_"))  # Replace hyphens with underscores for import
        print(f"✅ {package}")
    except ImportError:
        missing_packages.append(package)
        print(f"❌ {package}")

# Check Qdrant connection
try:
    print("\nChecking Qdrant connection...")
    from qdrant_client import QdrantClient
    client = QdrantClient(host="localhost", port=6333)
    client.get_collections()
    print("✅ Successfully connected to Qdrant")
except Exception as e:
    print(f"❌ Could not connect to Qdrant: {e}")
    print("Make sure Qdrant is installed and running on localhost:6333")

# Suggest installation command for missing packages
if missing_packages:
    print("\n⚠️ Missing packages. Install them with:")
    print(f"pip install {' '.join(missing_packages)}")
else:
    print("\n✅ All required Python packages are installed.")

# Check if scripts are properly set up
print("\nChecking scripts...")
scripts_dir = os.path.join(os.path.dirname(__file__), "scripts")
required_scripts = [
    "run_mcp_query.py",
    "mcp_builder.py",
    "query_chunks.py",
    "ollama_caller.py"
]

for script in required_scripts:
    script_path = os.path.join(scripts_dir, script)
    if os.path.exists(script_path):
        print(f"✅ {script}")
    else:
        print(f"❌ {script} is missing")

print("\nEnvironment check complete.") 