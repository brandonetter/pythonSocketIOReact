import logo from "./logo.svg";
import "./App.css";
import { io } from "socket.io-client";
import { useState, useEffect, useRef } from "react";

//Remember transport is set to false to prevent socket from using polling
const socket = io("http://localhost:5000", { transports: ["websocket"] });
function App() {
  const [username, setUsername] = useState("");
  const [messages, setMessages] = useState([]);
  const chatRef = useRef();

  useEffect(() => {
    //Connec and disconnect to events just for debugging
    socket.on("connect", () => {
      console.log("connected");
    });
    socket.on("disconnect", () => {
      console.log("disconnected");
    });

    //Listen to message event and add it to messages array
    socket.on("message", (message) => {
      console.log(message);
      setMessages((messages) => [...messages, message]);
    });

    //Disconnect from events when component unmounts
    return () => {
      socket.off("connect");
      socket.off("disconnect");
      socket.off("message");
    };
  }, []);

  function join() {
    socket.emit("login", { username: username });
  }

  function sendMessage() {
    socket.emit("message", { message: chatRef.current.value });
    chatRef.current.value = "";
  }

  return (
    <div className="App">
      username
      <input type="text" onChange={(e) => setUsername(e.target.value)} />{" "}
      <button onClick={join}>Join</button>
      <br />
      <div className="chat">
        {messages.map((message, index) => {
          return (
            <div key={index}>
              <span>{message?.user}: </span>
              <span>{message?.message}</span>
            </div>
          );
        })}
      </div>
      <br />
      <input type="text" ref={chatRef} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;
