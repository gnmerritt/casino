import React from 'react';
import Reflux from 'reflux';
import { DropdownButton, MenuItem } from 'react-bootstrap';

import MatchesStore from '../stores/MatchesStore';

const MatchSelector = React.createClass({
  propTypes: {
    onChange: React.PropTypes.func.isRequired,
  },
  mixins: [Reflux.connect(MatchesStore, 'matches')],

  onSelect(eventKey) {
    this.props.onChange(this.state.matches[eventKey]);
  },

  renderOption(matchInfo, i) {
    return (
      <MenuItem eventKey={i}>{matchInfo.guid}</MenuItem>
    );
  },

  render() {
    return (
      <DropdownButton
        title="Select a match"
        id="matchSelector"
        onSelect={this.onSelect}
      >
        {this.state.matches.info.map(this.renderOption)}
      </DropdownButton>
    );
  },
});

export default MatchSelector;
