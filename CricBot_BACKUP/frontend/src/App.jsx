"use client"

import { useState, useEffect, useRef } from "react"
import Login from "./Login"
import axios from "axios"
import Table from "./Components/Table"
import TypingIndicator from "./Components/TypingIndicator"

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [isDropdownOpen, setIsDropdownOpen] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [showLoginSuccess, setShowLoginSuccess] = useState(false)
  const [username, setUsername] = useState("")
  const [showScrollButton, setShowScrollButton] = useState(false)
  const [showGreeting, setShowGreeting] = useState(true)
  const [isTyping, setIsTyping] = useState(false)
  const inputRef = useRef(null)
  const messagesEndRef = useRef(null)
  const messagesContainerRef = useRef(null)
  const abortControllerRef = useRef(null)

  useEffect(() => {
    if (inputRef.current) inputRef.current.focus()
  }, [])

  useEffect(() => {
    const handleScroll = () => {
      if (messagesContainerRef.current) {
        const { scrollTop, scrollHeight, clientHeight } = messagesContainerRef.current
        const isAtBottom = scrollHeight - scrollTop - clientHeight < 100
        setShowScrollButton(!isAtBottom)
      }
    }

    const container = messagesContainerRef.current
    if (container) {
      container.addEventListener("scroll", handleScroll)
      return () => container.removeEventListener("scroll", handleScroll)
    }
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Cleanup function for ongoing requests when component unmounts
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
    }
  }, [])

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({
        behavior: "smooth",
        block: "end",
      })
      // Hide scroll button after scrolling
      setTimeout(() => setShowScrollButton(false), 500)
    }
  }

  const getData = async (prompt) => {
    if (!prompt.trim()) return;
  
    // Cancel any ongoing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
    
    // Create a new AbortController for this request
    abortControllerRef.current = new AbortController()
    const signal = abortControllerRef.current.signal
    
    setMessages((prev) => [...prev, { content: prompt, sender: "user" }]);
    setIsTyping(true);
    setShowGreeting(false);
  
    const body = {
      sender: "user123",
      message: prompt,
    };
    
    // Create a timeout that aborts the request after 10 seconds
    const timeoutId = setTimeout(() => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
        setIsTyping(false)
        setMessages((prev) => [...prev, {
          content: "Sorry, we were unable to retrieve a response. Please try again.",
          sender: "bot", 
          isTable: false
        }])
        scrollToBottom()
      }
    }, 30000)
  
    try {
      // First API call with timeout
      const res1 = await axios.post(
        "http://localhost:5005/webhooks/rest/webhook", 
        body, 
        { signal }
      );
      
      const rasaText = res1?.data?.[0]?.text;
  
      if (!rasaText || rasaText === "Sorry, I didn't get that. Can you please rephrase your question") {
        try {
          // Second API call if first fails
          const res = await axios.post(
            "http://192.168.148.31:8080/getAns", 
            { prompt }, 
            { signal }
          );
          
          clearTimeout(timeoutId);
          setMessages((prev) => [...prev, { content: res.data.data, sender: "bot", isTable: true }]);
        } catch (e) {
          // Only handle this error if it's not an abort error
          if (!axios.isCancel(e)) {
            clearTimeout(timeoutId);
            setMessages((prev) => [...prev, {
              content: "Sorry, I didn't get the answer for that. Can you please rephrase your question",
              sender: "bot", isTable: false
            }]);
          }
        }
      } else {
        clearTimeout(timeoutId);
        setMessages((prev) => [...prev, { content: rasaText, sender: "bot", isTable: false }]);
      }
    } catch (error) {
      // Only handle this error if it's not an abort error
      if (!axios.isCancel(error)) {
        clearTimeout(timeoutId);
        console.error("Error fetching data:", error);
        setMessages((prev) => [...prev, {
          content: "Sorry, I couldn't get a response. Please try again.",
          sender: "bot", isTable: false
        }]);
      }
    } finally {
      if (!signal.aborted) {
        clearTimeout(timeoutId);
        setIsTyping(false);
        setTimeout(scrollToBottom, 100);
      }
    }
  };  

  const handleSend = () => {
    if (input.trim()) {
      getData(input);
      setInput("");
    }
  }

  const handleLogout = () => {
    // Cancel any ongoing request when logging out
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
    
    setIsLoggedIn(false)
    setShowLoginSuccess(false)
    setUsername("")
    setMessages([])
    setShowGreeting(true)
    setIsTyping(false)
  }

  const onLoginSuccess = (user) => {
    setIsLoggedIn(true)
    setShowLoginSuccess(true)
    setUsername(user)
    setTimeout(() => setShowLoginSuccess(false), 3000)
  }

  if (!isLoggedIn) {
    return <Login onLoginSuccess={onLoginSuccess} />
  }

  return (
    <div className="flex flex-col h-screen bg-gray-900">
      {showLoginSuccess && (
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
            <span className="font-semibold text-lg">Welcome back, {username}!</span>
          </div>
        </div>
      )}

      <header className="flex justify-between items-center p-4 bg-gray-800 shadow-md">
        <div className="flex items-center">
          <div className="w-10 h-10 mr-3 relative">
            <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center">
              {/* Message Circle Icon */}
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
              </svg>
            </div>
          </div>
          <h1 className="text-2xl font-bold text-white font-sans tracking-wide">CricBot</h1>
        </div>
        <div className="relative group">
          <button
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center hover:bg-gray-600 transition-colors text-white shadow-md"
          >
            👤
          </button>
          <div className={`absolute right-0 mt-2 w-40 bg-gray-800 rounded-md shadow-lg py-1 z-10 border border-gray-700 ${isDropdownOpen ? 'opacity-100 visible' : 'opacity-0 invisible'} transition-all duration-300`}>
            <div className="px-4 py-2 text-sm text-gray-300 border-b border-gray-700">{username}</div>
            <button
              onClick={handleLogout}
              className="flex items-center w-full px-4 py-2 text-sm text-gray-300 hover:bg-gray-700 transition-colors"
            >
              <span className="mr-2">⬅</span>
              Logout
            </button>
          </div>
        </div>
      </header>

      {showGreeting && (
        <div className="flex-1 flex flex-col items-center justify-center p-4 bg-gradient-to-b from-gray-900 to-gray-800">
          <div className="text-center mb-6 bg-gray-800 p-8 rounded-xl shadow-2xl border border-gray-700 max-w-lg">
            <div className="flex justify-center mb-6">
              <div className="w-24 h-24 rounded-full bg-gray-700 flex items-center justify-center">
                {/* Message Circle Icon */}
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
                  <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
                </svg>
              </div>
            </div>
            <h2 className="text-4xl font-bold text-white mb-4 font-sans tracking-wide">Hello, {username}</h2>
            <h3 className="text-xl text-gray-300 whitespace-nowrap overflow-hidden text-ellipsis">
              I am ready to assist you with IPL related queries!
            </h3>
          </div>
        </div>
      )}

      {!showGreeting && (
        <main className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900" ref={messagesContainerRef}>
          {messages.map((msg, idx) => {
            if (msg.sender === "user") {
              return (
                <div key={idx} className="flex justify-end mb-4">
                  <div className="bg-gray-700 text-white p-3 rounded-lg max-w-[75%] md:max-w-[60%] shadow-md">
                    {msg.content}
                  </div>
                  <div className="w-8 h-8 ml-2 rounded-full bg-gray-700 flex items-center justify-center shadow-sm">
                    {/* User Icon */}
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </div>
                </div>
              )
            } else if (msg.isTable && Array.isArray(msg.content)) {
              const total = msg.content.length
              return (
                <div key={idx} className="flex flex-col space-y-4">
                  <div className="flex items-start">
                    <div className="w-8 h-8 mr-2 relative">
                      <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
                        {/* Message Circle Icon */}
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
                          <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
                        </svg>
                      </div>
                    </div>
                    <div className="flex flex-col space-y-4 max-w-[75%] md:max-w-[60%]">
                      {msg.content.map((item, i) => (
                        <Table key={i} data={item.row} filtersData={item.filters} index={i} total={total} />
                      ))}
                    </div>
                  </div>
                </div>
              )
            } else {
              return (
                <div key={idx} className="flex justify-start mb-4">
                  <div className="w-8 h-8 mr-2 relative">
                    <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
                      {/* Message Circle Icon */}
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
                        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
                      </svg>
                    </div>
                  </div>
                  <div className="bg-gray-700 text-white p-3 rounded-lg max-w-[75%] md:max-w-[60%] shadow-md">
                    {msg.content}
                  </div>
                </div>
              )
            }
          })}

          {isTyping && (
            <div className="flex justify-start mb-2">
              <div className="w-8 h-8 mr-2 relative">
                <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
                  {/* Message Circle Icon */}
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
                    <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
                  </svg>
                </div>
              </div>
              <div className="bg-gray-700 text-white p-3 rounded-lg shadow-md">
                <TypingIndicator />
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </main>
      )}

      {showScrollButton && !showGreeting && (
        <div className="fixed bottom-24 left-1/2 transform -translate-x-1/2 z-10">
          <button
            className="p-3 rounded-full bg-gray-700 text-white shadow-lg hover:bg-gray-600 transition-colors flex items-center justify-center"
            onClick={scrollToBottom}
            aria-label="Scroll to bottom"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 16L6 10H18L12 16Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
      )}

      <footer className="p-4 md:p-6 bg-gray-800 shadow-inner">
        <div className="flex items-center gap-3 bg-gray-700 rounded-xl p-2 shadow-inner">
          <input
            type="text"
            className="flex-1 p-2 md:p-3 bg-transparent text-white placeholder-gray-400 focus:outline-none"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if(e.key === "Enter"){
                handleSend();
              } 
            }}
            ref={inputRef}
            disabled={isTyping}
          />
          <button
            onClick={handleSend}
            className={`p-2 md:p-3 rounded-full ${isTyping ? 'bg-gray-500 cursor-not-allowed' : 'bg-gray-600 hover:bg-gray-500'} text-white transition-colors shadow-md`}
            disabled={isTyping}
          >
            {/* Send Icon */}
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </footer>
    </div>
  )
}

