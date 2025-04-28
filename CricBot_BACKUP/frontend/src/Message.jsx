import React from "react";

function Message({ text, sender }) {
  return (
    <div className={`flex ${sender === "user" ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-xs p-3 rounded-lg ${
          sender === "user" ? "bg-blue-500 text-white" : "bg-gray-700 text-white"
        }`}
      >
        {text}
      </div>
    </div>
  );
}

export default Message;