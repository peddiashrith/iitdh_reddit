import React, { Component } from 'react';

export class CardTemp extends Component {
    constructor(props) {
        super(props);

        this.state = {
            allposts: [],
        };
    }

    componentDidMount = async () => {
        fetch('http://localhost:8000/api/feed/')
            .then((response) => response.json())
            .then((data) =>
                this.setState(
                    {
                        allposts: data,
                    },
                    () => console.log(this.state)
                )
            );
    };

    render() {
        return (
            <div className='container'>
                <div className='jumbotron'>
                    <h3>r/Django</h3>
                </div>
                {this.state.allposts.map((post, index) => (
                    <div className='card' key={post.id}>
                        <h5 className='card-header card-link'>
                            {post.author.username}
                        </h5>
                        <div className='card-body'>
                            <p className='card-text'>{post.description}</p>
                            <div className='float-right'>
                                <a href='#' className='btn btn-primary'>
                                    Accept
                                </a>{' '}
                                <a href='#' className='btn btn-danger'>
                                    Reject
                                </a>
                            </div>
                        </div>
                        <div className='card-footer'>
                            <h5>Tags: </h5>
                            {post.tags.map((tag, index) => (
                                <a href='#' className='card-link' key={index}>
                                    {tag}
                                </a>
                            ))}
                        </div>
                        <div className='card-footer'>
                            <h5>Links: </h5>
                            {post.links.map((link, index) => (
                                <a href='#' className='card-link' key={index}>
                                    {link}
                                </a>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        );
    }
}

export default CardTemp;
