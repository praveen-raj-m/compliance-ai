# Compliance AI Assistant

A fully local compliance assistant that enables users to query regulations and verify company policies against compliance standards, without relying on cloud services.

## Features

- Query compliance standards like GDPR, ISO27001, NIST, and HIPAA using natural language
- Upload and analyze company policies against compliance standards
- Identifies covered, partially covered, and uncovered compliance areas
- Fully local processing with no data sent to external APIs
- Semantic search and context-aware prompt generation
- Dark-themed modern UI built with React and TailwindCSS

## Architecture

- **Frontend**: React with Vite and TailwindCSS
- **Backend**: Flask API server
- **Vector Database**: Qdrant for semantic search
- **LLM**: Local model via Ollama (LLaMA 3)
- **Document Processing**: Chunking and semantic enrichment of regulations and policies

## Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- [Ollama](https://ollama.ai/) with LLaMA 3 model installed
- [Qdrant](https://qdrant.tech/documentation/quick-start/) vector database

## Setup Instructions

### Backend Setup

1. Create a Python virtual environment:

   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Verify your environment is properly set up:

   ```
   python check_env.py
   ```

4. Start the Qdrant server (if not already running):

   ```
   docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
   ```

5. Start the Flask server:
   ```
   python app.py
   ```

### Frontend Setup

1. Install dependencies:

   ```
   cd frontend
   npm install
   ```

2. Start the development server:

   ```
   npm run dev
   ```

3. Access the application at `http://localhost:5173`

### Ollama Setup

1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull the LLaMA 3 model:
   ```
   ollama pull llama3
   ```
3. Verify Ollama is running:
   ```
   ollama list
   ```

## Complete System Startup

For the full system to work, make sure you have:

1. Qdrant running (via Docker or local installation)
2. Ollama service running with the llama3 model pulled
3. Backend Flask server running
4. Frontend development server running

To test if everything is working:

1. Upload a compliance standard document through the UI
2. Ask a question about compliance regulations
3. Check that you receive a properly formatted response with sources

## Usage

1. **Querying Regulations**:

   - Select a compliance standard
   - Type your question
   - View the AI-generated response with references

2. **Analyzing Company Policies**:
   - Upload your company policy document
   - Select the compliance standard to compare against
   - Review the compliance analysis showing covered and gaps areas

## Project Structure

- `/frontend`: React frontend application
- `/backend`: Flask API server
- `/backend/data`: Storage for regulations and uploaded documents
- `/backend/scripts`: Processing scripts for documents and vector operations
