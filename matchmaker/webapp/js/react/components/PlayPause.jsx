import React from 'react';
import Reflux from 'reflux';
import { Button } from 'react-bootstrap';

import TimerActions from '../actions/TimerActions';
import TimerStore from '../stores/TimerStore';

const PlayPause = React.createClass({
  mixins: [Reflux.connect(TimerStore, 'replay')],

  render() {
    const text = this.state.replay.playing ? 'Pause' : 'Play';
    return (
      <Button onClick={TimerActions.togglePlaying} >
        {text}
      </Button>
    );
  },
});

export default PlayPause;
