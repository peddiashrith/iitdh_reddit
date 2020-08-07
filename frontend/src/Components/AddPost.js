import React, { Component } from "react";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import PostAddIcon from "@material-ui/icons/PostAdd";
import Typography from "@material-ui/core/Typography";
import { makeStyles, withStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import MultiTags from "./MultiTags";

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
    form: {
        width: "100%", // Fix IE 11 issue.
        marginTop: theme.spacing(3),
    },
    submit: {
        margin: theme.spacing(3, 0, 2),
    },
});
export class AddPost extends Component {
    constructor(props) {
        super(props);

        this.state = {
            post_title: "",
            post_description: "",
            post_tags: [],
            post_links: [],
        };
    }

    handleChange = (event) => {
        this.setState(
            {
                [event.target.name]: event.target.value,
            },
            console.log(`After changinng ${this.state}`)
        );
    };

    handleSubmit = (event) => {
        event.preventDefault();
        console.log("Clicked");
    };

    render() {
        const { classes } = this.props;
        return (
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <div className={classes.paper}>
                    <Avatar className={classes.avatar}>
                        <PostAddIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Create Post
                    </Typography>
                    <form className={classes.form} noValidate>
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <TextField
                                    name="post_title"
                                    value={this.state.post_title}
                                    variant="outlined"
                                    required
                                    fullWidth
                                    id="post_title"
                                    label="Post Title"
                                    autoFocus
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    name="post_description"
                                    variant="outlined"
                                    required
                                    multiline
                                    rows={5}
                                    fullWidth
                                    id="post_description"
                                    label="Post Description"
                                    name="post_description"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <MultiTags />
                            </Grid>
                        </Grid>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            color="primary"
                            className={classes.submit}
                            onClick={this.handleSubmit}
                        >
                            Create
                        </Button>
                    </form>
                </div>
            </Container>
        );
    }
}

export default withStyles(useStyles, { withTheme: true })(AddPost);
