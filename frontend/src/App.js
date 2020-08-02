import React from "react";
import "./App.css";
import Navbar from "./Components/Navbar";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import PostsList from "./Components/PostsList";

function App() {
    return (
        <div className="App">
            <Router>
                <Navbar></Navbar>
                <Switch>
                    <Route exact path="/posts" component={PostsList} />
                </Switch>
            </Router>
        </div>
    );
}

export default App;
