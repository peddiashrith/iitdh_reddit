import React from "react";
import "./App.css";
import Navbar from "./Components/Navbar";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import PostsList from "./Components/PostsList";
import TempNavbar from "./Components/TempNavbar";
import Dashboard from "./Components/Dashboard";
import SignIn from "./Components/SignIn";
import SignUp from "./Components/SignUp";

function App() {
    return (
        <div className="App">
            <Router>
                <Navbar></Navbar>
                {/* <PostsList></PostsList> */}
                <TempNavbar></TempNavbar>
                {/* <SignUp></SignUp> */}
                {/* <Dashboard></Dashboard> */}
                {/* <Switch>
                    <Route exact path="/posts" component={PostsList} />
                </Switch> */}
            </Router>
        </div>
    );
}

export default App;
