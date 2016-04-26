import React from 'react';
import Reflux from 'reflux';
import { DropdownButton, MenuItem } from 'react-bootstrap';

import MatchesStore from '../stores/MatchesStore';
import ReplayActions from '../actions/ReplayActions';

const MatchSelector = React.createClass({
  mixins: [Reflux.connect(MatchesStore, 'matches')],

  onSelect(event, index) {
    ReplayActions.selectMatch(this.state.matches.info[index]);
  },

  renderOption(matchInfo, i) {
    return (
      <MenuItem key={i} eventKey={i}>{matchInfo.guid}</MenuItem>
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
