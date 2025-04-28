import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAoAcgjm_GWbrnhzafrJgc-laKhjVET1uM",
  authDomain: "sharatrk07-cricbot.firebaseapp.com",
  projectId: "sharatrk07-cricbot",
  storageBucket: "sharatrk07-cricbot.firebasestorage.app",
  messagingSenderId: "659673592547",
  appId: "1:659673592547:web:88ecf160e357618f62cbd6"
};

const app = initializeApp(firebaseConfig);
console.log("Firebase initialized successfully:", app);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);