import React from "react";
import ReactDOM from "react-dom";
import { GoogleLogin } from "react-google-login";

const responseGoogle = (response) => {
    console.log(response);
};

function GoogleBtn() {
    return (
        <GoogleLogin
            clientId="220814816148-ruqpghv4hoo50veti2mjm2f4qvugnd80.apps.googleusercontent.com"
            buttonText="Login with Google"
            onSuccess={responseGoogle}
            onFailure={responseGoogle}
            cookiePolicy={"single_host_origin"}
        />
    );
}

export default GoogleBtn;
