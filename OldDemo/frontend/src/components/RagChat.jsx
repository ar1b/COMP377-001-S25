// src/components/RagChat.jsx
import { useState } from "react";
import { Container, Form, Button, Card, Spinner, Alert } from "react-bootstrap";

function RagChat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askQuestion = async (e) => {
    e.preventDefault();
    setLoading(true);
    setAnswer(null);
    setSources([]);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      if (response.ok) {
        setAnswer(data.answer.trim());
        setSources(data.sources);
      } else {
        setError(data.error || "Something went wrong.");
      }
    } catch (err) {
      setError("Could not connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="my-4" style={{ maxWidth: "700px" }}>
      <h2 className="mb-4">Want to talk about it?</h2>
      <Form onSubmit={askQuestion}>
        <Form.Group className="mb-3">
          <Form.Label>Your Question</Form.Label>
          <Form.Control
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., Why am I so sad?"
            required
          />
        </Form.Group>
        <div className="button-container">
        <Button type="submit" disabled={loading}>
          {loading ? <Spinner animation="border" size="sm" /> : "Ask"}
        </Button>
        </div>
      </Form>

      {error && <Alert variant="danger" className="mt-3">{error}</Alert>}

      {answer && (
        <Card className="mt-4">
          <Card.Body>
            <Card.Title>Answer</Card.Title>
            <Card.Text>{answer}</Card.Text>
          </Card.Body>
        </Card>
      )}
    </Container>
  );
}

export default RagChat;
