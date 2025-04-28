// // App.jsx for Bakend
// import React, { useState, useEffect, useRef } from "react";
// import Login from "./Login";
// import axios from "axios";
// import Table from "./Table";

// function App() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [isLoggedIn, setIsLoggedIn] = useState(false);
//   const [showLoginSuccess, setShowLoginSuccess] = useState(false);

//   const inputRef = useRef(null);

//   const getData = async (prompt) => {
//     if (!input.trim()) return;
//     setMessages((prev) => [...prev, { content: input, sender: "user" }]);
//     // NETWORK ADDRESS NEEDS TO CHANGE HERE
//       let body = {
//         "sender": "user123",
//         "message": prompt,
//       }

//       console.log('hello');

//       const res1 = await axios.post('http://localhost:5005/webhooks/rest/webhook',body);
//       console.log(res1.data)
//       if(res1.data[0].text==="Sorry, I didn't get that. Can you please rephrase your question"){
//         try{
//           const res = await axios.post("http://192.168.148.31:8080/getAns", { 'prompt':prompt });
//           setMessages((prev) => [...prev, { content: res.data.data, sender: "bot",isTable:true }]);
//         }catch(e){
//               setMessages((prev) => [...prev, { content: "Sorry, I didn't get the answer for that. Can you please rephrase your question", sender: "bot",isTable:false }]);
//         }
//       }else{
//         setMessages((prev)=>[...prev,{content:res1.data[0].text,sender:'bot',isTable:false}]);
//       }
//     }

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





















// // // if(data.text=="Sorry, I didn't get that. Can you please rephrase your question")


// // // App.jsx
// // import React, { useState, useEffect, useRef } from "react";
// // import io from "socket.io-client";
// // import Login from "./Login";
// // import axios from "axios";
// // import Table from "./Table";

// // function App() {
// //   const [messages, setMessages] = useState([]);
// //   const [input, setInput] = useState("");
// //   const [isLoggedIn, setIsLoggedIn] = useState(false);
// //   const [showLoginSuccess, setShowLoginSuccess] = useState(false);
// //   const socket = useRef(null);
// //   const inputRef = useRef(null);

// //   useEffect(() => {
// //     socket.current = io("http://localhost:5005", {
// //       path: "/socket.io/",
// //       transports: ["websocket"],
// //     });
// //     socket.current.on("connect", () =>
// //       socket.current.emit("session_request", { session_id: "user123" })
// //     );
// //     return () => socket.current.disconnect();
// //   }, []);

// //   const getData = async (prompt) => {
// //     // NETWORK ADDRESS NEEDS TO CHANGE HERE
// //     const res = await axios.post("http://192.168.148.31:8080/getAns", { prompt });
// //     setMessages((prev) => [...prev, { content: res.data.data, sender: "bot" }]);
// //   };

// //   const handleSend = () => {
// //     if (!input.trim()) return;
// //     setMessages((prev) => [...prev, { content: input, sender: "user" }]);
// //     socket.current.emit("user_uttered", {
// //       message: input,
// //       session_id: "user123",
// //     });
// //     getData(input);
// //     setInput("");
// //   };

// //   const onLoginSuccess = () => {
// //     setIsLoggedIn(true);
// //     setShowLoginSuccess(true);
// //     setTimeout(() => setShowLoginSuccess(false), 3000);
// //   };

// //   if (!isLoggedIn) return <Login onLoginSuccess={onLoginSuccess} />;

// //   return (
// //     <div className="flex flex-col h-screen bg-gray-900">
// //       {showLoginSuccess && (
// //         <div className="bg-green-500 text-white p-2 text-center">
// //           Login Successful!
// //         </div>
// //       )}
// //       <header className="flex justify-between items-center p-4 bg-gray-800">
// //         <h1 className="text-2xl font-bold text-white">CricBot</h1>
// //         <button onClick={() => setIsLoggedIn(false)} className="text-white">
// //           Logout
// //         </button>
// //       </header>
// //       <main className="flex-1 overflow-y-auto p-4 space-y-4">
// //         {messages.map((msg, idx) => {
// //           if (msg.sender === "user") {
// //             return (
// //               <div key={idx} className="flex justify-end mb-2">
// //                 <div className="bg-blue-600 text-white p-3 rounded-lg">
// //                   {msg.content}
// //                 </div>
// //               </div>
// //             );
// //           } else if (Array.isArray(msg.content)) {
// //             const total = msg.content.length;
// //             return (
// //               <div key={idx} className="flex flex-col space-y-4">
// //                 {msg.content.map((item, i) => (
// //                   <Table
// //                     key={i}
// //                     data={item.row}
// //                     filtersData={item.filters}
// //                     index={i}
// //                     total={total}
// //                   />
// //                 ))}
// //               </div>
// //             );
// //           } else {
// //             return (
// //               <div key={idx} className="flex justify-start mb-2">
// //                 <div className="bg-gray-700 text-white p-3 rounded-lg">
// //                   {msg.content}
// //                 </div>
// //               </div>
// //             );
// //           }
// //         })}
// //       </main>
// //       <footer className="p-4 bg-gray-800">
// //         <div className="flex items-center gap-2">
// //           <input
// //             ref={inputRef}
// //             type="text"
// //             className="flex-1 p-3 rounded-lg bg-gray-700 text-white focus:outline-none"
// //             placeholder="Type your message..."
// //             value={input}
// //             onChange={(e) => setInput(e.target.value)}
// //             onKeyDown={(e) => e.key === "Enter" && handleSend()}
// //           />
// //           <button
// //             onClick={handleSend}
// //             className="p-3 bg-gray-700 text-gray-400 rounded-lg hover:text-gray-200"
// //           >
// //             ➤
// //           </button>
// //         </div>
// //       </footer>
// //     </div>
// //   );
// // }

// // export default App;