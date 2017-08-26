import React, { Component } from "react";
import PropTypes from "prop-types";
class TabSelector extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    let { children, handler } = this.props;
    return (
      <div className="tab-selector">
        <div className="tab-container">
          {React.Children.map(children, (child, i) => {
            return (
              <div
                className="tab-box"
                onClick={() => handler(child.props.value)}
              >
                {child}
              </div>
            );
          })}
        </div>
      </div>
    );
  }
}
TabSelector.propTypes = {
  handler: PropTypes.function
};

export default TabSelector;