export default App













// "use client"

// import { useState, useEffect, useRef } from "react"
// import Login from "./Login"
// import axios from "axios"
// import Table from "./Components/Table"
// import TypingIndicator from "./Components/TypingIndicator"

// function App() {
//   const [messages, setMessages] = useState([])
//   const [input, setInput] = useState("")
//   const [isDropdownOpen, setIsDropdownOpen] = useState(false)
//   const [isLoggedIn, setIsLoggedIn] = useState(false)
//   const [showLoginSuccess, setShowLoginSuccess] = useState(false)
//   const [username, setUsername] = useState("")
//   const [showScrollButton, setShowScrollButton] = useState(false)
//   const [showGreeting, setShowGreeting] = useState(true)
//   const [isTyping, setIsTyping] = useState(false)
//   const inputRef = useRef(null)
//   const messagesEndRef = useRef(null)
//   const messagesContainerRef = useRef(null)

//   useEffect(() => {
//     if (inputRef.current) inputRef.current.focus()
//   }, [])

//   useEffect(() => {
//     const handleScroll = () => {
//       if (messagesContainerRef.current) {
//         const { scrollTop, scrollHeight, clientHeight } = messagesContainerRef.current
//         const isAtBottom = scrollHeight - scrollTop - clientHeight < 100
//         setShowScrollButton(!isAtBottom)
//       }
//     }

