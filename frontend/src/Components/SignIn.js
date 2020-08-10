import React, { Component } from "react";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import Typography from "@material-ui/core/Typography";
import { makeStyles, withStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import PersonIcon from "@material-ui/icons/Person";
import { GoogleLogin, GoogleLogout } from "react-google-login";

const CLIENT_ID =
    "220814816148-ruqpghv4hoo50veti2mjm2f4qvugnd80.apps.googleusercontent.com";

const useStyles = (theme) => ({
    paper: {
        marginTop: theme.spacing(8),
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
    },
    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main,
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
});

export class SignIn extends Component {
    constructor(props) {
        super(props);

        this.state = {
            isLoggedIn: false,
            accessToken: "",
            // name: "",
            // email: "",
            // image: "",
        };
    }

    handleLogin = (response) => {
        if (response.accessToken) {
            this.setState({
                isLoggedIn: true,
                accessToken: response.accessToken,
                // name: response.profileObj.name,
                // email: response.profileObj.email,
                // image: response.profileObj.imageUrl,
            });
            // localStorage.setItem("accessToken", response.accessToken);
        }
    };

    handleLogout = (response) => {
        this.setState({
            isLogined: false,
            accessToken: "",
        });
    };

    handleLoginFailure(response) {
        alert("Failed to log in");
    }

    handleLogoutFailure(response) {
        alert("Failed to log out");
    }

    render() {
        const { classes } = this.props;
        return (
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <div className={classes.paper}>
                    <Avatar className={classes.avatar}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign in
                    </Typography>
                    <Typography component="h2" variant="h5">
                        Login with <strong>IITDH</strong> account
                    </Typography>
                    <GoogleLogin
                        clientId={CLIENT_ID}
                        render={(
                            renderProps /* Custom styling for the google button*/
                        ) => (
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                color="primary"
                                className={classes.submit}
                                startIcon={<PersonIcon></PersonIcon>}
                                onClick={renderProps.onClick}
                                disabled={renderProps.disabled}
                            >
                                Login with Google
                            </Button>
                        )}
                        buttonText="Login with Google"
                        onSuccess={this.handleLogin}
                        onFailure={this.handleLoginFailure}
                        cookiePolicy={"single_host_origin"}
                        responseType="code,token"
                    />

                    {/* <Typography variant="h5">
                        username:{this.state.name}
                        email:{this.state.email}
                        <img src={this.state.image}></img>
                    </Typography> */}
                </div>
            </Container>
        );
    }
}

export default withStyles(useStyles, { withTheme: true })(SignIn);
