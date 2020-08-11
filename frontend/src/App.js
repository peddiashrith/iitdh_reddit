import React from "react";
import "./App.css";
import Navbar from "./Components/Navbar";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import PostsList from "./Components/PostsList";
import Dashboard from "./Components/Dashboard";
import SignIn from "./Components/SignIn";
import SignUp from "./Components/SignUp";
import AddPost from "./Components/AddPost";
import MultiTags from "./Components/MultiTags";
import AllPosts from "./Components/AllPosts";
import CardTemp from "./Components/CardTemp";
import Login from "./Components/Login";
import GoogleBtn from "./Components/GoogleBtn";
function App() {
    return (
        <div className="App">
            <Router>
                <Navbar></Navbar>
                {/* <Login></Login> */}
                {/* <GoogleBtn></GoogleBtn> */}
                {/* <SignIn></SignIn> */}
                {/* <SignIn></SignIn> */}
                {/* <AddPost></AddPost> */}
                {/* <AllPosts></AllPosts> */}
                <CardTemp></CardTemp>
            </Router>
        </div>
    );
}

export default App;
