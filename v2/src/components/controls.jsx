import React, { Component } from "react";
import { Card, CardHeader, CardActions } from "material-ui/Card";
import { GridList, GridTile } from "material-ui/GridList";
import Toggle from "material-ui/Toggle";
import Slider from "material-ui/Slider";
import { ChromePicker } from "react-color";
import { TabSelector } from "./";

export default class Controls extends Component {
  constructor(props) {
    super(props);
  }
  handleColorChange(color, event) {
    console.log(color.rgb);
    this.props.update({
      R: color.rgb.r,
      B: color.rgb.b,
      G: color.rgb.g
    });
  }
  render() {
    let {
      B,
      DisplayID,
      G,
      PatternID,
      R,
      W,
      brightedges,
      brightness,
      cutoff,
      cycleSpeed,
      dimcenter,
      fade,
      on
    } = this.props.data;
    let basicData = {
      on,
      brightedges,
      dimcenter,
      brightness
    };
    let advancedData = {
      cycleSpeed,
      cutoff,
      fade
    };
    return (
      <div className="controls-container">
        <Basics data={basicData} update={update => this.props.update(update)} />
        <Color
          color={{ B, G, R }}
          onChange={(color, event) => this.handleColorChange(color)}
        />
        <Advanced
          data={advancedData}
          update={update => this.props.update(update)}
        />
        <Patterns update={id => this.props.update({ PatternID: id })} />
        <Displays update={id => this.props.update({ DisplayID: id })} />
      </div>
    );
  }
}
const Basics = props => {
  let { data } = props;
  return (
    <div className="control-container">
      <Card>
        <CardHeader title="Basic Controls" />
        <CardActions>
          <Toggle
            label="Power"
            toggled={data.on}
            onToggle={() => props.update({ on: data.on ? 0 : 1 })}
          />
          <Toggle
            label="Bright Edges"
            toggled={data.brightedges}
            onToggle={() =>
              props.update({ brightedges: data.brightedges ? 0 : 1 })}
          />
          <Toggle
            label="Dim Center"
            toggled={data.dimcenter}
            onToggle={() => props.update({ dimcenter: data.dimcenter ? 0 : 1 })}
          />
          <div>
            Brightness
            <Slider
              value={data.brightness}
              max={255}
              onChange={(event, value) => {
                props.update({ brightness: value });
              }}
            />
          </div>
        </CardActions>
      </Card>
    </div>
  );
};
const Color = props => {
  let { R, G, B } = props.color;
  return (
    <div className="control-container">
      <Card>
        <CardHeader title="Color" />
        <ChromePicker
          onChange={color => props.onChange(color)}
          color={{ r: R, g: G, b: B }}
        />
      </Card>
    </div>
  );
};
const Advanced = props => {
  return (
    <div className="control-container">
      <Card>
        <CardHeader title="Advanced Controls" />
        <CardActions>
          <div>
            Cutoff
            <Slider
              value={props.data.cutoff}
              onChange={(event, value) => props.update({ cutoff: value })}
              max={1}
            />
          </div>
          <div>
            Fade
            <Slider
              value={props.data.fade}
              onChange={(event, value) => props.update({ fade: value })}
              max={1}
            />
          </div>
          <div>
            Cycle
            <Slider
              value={props.data.cycleSpeed}
              onChange={(event, value) => props.update({ cycleSpeed: value })}
              max={255}
            />
          </div>
        </CardActions>
      </Card>
    </div>
  );
};
const Patterns = props => {
  return (
    <div className="control-container">
      <Card>
        <CardHeader title="Patterns" />
        <TabSelector handler={id => props.update(id)}>
          <h3 value={0}> Single Light </h3>
          <h3 value={1}> Rainbow </h3>
          <h3 value={2}> Random </h3>
          <h3 value={3}> Random Bright </h3>
          <h3 value={4}> Grayscale </h3>
          <h3 value={5}> USC </h3>
          <h3 value={6}> Mood </h3>
        </TabSelector>
      </Card>
    </div>
  );
};

const Displays = props => {
  return (
    <div className="control-container">
      <Card>
        <CardHeader title="Dipslays" />
        <TabSelector handler={id => props.update(id)}>
          <h3 value={0}> Fill </h3>
          <h3 value={1}> Middle Out </h3>
          <h3 value={2}> Middle Out Fill </h3>
          <h3 value={3}> Strobe </h3>
          <h3 value={4}> Cycle </h3>
          <h3 value={5}> Midddle Out White </h3>
        </TabSelector>
      </Card>
    </div>
  );
};