//     const container = messagesContainerRef.current
//     if (container) {
//       container.addEventListener("scroll", handleScroll)
//       return () => container.removeEventListener("scroll", handleScroll)
//     }
//   }, [])

//   useEffect(() => {
//     scrollToBottom()
//   }, [messages])

//   const scrollToBottom = () => {
//     if (messagesEndRef.current) {
//       messagesEndRef.current.scrollIntoView({
//         behavior: "smooth",
//         block: "end",
//       })
//       // Hide scroll button after scrolling
//       setTimeout(() => setShowScrollButton(false), 500)
//     }
//   }

//   const getData = async (prompt) => {
//     if (!prompt.trim()) return;
  
//     setMessages((prev) => [...prev, { content: prompt, sender: "user" }]);
//     setIsTyping(true);
//     setShowGreeting(false);
  
//     const body = {
//       sender: "user123",
//       message: prompt,
//     };
  
//     try {
//       const res1 = await axios.post("http://localhost:5005/webhooks/rest/webhook", body);
//       const rasaText = res1?.data?.[0]?.text;
  
//       if (!rasaText || rasaText === "Sorry, I didn't get that. Can you please rephrase your question") {
//         try {
//           const res = await axios.post("http://192.168.148.31:8080/getAns", { prompt });
//           setMessages((prev) => [...prev, { content: res.data.data, sender: "bot", isTable: true }]);
//         } catch (e) {
//           setMessages((prev) => [...prev, {
//             content: "Sorry, I didn't get the answer for that. Can you please rephrase your question",
//             sender: "bot", isTable: false
//           }]);
//         }
//       } else {
//         setMessages((prev) => [...prev, { content: rasaText, sender: "bot", isTable: false }]);
//       }
//     } catch (error) {
//       console.error("Error fetching data:", error);
//       setMessages((prev) => [...prev, {
//         content: "Sorry, I couldn't get a response. Please try again.",
//         sender: "bot", isTable: false
//       }]);
//     }
  
