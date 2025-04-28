"use client"

import { useState, useEffect } from "react"

function TypingIndicator() {
  const [dots, setDots] = useState(1)

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => (prev < 3 ? prev + 1 : 1))
    }, 500)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="flex items-center">
      <div className="flex space-x-1">
        <div className={`w-2 h-2 rounded-full bg-gray-400 animate-bounce`} style={{ animationDelay: "0ms" }}></div>
        <div className={`w-2 h-2 rounded-full bg-gray-400 animate-bounce`} style={{ animationDelay: "150ms" }}></div>
        <div className={`w-2 h-2 rounded-full bg-gray-400 animate-bounce`} style={{ animationDelay: "300ms" }}></div>
      </div>
    </div>
  )
}

export default TypingIndicator