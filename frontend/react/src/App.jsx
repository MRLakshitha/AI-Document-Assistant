import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [summary, setSummary] = useState("");
  const [highlights, setHighlights] = useState([]);

  const uploadFile = async () => {
    const formData = new FormData();
    formData.append("file", file);

    await axios.post("http://127.0.0.1:5000/upload", formData);
    alert("Uploaded & Processed!");
  };

  const askQuestion = async () => {
    const res = await axios.post("http://127.0.0.1:5000/ask", {
      question,
    });
    setAnswer(res.data.answer);
  };

  const getSummary = async () => {
    const res = await axios.get("http://127.0.0.1:5000/summary");
    setSummary(res.data.summary);
  };

  const getHighlights = async () => {
    const res = await axios.get("http://127.0.0.1:5000/highlights");
    setHighlights(res.data.highlights);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>AI Multi-Agent System</h1>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Upload PDF</button>

      <hr />

      <button onClick={getSummary}>Generate Summary</button>
      <p>{summary}</p>

      <hr />

      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask something..."
      />
      <button onClick={askQuestion}>Ask</button>
      <p>{answer}</p>

      <hr />

      <button onClick={getHighlights}>Get Highlights</button>
      <ul>
        {highlights.map((h, i) => (
          <li key={i}>{h}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;