//     setIsTyping(false);
//     setTimeout(scrollToBottom, 100);
//   };  

//   const handleSend = () => {
//     if (input.trim()) {
//       getData(input);
//     }
//   }

//   const handleLogout = () => {
//     setIsLoggedIn(false)
//     setShowLoginSuccess(false)
//     setUsername("")
//     setMessages([])
//     setShowGreeting(true)
//   }

//   const onLoginSuccess = (user) => {
//     setIsLoggedIn(true)
//     setShowLoginSuccess(true)
//     setUsername(user)
//     setTimeout(() => setShowLoginSuccess(false), 3000)
//   }

//   if (!isLoggedIn) {
//     return <Login onLoginSuccess={onLoginSuccess} />
//   }

//   return (
//     <div className="flex flex-col h-screen bg-gray-900">
//       {showLoginSuccess && (
//         <div className="bg-gray-800 text-green-400 p-3 text-center shadow-lg animate-fadeIn">
//           <div className="flex items-center justify-center">
//             <svg
//               className="w-6 h-6 mr-2"
//               fill="none"
//               stroke="currentColor"
//               viewBox="0 0 24 24"
//               xmlns="http://www.w3.org/2000/svg"
//             >
//               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
//             </svg>
//             <span className="font-semibold text-lg">Welcome back, {username}!</span>
//           </div>
//         </div>
//       )}

//       <header className="flex justify-between items-center p-4 bg-gray-800 shadow-md">
//         <div className="flex items-center">
//           <div className="w-10 h-10 mr-3 relative">
//             <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center">
//               {/* Message Circle Icon */}
//               <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
//                 <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
//               </svg>
//             </div>
//           </div>
//           <h1 className="text-2xl font-bold text-white font-sans tracking-wide">CricBot</h1>
//         </div>
//         <div className="relative group">
//           <button
//             onClick={() => setIsDropdownOpen(!isDropdownOpen)}
//             className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center hover:bg-gray-600 transition-colors text-white shadow-md"
//           >
//             👤
//           </button>
//           <div className={`absolute right-0 mt-2 w-40 bg-gray-800 rounded-md shadow-lg py-1 z-10 border border-gray-700 ${isDropdownOpen ? 'opacity-100 visible' : 'opacity-0 invisible'} transition-all duration-300`}>
//             <div className="px-4 py-2 text-sm text-gray-300 border-b border-gray-700">{username}</div>
//             <button
//               onClick={handleLogout}
//               className="flex items-center w-full px-4 py-2 text-sm text-gray-300 hover:bg-gray-700 transition-colors"
//             >
//               <span className="mr-2">⬅</span>
//               Logout
//             </button>
//           </div>
//         </div>
//       </header>

