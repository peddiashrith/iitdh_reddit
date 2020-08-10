import React, { Component } from "react";
import { GoogleLogin, GoogleLogout } from "react-google-login";

const CLIENT_ID =
    "220814816148-ruqpghv4hoo50veti2mjm2f4qvugnd80.apps.googleusercontent.com";
const CLIENT_SECRET = "4VTAO5DXMgl5eZZpaBpaWsaJ";

class Login extends Component {
    constructor(props) {
        super(props);

        this.state = {
            isLogined: false,
            accessToken: "",
        };

        this.login = this.login.bind(this);
        this.handleLoginFailure = this.handleLoginFailure.bind(this);
        this.logout = this.logout.bind(this);
        this.handleLogoutFailure = this.handleLogoutFailure.bind(this);
    }

    login(response) {
        if (response.accessToken) {
            this.setState((state) => ({
                isLogined: true,
                accessToken: response.accessToken,
            }));
        }
    }

    logout(response) {
        this.setState((state) => ({
            isLogined: false,
            accessToken: "",
        }));
    }

    handleLoginFailure(response) {
        alert("Failed to log in");
    }

    handleLogoutFailure(response) {
        alert("Failed to log out");
    }

    render() {
        return (
            <div className="container center">
                {this.state.isLogined ? (
                    <GoogleLogout
                        clientId={CLIENT_ID}
                        buttonText="Logout"
                        onLogoutSuccess={this.logout}
                        onFailure={this.handleLogoutFailure}
                    ></GoogleLogout>
                ) : (
                    <GoogleLogin
                        clientId={CLIENT_ID}
                        buttonText="Login"
                        onSuccess={this.login}
                        onFailure={this.handleLoginFailure}
                        cookiePolicy={"single_host_origin"}
                        responseType="code,token"
                    />
                )}
                {this.state.accessToken ? (
                    <h5>
                        Your Access Token: <br />
                        <br /> {this.state.accessToken}
                    </h5>
                ) : null}
            </div>
        );
    }
}

export default Login;
