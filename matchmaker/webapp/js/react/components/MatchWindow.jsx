import React from 'react';
import Reflux from 'reflux';

import ReplayStore from '../stores/ReplayStore';
import ActiveMatchStore from '../stores/ActiveMatchStore';

const MatchWindow = React.createClass({
  mixins: [
    Reflux.connect(ReplayStore, 'replay'),
    Reflux.connect(ActiveMatchStore, 'match'),
  ],

  render() {
    return (
      <div>
        <ul>
          <li>playing: {this.state.replay.playing ? 'true' : 'false'}</li>
          <li>speed: {this.state.replay.speed}</li>
          <li>handNumber: {this.state.replay.handNumber}</li>
          <li>match: {this.state.replay.match.guid}</li>
        </ul>
      </div>
    );
  },
});

export default MatchWindow;
