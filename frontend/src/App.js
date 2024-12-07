import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [responses, setResponses] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const res = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    setResponses([...responses, { user: message, bot: data.response }]);
    setMessage('');
  };

  return (
    <div className="App">
      <h1>Chat with Bot</h1>
      <div>
        {responses.map((resp, idx) => (
          <div key={idx}>
            <strong>You:</strong> {resp.user}
            <br />
            <strong>Bot:</strong> {resp.bot}
            <hr />
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask something..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default App;