//       {showGreeting && (
//         <div className="flex-1 flex flex-col items-center justify-center p-4 bg-gradient-to-b from-gray-900 to-gray-800">
//           <div className="text-center mb-6 bg-gray-800 p-8 rounded-xl shadow-2xl border border-gray-700 max-w-lg">
//             <div className="flex justify-center mb-6">
//               <div className="w-24 h-24 rounded-full bg-gray-700 flex items-center justify-center">
//                 {/* Message Circle Icon */}
//                 <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
//                   <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
//                 </svg>
//               </div>
//             </div>
//             <h2 className="text-4xl font-bold text-white mb-4 font-sans tracking-wide">Hello, {username}</h2>
//             <h3 className="text-xl text-gray-300 whitespace-nowrap overflow-hidden text-ellipsis">
//               I am ready to assist you with IPL related queries!
//             </h3>
//           </div>
//         </div>
//       )}

//       {!showGreeting && (
//         <main className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900" ref={messagesContainerRef}>
//           {messages.map((msg, idx) => {
//             if (msg.sender === "user") {
//               return (
//                 <div key={idx} className="flex justify-end mb-4">
//                   <div className="bg-gray-700 text-white p-3 rounded-lg max-w-[75%] md:max-w-[60%] shadow-md">
//                     {msg.content}
//                   </div>
//                   <div className="w-8 h-8 ml-2 rounded-full bg-gray-700 flex items-center justify-center shadow-sm">
//                     {/* User Icon */}
//                     <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
//                       <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
//                       <circle cx="12" cy="7" r="4"></circle>
//                     </svg>
//                   </div>
//                 </div>
//               )
//             } else if (msg.isTable && Array.isArray(msg.content)) {
//               const total = msg.content.length
//               return (
//                 <div key={idx} className="flex flex-col space-y-4">
//                   <div className="flex items-start">
//                     <div className="w-8 h-8 mr-2 relative">
//                       <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
//                         {/* Message Circle Icon */}
//                         <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
//                           <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
//                         </svg>
//                       </div>
//                     </div>
//                     <div className="flex flex-col space-y-4 max-w-[75%] md:max-w-[60%]">
//                       {msg.content.map((item, i) => (
//                         <Table key={i} data={item.row} filtersData={item.filters} index={i} total={total} />
//                       ))}
//                     </div>
//                   </div>
//                 </div>
//               )
//             } else {
//               return (
//                 <div key={idx} className="flex justify-start mb-4">
//                   <div className="w-8 h-8 mr-2 relative">
//                     <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
//                       {/* Message Circle Icon */}
//                       <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
//                         <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
//                       </svg>
//                     </div>
//                   </div>
//                   <div className="bg-gray-700 text-white p-3 rounded-lg max-w-[75%] md:max-w-[60%] shadow-md">
//                     {msg.content}
//                   </div>
//                 </div>
//               )
//             }
//           })}

//           {isTyping && (
//             <div className="flex justify-start mb-2">
//               <div className="w-8 h-8 mr-2 relative">
//                 <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
//                   {/* Message Circle Icon */}
//                   <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
//                     <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
//                   </svg>
//                 </div>
//               </div>
//               <div className="bg-gray-700 text-white p-3 rounded-lg shadow-md">
//                 <TypingIndicator />
//               </div>
//             </div>
//           )}

