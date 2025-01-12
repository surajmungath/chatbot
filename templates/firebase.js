import firebase from "firebase/app";
import "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyBmbUvO3TOqMqLHZ6EehRgmKPv-dWOtZtU",
    authDomain: "signlog-1b4ab.firebaseapp.com",
    projectId: "signlog-1b4ab",
    storageBucket: "signlog-1b4ab.firebasestorage.app",
    messagingSenderId: "21919134283",
    appId: "1:21919134283:web:780404d8876972742b53ce",
    measurementId: "G-D80BS0F05P"
  };
// Initialize Firebase
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

export const auth = firebase.auth();
