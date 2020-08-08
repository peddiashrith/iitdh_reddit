import React from "react";
import "../css/Card.css";
import Defaultimg from "../images/default.jpg";
function AllPosts() {
    return (
        <div className="container">
            <div className="row">
                <div className="col">
                    <article className="media content-section">
                        <img
                            className="rounded-circle article-img"
                            src={Defaultimg}
                            alt="profile"
                        />
                        <div className="media-body">
                            <div className="article-metadata">
                                <a className="mr-2" href="google.com">
                                    Ashrith
                                </a>
                                <small className="text-muted">
                                    created on: Aug 8, 2020
                                </small>
                                <small className="text-muted">
                                    updated on: Aug 8, 2020
                                </small>
                            </div>
                            <h2>
                                <a className="article-title" href="google.com">
                                    Django and Reactjs
                                </a>
                            </h2>
                            <p className="article-content">Small Description</p>
                            <a className="article-content" href="google.com">
                                <b>Links</b>
                            </a>
                        </div>
                    </article>
                </div>
            </div>
        </div>
    );
}

export default AllPosts;
