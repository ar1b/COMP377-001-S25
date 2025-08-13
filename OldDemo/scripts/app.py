from flask import Flask, request, jsonify
from rag_chain import get_rag_chain
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend use

# Initialize the RAG pipeline
qa_chain = get_rag_chain()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    
    if not question:
        return jsonify({"error": "Missing question"}), 400

    try:
        result = qa_chain(question)
        answer = result["result"]
        sources = [doc.metadata.get("source", "Unknown") for doc in result.get("source_documents", [])]
        return jsonify({
            "answer": answer,
            "sources": sources
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