//           <div ref={messagesEndRef} />
//         </main>
//       )}

//       {showScrollButton && !showGreeting && (
//         <div className="fixed bottom-24 left-1/2 transform -translate-x-1/2 z-10">
//           <button
//             className="p-3 rounded-full bg-gray-700 text-white shadow-lg hover:bg-gray-600 transition-colors flex items-center justify-center"
//             onClick={scrollToBottom}
//             aria-label="Scroll to bottom"
//           >
//             <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
//               <path d="M12 16L6 10H18L12 16Z" fill="currentColor"/>
//             </svg>
//           </button>
//         </div>
//       )}

//       <footer className="p-4 md:p-6 bg-gray-800 shadow-inner">
//         <div className="flex items-center gap-3 bg-gray-700 rounded-xl p-2 shadow-inner">
//           <input
//             type="text"
//             className="flex-1 p-2 md:p-3 bg-transparent text-white placeholder-gray-400 focus:outline-none"
//             placeholder="Type your message..."
//             value={input}
//             onChange={(e) => setInput(e.target.value)}
//             onKeyDown={(e) => {
//               if(e.key === "Enter"){
//                 handleSend(input);
//                 setInput('');
//               } 
//             }}
//             ref={inputRef}
//           />
//           <button
//             onClick={()=>{
//               handleSend(input);
//               setInput('');
//             }}
//             className="p-2 md:p-3 rounded-full bg-gray-600 text-white hover:bg-gray-500 transition-colors shadow-md"
//           >
//             {/* Send Icon */}
//             <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white">
//               <line x1="22" y1="2" x2="11" y2="13"></line>
//               <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
//             </svg>
//           </button>
//         </div>
//       </footer>
//     </div>
//   )
// }

// export default App















// WORKING PERFECTLY

// if(data.text=="Sorry, I didn't get that. Can you please rephrase your question")
// App.jsx for Bakend
// import React, { useState, useEffect, useRef } from "react";
// import Login from "./Login";
// import axios from "axios";
// import Table from './Components/Table'
// import TypingIndicator from './Components/TypingIndicator'

// function App() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [isLoggedIn, setIsLoggedIn] = useState(false);
//   const [showLoginSuccess, setShowLoginSuccess] = useState(false);

//   const inputRef = useRef(null);

//   // const getData = async (prompt) => {
//   //   if (!input.trim()) return;
//   //   setMessages((prev) => [...prev, { content: input, sender: "user" }]);
//   //   // NETWORK ADDRESS NEEDS TO CHANGE HERE
//   //     let body = {
//   //       "sender": "user123",
//   //       "message": prompt,
//   //     }

//   //     console.log('hello');

//   //     const res1 = await axios.post('http://localhost:5005/webhooks/rest/webhook',body);
//   //     console.log(res1.data)
//   //     if(res1.data[0].text==="Sorry, I didn't get that. Can you please rephrase your question"){
//   //       try{
//   //         const res = await axios.post("http://192.168.148.31:8080/getAns", { 'prompt':prompt });
//   //         setMessages((prev) => [...prev, { content: res.data.data, sender: "bot",isTable:true }]);
//   //       }catch(e){
//   //             setMessages((prev) => [...prev, { content: "Sorry, I didn't get the answer for that. Can you please rephrase your question", sender: "bot",isTable:false }]);
//   //       }
//   //     }else{
//   //       setMessages((prev)=>[...prev,{content:res1.data[0].text,sender:'bot',isTable:false}]);
//   //     }
//   //   }


//   const getData = async (prompt) => {
//     if (!input.trim()) return;
  
//     setMessages((prev) => [...prev, { content: input, sender: "user" }]);
  
//     const body = {
//       sender: "user123",
//       message: prompt,
//     };
  
//     try {
//       console.log("Sending to Rasa...");
//       const res1 = await axios.post("http://localhost:5005/webhooks/rest/webhook", body);
//       console.log("Rasa Response:", res1.data);
  
