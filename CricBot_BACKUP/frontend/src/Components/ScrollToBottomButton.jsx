"use client"

import { ChevronDown } from "lucide-react"

const ScrollToBottomButton = ({ onClick, visible }) => {
  if (!visible) return null

  return (
    <div className="fixed bottom-24 right-6 z-10">
      <button
        className="p-3 rounded-full bg-gray-700 text-white shadow-lg hover:bg-gray-600 transition-colors flex items-center justify-center"
        onClick={onClick}
        aria-label="Scroll to bottom"
      >
        <ChevronDown className="w-5 h-5" />
      </button>
    </div>
  )
}

export default ScrollToBottomButton
