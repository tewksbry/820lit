import React, { Component } from "react";
import { Header, Controls } from "../components";
import * as firebase from "firebase";

export default class ControlsContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: {}
    };
    this.app = firebase.initializeApp({
      apiKey: "AIzaSyCw2VULu88Y6GFyIhA3uX3xH0ELNyGZRX8",
      authDomain: "sound-visualizer-6443f.firebaseapp.com",
      databaseURL: "https://sound-visualizer-6443f.firebaseio.com",
      storageBucket: "sound-visualizer-6443f.appspot.com",
      messagingSenderId: "990692069532"
    });
    this.database = firebase.database();
    this.database.ref("/").on("value", snap => this.setData(snap));
  }
  setData(snap) {
    let data = snap.val();
    this.setState({ data });
  }
  updateFirebase(update) {
    this.database.ref("/").update(update);
  }

  render() {
    return (
      <div className="controls-container">
        <Header />
        <Controls
          data={this.state.data}
          update={update => this.updateFirebase(update)}
        />
      </div>
    );
  }
}
