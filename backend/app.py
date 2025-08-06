from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import openai
from utils.document_processor import process_document
from utils.vector_db import VectorDB
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
vector_db = VectorDB()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{timestamp}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    
    file.save(filepath)
    
    # Process document and store in vector DB
    try:
        document_content = process_document(filepath)
        vector_db.add_document(unique_filename, document_content)
        return jsonify({
            "status": "success", 
            "filename": unique_filename,
            "message": f"Document processed and stored successfully"
        })
    except Exception as e:
        return jsonify({"error": f"Document processing failed: {str(e)}"}), 500

@app.route('/query', methods=['POST'])
def query_documents():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "No query provided"}), 400
    
    query = data['query']
    
    try:
        # Get relevant document chunks
        relevant_chunks = vector_db.query(query)
        
        # Generate response using LLM
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": """
                    You are a document analysis assistant. 
                    Answer questions based ONLY on the provided document chunks.
                    Format your response as JSON with 'answer' and 'explanation' keys.
                    Be concise and factual.
                """},
                {"role": "user", "content": f"""
                    Document chunks: {relevant_chunks}
                    
                    Question: {query}
                    
                    Provide:
                    1. A direct answer to the question
                    2. A step-by-step explanation of how you arrived at the answer
                """}
            ],
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message['content'])
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Query processing failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
