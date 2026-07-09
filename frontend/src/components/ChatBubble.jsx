function ChatBubble({ role, text }) {
  const isUser = role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`rounded-lg p-3 max-w-[85%] text-sm ${
          isUser ? "bg-gray-200" : "bg-green-100"
        }`}
      >
        {text}
      </div>
    </div>
  );
}

export default ChatBubble;