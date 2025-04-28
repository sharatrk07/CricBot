// Login.jsx
"use client"

import React, { useState } from "react"
import { auth } from "./firebase/firebase"
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword
} from "firebase/auth"

function Login({ onLoginSuccess }) {
  const [activeForm, setActiveForm] = useState("login")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")
    setIsLoading(true)

    try {
      if (activeForm === "login") {
        const { user } = await signInWithEmailAndPassword(
          auth,
          username,
          password
        )
        onLoginSuccess(user.email)
      } else {
        if (password !== confirmPassword) {
          setError("Passwords do not match")
          setIsLoading(false)
          return
        }
        const { user } = await createUserWithEmailAndPassword(
          auth,
          username,
          password
        )
        onLoginSuccess(user.email)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-gray-300">
      <header className="flex justify-between items-center p-4 bg-gray-800 shadow-md">
        <div className="flex items-center">
          <div className="w-10 h-10 mr-3 relative">
            <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center">
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                ></path>
              </svg>
            </div>
          </div>
          <h1 className="text-2xl font-bold text-white font-sans tracking-wide">CricBot</h1>
        </div>
      </header>

      <div className="flex-grow flex flex-col items-center justify-center p-4">
        <div className="w-full max-w-md">
          <div className="flex mb-6 rounded-t-lg overflow-hidden shadow-lg">
            <button
              onClick={() => setActiveForm("login")}
              className={`flex-1 py-3 text-center transition-colors flex items-center justify-center ${
                activeForm === "login" ? "bg-gray-700 text-white" : "bg-gray-800 text-gray-400"
              }`}
            >
              <svg
                className="w-5 h-5 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
                ></path>
              </svg>
              Login
            </button>
            <button
              onClick={() => setActiveForm("signup")}
              className={`flex-1 py-3 text-center transition-colors flex items-center justify-center ${
                activeForm === "signup" ? "bg-gray-700 text-white" : "bg-gray-800 text-gray-400"
              }`}
            >
              <svg
                className="w-5 h-5 mr-2"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
                ></path>
              </svg>
              Sign Up
            </button>
          </div>

          <form
            onSubmit={handleSubmit}
            className="bg-gray-800 p-8 rounded-b-lg shadow-lg border border-gray-700"
          >
            {error && (
              <div className="mb-4 p-3 bg-gray-700 border-l-4 border-red-500 text-red-400 rounded">
                <div className="flex items-center">
                  <svg
                    className="w-5 h-5 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    ></path>
                  </svg>
                  {error}
                </div>
              </div>
            )}
            <div className="mb-6">
              <label htmlFor="username" className="block text-sm font-medium mb-2">
                Username
              </label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">👤</span>
                <input
                  type="text"
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full p-3 pl-10 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500 border border-gray-600"
                  required
                />
              </div>
            </div>
            <div className="mb-6">
              <label htmlFor="password" className="block text-sm font-medium mb-2">
                Password
              </label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">🔒</span>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full p-3 pl-10 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500 border border-gray-600"
                  required
                />
              </div>
            </div>
            {activeForm === "signup" && (
              <div className="mb-6">
                <label htmlFor="confirmPassword" className="block text-sm font-medium mb-2">
                  Confirm Password
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">🔒</span>
                  <input
                    type="password"
                    id="confirmPassword"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full p-3 pl-10 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500 border border-gray-600"
                    required
                  />
                </div>
              </div>
            )}
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-3 px-4 ${
                isLoading ? "bg-gray-600" : "bg-gray-700 hover:bg-gray-600"
              } text-white rounded-md transition-colors font-medium shadow-md flex items-center justify-center`}
            >
              {isLoading ? (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Processing...
                </>
              ) : activeForm === "login" ? (
                "Sign In"
              ) : (
                "Sign Up"
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Login


















// WORKING PERFECTLY
// import React, { useState } from "react";
// import { auth } from "./firebase/firebase";
// import {
//   signInWithEmailAndPassword,
//   createUserWithEmailAndPassword
// } from "firebase/auth";

// function Login({ onLoginSuccess }) {
//   const [activeForm, setActiveForm] = useState("login");
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");
//   const [confirmPassword, setConfirmPassword] = useState("");
//   const [error, setError] = useState("");
//   const [loading, setLoading] = useState(false);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setError("");
//     setLoading(true);
//     try {
//       if (activeForm === "login") {
//         const userCredential = await signInWithEmailAndPassword(
//           auth,
//           username,
//           password
//         );
//         onLoginSuccess(userCredential.user);
//       } else {
//         if (password !== confirmPassword) {
//           setError("Passwords do not match");
//           setLoading(false);
//           return;
//         }
//         const userCredential = await createUserWithEmailAndPassword(
//           auth,
//           username,
//           password
//         );
//         onLoginSuccess(userCredential.user);
//       }
//     } catch (err) {
//       setError(err.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="flex flex-col h-screen bg-gray-900 text-gray-300">
//       <header className="flex justify-between items-center p-4 bg-gray-800">
//         <h1 className="text-2xl font-bold">CricBot</h1>
//       </header>

//       <div className="flex-grow flex flex-col items-center justify-center p-4">
//         <div className="w-full max-w-md">
//           <div className="flex mb-6">
//             <button
//               onClick={() => setActiveForm("login")}
//               className={`flex-1 py-2 text-center transition-colors ${
//                 activeForm === "login"
//                   ? "bg-gray-700 text-gray-100"
//                   : "bg-gray-800 text-gray-400"
//               }`}
//             >
//               <span className="inline-block mr-2">➡️</span>
//               Login
//             </button>
//             <button
//               onClick={() => setActiveForm("signup")}
//               className={`flex-1 py-2 text-center transition-colors ${
//                 activeForm === "signup"
//                   ? "bg-gray-700 text-gray-100"
//                   : "bg-gray-800 text-gray-400"
//               }`}
//             >
//               <span className="inline-block mr-2">👤+</span>
//               Sign Up
//             </button>
//           </div>

//           <form onSubmit={handleSubmit} className="bg-gray-800 p-6 rounded-lg">
//             {error && (
//               <p className="mb-4 text-center text-red-500">{error}</p>
//             )}
//             <div className="mb-4">
//               <label
//                 htmlFor="username"
//                 className="block text-sm font-medium mb-2"
//               >
//                 Username
//               </label>
//               <div className="relative">
//                 <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
//                   👤
//                 </span>
//                 <input
//                   type="email"
//                   id="username"
//                   value={username}
//                   onChange={(e) => setUsername(e.target.value)}
//                   className="w-full p-2 pl-10 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-600"
//                   required
//                   disabled={loading}
//                 />
//               </div>
//             </div>
//             <div className="mb-4">
//               <label
//                 htmlFor="password"
//                 className="block text-sm font-medium mb-2"
//               >
//                 Password
//               </label>
//               <div className="relative">
//                 <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
//                   🔒
//                 </span>
//                 <input
//                   type="password"
//                   id="password"
//                   value={password}
//                   onChange={(e) => setPassword(e.target.value)}
//                   className="w-full p-2 pl-10 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-600"
//                   required
//                   disabled={loading}
//                 />
//               </div>
//             </div>
//             {activeForm === "signup" && (
//               <div className="mb-4">
//                 <label
//                   htmlFor="confirmPassword"
//                   className="block text-sm font-medium mb-2"
//                 >
//                   Confirm Password
//                 </label>
//                 <div className="relative">
//                   <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
//                     🔒
//                   </span>
//                   <input
//                     type="password"
//                     id="confirmPassword"
//                     value={confirmPassword}
//                     onChange={(e) => setConfirmPassword(e.target.value)}
//                     className="w-full p-2 pl-10 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-600"
//                     required
//                     disabled={loading}
//                   />
//                 </div>
//               </div>
//             )}
//             <button
//               type="submit"
//               className="w-full py-2 px-4 bg-gray-700 text-gray-100 rounded-md hover:bg-gray-600 transition-colors"
//               disabled={loading}
//             >
//               {activeForm === "login" ? "Sign In" : "Sign Up"}
//             </button>
//           </form>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default Login;
