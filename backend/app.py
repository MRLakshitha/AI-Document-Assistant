from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

from agents import ingestion_agent, qa_agent, summarizer_agent, highlight_agent

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        print("✅ File saved:", file_path)

        result = ingestion_agent(file_path)

        print("✅ Ingestion done")

        return jsonify({"message": result})

    except Exception as e:
        print("❌ ERROR IN UPLOAD:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/summary", methods=["GET"])
def summary():
    print("SUMMARY API HIT")
    result = summarizer_agent()
    print("RESULT:", result)
    return jsonify({"summary": result})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")
    return jsonify({"answer": qa_agent(question)})


@app.route("/highlights", methods=["GET"])
def highlights():
    return jsonify({"highlights": highlight_agent()})

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response

# 🔥 VERY IMPORTANT (this was missing)
if __name__ == "__main__":
  app.run(debug=False)
