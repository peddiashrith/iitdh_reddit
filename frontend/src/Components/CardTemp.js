import React from "react";

function CardTemp() {
    return (
        <div class="container">
            <div class="card">
                <h5 class="card-header card-link">Ashrith</h5>
                <div class="card-body">
                    <h5 class="card-title">
                        Django together with Reactjs is Dope!
                    </h5>
                    <p class="card-text">
                        Card titles are used by adding .card-title to a tag. In
                        the same way, links are added and placed next to each
                        other by adding .card-link to an tag.
                    </p>
                    <div class="float-right">
                        <a href="#" class="btn btn-primary">
                            Accept
                        </a>{" "}
                        <a href="#" class="btn btn-danger">
                            Reject
                        </a>
                    </div>
                </div>
                <div class="card-footer">
                    <h5>Tags: </h5>
                    <a href="#" class="card-link">
                        Django
                    </a>
                    <a href="#" class="card-link">
                        Reactjs
                    </a>
                </div>
                <div class="card-footer">
                    <h5>References: </h5>
                    <a href="#" class="card-link">
                        google.com
                    </a>
                    <a href="#" class="card-link">
                        google.com
                    </a>
                    <a href="#" class="card-link">
                        google.com
                    </a>
                </div>
            </div>
        </div>
    );
}

export default CardTemp;
