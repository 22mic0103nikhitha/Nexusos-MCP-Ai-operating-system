import { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    try {
      const res = await axios.post(
        "http://localhost:8000/chat",
        { message }
      );
      setResponse(res.data.response);
    } catch (error) {
      console.error(error);
      setResponse("Error connecting to backend");
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 font-sans">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-4xl font-bold text-center mb-8 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          NexusOS
        </h1>

        <div className="flex space-x-4">
          <input
            className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Ask NexusOS anything..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />

          <button 
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition-colors"
            onClick={sendMessage}
          >
            Send
          </button>
        </div>

        {response && (
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 mt-6 shadow-lg">
            <pre className="whitespace-pre-wrap font-mono text-sm text-gray-300">
              {response}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
