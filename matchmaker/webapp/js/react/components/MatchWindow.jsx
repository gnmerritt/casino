import React from 'react';
import Reflux from 'reflux';

import ReplayStore from '../stores/ReplayStore';
import ActiveMatchStore from '../stores/ActiveMatchStore';
import ActiveHandStore from '../stores/ActiveHandStore';

const MatchWindow = React.createClass({
  mixins: [
    Reflux.connect(ReplayStore, 'replay'),
    Reflux.connect(ActiveMatchStore, 'match'),
    Reflux.connect(ActiveHandStore, 'hand'),
  ],

  render() {
    return (
      <div>
        <ul>
          <li>playing: {this.state.replay.playing ? 'true' : 'false'}</li>
          <li>speed: {this.state.replay.speed}</li>
          <li>handNumber: {this.state.replay.handNumber} / {this.state.replay.hands.length}</li>
          <li>handPhase: {this.state.replay.handPhase}</li>
          <li>match: {this.state.replay.match.guid}</li>
        </ul>
        <div>Current: {this.state.currentPhase}</div>
      </div>
    );
  },
});

export default MatchWindow;