//       const rasaReply = Array.isArray(res1.data) && res1.data.length > 0 && res1.data[0]?.text;
  
//       if (rasaReply && res1.data[0].text !== "Sorry, I didn't get that. Can you please rephrase your question") {
//         setMessages((prev) => [
//           ...prev,
//           { content: res1.data[0].text, sender: "bot", isTable: false },
//         ]);
//       } else {
//         console.log("Fallback to 8080 server...");
//         try {
//           const res = await axios.post("http://192.168.148.31:8080/getAns", { prompt });
//           setMessages((prev) => [
//             ...prev,
//             { content: res.data.data, sender: "bot", isTable: true },
//           ]);
//         } catch (e) {
//           console.error("Fallback API error:", e);
//           setMessages((prev) => [
//             ...prev,
//             {
//               content:
//                 "Sorry, I didn't get the answer for that. Can you please rephrase your question",
//               sender: "bot",
//               isTable: false,
//             },
//           ]);
//         }
//       }
//     } catch (error) {
//       console.error("Rasa API error:", error);
//       setMessages((prev) => [
//         ...prev,
//         {
//           content: "Sorry! There was an error talking to the assistant.",
//           sender: "bot",
//           isTable: false,
//         },
//       ]);
//     }
//   };
  

//   const onLoginSuccess = () => {
//     setIsLoggedIn(true);
//     setShowLoginSuccess(true);
//     setTimeout(() => setShowLoginSuccess(false), 3000);
//   };

//   if (!isLoggedIn) return <Login onLoginSuccess={onLoginSuccess} />;

//   return (
//     <div className="flex flex-col h-screen bg-gray-900">
//       {showLoginSuccess && (
//         <div className="bg-green-500 text-white p-2 text-center">
//           Login Successful!
//         </div>
//       )}
//       <header className="flex justify-between items-center p-4 bg-gray-800">
//         <h1 className="text-2xl font-bold text-white">CricBot</h1>
//         <button onClick={() => setIsLoggedIn(false)} className="text-white">
//           Logout
//         </button>
//       </header>
//       <main className="flex-1 overflow-y-auto p-4 space-y-4">
//         {messages.map((msg, idx) => {
//           if (msg.sender === "user") {
//             return (
//               <div key={idx} className="flex justify-end mb-2">
//                 <div className="bg-blue-600 text-white p-3 rounded-lg">
//                   {msg.content}
//                 </div>
//               </div>
//             );
//           } else if (Array.isArray(msg.content) && msg.isTable) {
//             const total = msg.content.length;
//             return (
//               <div key={idx} className="flex flex-col space-y-4">
//                 {msg.content.map((item, i) => (
//                   <Table
//                     key={i}
//                     data={item.row}
//                     filtersData={item.filters}
//                     index={i}
//                     total={total}
//                   />
//                 ))}
//               </div>
//             );
//           } else {
//             return (
//               <div key={idx} className="flex justify-start mb-2">
//                 <div className="bg-gray-700 text-white p-3 rounded-lg">
//                   {msg.content}
//                 </div>
//               </div>
//             );
//           }
//         })}
//       </main>
//       <footer className="p-4 bg-gray-800">
//         <div className="flex items-center gap-2">
//           <input
//             ref={inputRef}
//             type="text"
//             className="flex-1 p-3 rounded-lg bg-gray-700 text-white focus:outline-none"
//             placeholder="Type your message..."
//             value={input}
//             onChange={(e) => setInput(e.target.value)}
//             onKeyDown={(e) =>{
//             if(e.key === "Enter"){
//               getData(input)
//               setInput('');
//             }
//             }}
//           />
//           <button
//             onClick={()=>{getData(input);setInput('')}}
//             className="p-3 bg-gray-700 text-gray-400 rounded-lg hover:text-gray-200"
//           >
//             ➤
//           </button>
//         </div>
//       </footer>
//     </div>
//   );
// }

// export default App;