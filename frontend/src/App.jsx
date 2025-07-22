import React, { useState } from "react";
import axios from "axios";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showPipeline, setShowPipeline] = useState(false);

  const handleAsk = async () => {
    setLoading(true);
    setError(null);
    setResponse(null);
    setShowPipeline(false);
    try {
      const res = await axios.post("http://localhost:8000/ask", {
        question: question,
        intent: "improve_answer"
      }, {
        headers: {
          "Content-Type": "application/json"
        }
      });
      setResponse(res.data);
    } catch (err) {
      setError("Error contacting backend");
    } finally {
      setLoading(false);
    }
  };

  const renderPipeline = () => {
    if (!response?.pipeline_trace || !showPipeline) return null;
    return (
      <div style={{ marginTop: "1rem" }}>
        {response.pipeline_trace.map((step, index) => (
          <div key={index} style={styles.cardDark}>
            <strong>Tool:</strong> {step.tool}<br />
            <strong>Status:</strong> {step.status}<br />
            <strong>Phase:</strong> {step.phase}<br />
            {step.feedback && (
              <>
                <strong>Feedback:</strong>
                <p>{step.feedback}</p>
              </>
            )}
            {step.content && (
              <>
                <strong>Content:</strong>
                <pre style={styles.codeBlock}>
                  {step.content.slice(0, 500)}{step.content.length > 500 ? "..." : ""}
                </pre>
              </>
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div style={styles.page}>
      <div style={styles.overlay}>
        <div style={styles.container}>
          <h1 style={styles.title}>🤖 IntellectMesh</h1>
          <div style={styles.inputRow}>
            <input
              type="text"
              placeholder="Ask your question..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              style={styles.input}
            />
            <button onClick={handleAsk} style={styles.button}>Go</button>
          </div>

          {loading && <p>⏳ Waiting for response...</p>}
          {error && <p style={{ color: "red" }}>{error}</p>}

          {response?.answer && (
            <div style={styles.cardDark}>
              <h2>📌 Final Answer:</h2>
              <pre style={styles.answerText}>{response.answer}</pre>
            </div>
          )}

          {response?.pipeline_trace && (
            <div style={{ marginTop: "1.5rem", width: "100%" }}>
              <button onClick={() => setShowPipeline(!showPipeline)} style={styles.pipelineButton}>
                {showPipeline ? "Hide Pipeline Trace" : "Show Pipeline Trace"}
              </button>
              {renderPipeline()}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    backgroundImage: 'url("/c.jpeg")', // Make sure the image is in public/
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundRepeat: "no-repeat",
    minHeight: "100vh",
    fontFamily: "Segoe UI, sans-serif",
    display: "flex",
    justifyContent: "center",
    alignItems: "center"
  },
  overlay: {
    backgroundColor: "rgba(0,0,0,0.6)",
    width: "100%",
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center"
  },
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "2rem",
    color: "#fff",
    width: "100%",
    maxWidth: "800px"
  },
  title: {
    fontSize: "2.5rem",
    marginBottom: "1rem"
  },
  inputRow: {
    display: "flex",
    width: "100%",
    maxWidth: "700px",
    marginBottom: "1.5rem"
  },
  input: {
    flex: 1,
    padding: "0.75rem",
    fontSize: "1rem",
    borderRadius: "6px 0 0 6px",
    border: "1px solid #ccc"
  },
  button: {
    backgroundColor: "#2563eb",
    color: "white",
    padding: "0.75rem 1.25rem",
    border: "none",
    fontSize: "1rem",
    borderRadius: "0 6px 6px 0",
    cursor: "pointer"
  },
  cardDark: {
    background: "#1e293b",
    color: "white",
    padding: "1rem",
    borderRadius: "10px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.2)",
    width: "100%",
    marginBottom: "1rem"
  },
  codeBlock: {
    backgroundColor: "#334155",
    padding: "0.5rem",
    borderRadius: "6px",
    color: "#e0f2fe",
    marginTop: "0.5rem",
    whiteSpace: "pre-wrap"
  },
  answerText: {
    fontSize: "1rem",
    whiteSpace: "pre-wrap"
  },
  pipelineButton: {
    padding: "0.6rem 1.2rem",
    backgroundColor: "#1d4ed8",
    color: "white",
    border: "none",
    borderRadius: "6px",
    fontSize: "1rem",
    cursor: "pointer",
    marginBottom: "1rem"
  }
};

export default App;
