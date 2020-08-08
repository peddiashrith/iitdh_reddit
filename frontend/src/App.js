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
function App() {
    return (
        <div className="App">
            <Router>
                <Navbar></Navbar>
                {/* <PostsList></PostsList> */}
                {/* <SignIn></SignIn> */}
                {/* <AddPost></AddPost> */}
                {/* <AllPosts></AllPosts> */}
                {/* <AllPosts></AllPosts> */}
                <CardTemp></CardTemp>
                {/* <CardTemp></CardTemp> */}
            </Router>
        </div>
    );
}

export default App;
