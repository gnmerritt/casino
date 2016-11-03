import React from 'react';
import Reflux from 'reflux';

import ReplayStore from '../stores/ReplayStore';
import ActiveMatchStore from '../stores/ActiveMatchStore';
import ActiveHandStore from '../stores/ActiveHandStore';

import Player from './Player';

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

        <div>
          <h2>Players</h2>
          {this.state.hand.players.map(p => <Player name={p} key={p} />)}
        </div>
      </div>
    );
  },
});

export default MatchWindow;
