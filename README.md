# 📄 AI Document Assistant

An AI-powered web application that allows users to upload PDF documents and interact with them using intelligent features like summarization, question answering, and key highlights.

---

## 🚀 Features

- 📤 Upload PDF documents
- 🧠 AI-generated summary of documents
- ❓ Ask questions based on document content
- ✨ Extract important highlights
- ⚡ Fast semantic search using vector database (FAISS)

---

## 🛠️ Tech Stack

### Frontend
- React (Vite)
- Axios

### Backend
- Flask (Python)
- LangChain

### AI & NLP
- HuggingFace Embeddings (`all-MiniLM-L6-v2`)
- Groq API (LLM)

### Vector Database
- FAISS

---

## 📂 Project Structure
ai-agent-docs/
│
├── frontend/ # React frontend
│ └── client/
│
├── backend/ # Flask backend
│ ├── app.py
│ ├── agents.py
│ ├── uploads/
│ └── venv/
│
└── README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/AI-Document-Assistant.git
cd AI-Document-Assistant

cd backend
python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt

.env -GROQ_API_KEY=your_groq_api_key

run -python app.py

frontend -cd frontend/client
npm install
npm run dev
