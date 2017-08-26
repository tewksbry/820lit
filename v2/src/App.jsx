import React, { Component } from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import { LockRoute, ControlsRoute } from "./routes";

class App extends Component {
  render() {
    return (
      <div className="App">
        <Router>
          <div>
            <Route path="/" exact={true} component={LockRoute} />
            <Route path="/controls" component={ControlsRoute} />
          </div>
        </Router>
      </div>
    );
  }
}

export default App;
