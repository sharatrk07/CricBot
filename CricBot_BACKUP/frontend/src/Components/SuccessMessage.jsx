const SuccessMessage = ({ message }) => {
  if (!message) return null

  return (
    <div className="bg-gray-800 text-green-400 p-3 text-center shadow-lg animate-fadeIn">
      <div className="flex items-center justify-center">
        <svg
          className="w-6 h-6 mr-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
        </svg>
        <span className="font-semibold text-lg">{message}</span>
      </div>
    </div>
  )
}

export default SuccessMessage
