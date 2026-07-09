import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { sendMessage } from "../store/chatSlice";
import ChatBubble from "./ChatBubble";

function AIChat() {
  const [input, setInput] = useState("");
  const dispatch = useDispatch();
  const { messages, loading } = useSelector((state) => state.chat);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;
    console.log("Sending:", trimmed);
    const result = await dispatch(sendMessage(trimmed));
    console.log("Dispatch Result:", result);
    setInput("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="h-full flex flex-col">
      <div className="bg-blue-600 text-white p-4 rounded-t-xl">
        <h2 className="text-xl font-bold">🤖 AI Assistant</h2>
        <p className="text-sm mt-1">Log interaction details here via chat</p>
      </div>

      <div className="flex-1 p-4 overflow-auto space-y-3">
        {messages.length === 0 && (
          <div className="bg-cyan-100 rounded-lg p-3 text-sm">
            Log interaction details here (e.g., "Met Dr. Smith, discussed
            Product X efficacy, positive sentiment, shared brochure") or ask
            for help.
          </div>
        )}

        {messages.map((msg, idx) => (
          <ChatBubble key={idx} role={msg.role} text={msg.text} />
        ))}

        {loading && (
          <div className="text-sm text-gray-500 italic">AI is thinking...</div>
        )}
      </div>

      <div className="border-t p-4 flex gap-3">
        <input
          className="flex-1 border rounded-lg p-3"
          placeholder="Describe Interaction..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          className="bg-blue-600 text-white px-6 rounded-lg disabled:opacity-50"
          onClick={handleSend}
          disabled={loading}
        >
          {loading ? "..." : "Log"}
        </button>
      </div>
    </div>
  );
}

export default AIChat;