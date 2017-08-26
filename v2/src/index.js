import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import darkBaseTheme from "material-ui/styles/baseThemes/darkBaseTheme";
import getMuiTheme from "material-ui/styles/getMuiTheme";
import App from "./App";
import MuiThemeProvider from "material-ui/styles/MuiThemeProvider";

let theme = getMuiTheme(darkBaseTheme);

ReactDOM.render(
  <MuiThemeProvider muiTheme={theme}>
    <App />
  </MuiThemeProvider>,
  document.getElementById("root")
);
