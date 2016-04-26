import Reflux from 'reflux';

import ReplayActions from '../actions/ReplayActions';

const ReplayStore = Reflux.createStore({
  listenables: [ReplayActions],
  state: {
    playing: false,
    speed: 500, // ms between hand phases
    handNumber: 0,
    match: {},
  },

  getInitialState() {
    return this.state;
  },

  onSelectMatch(match) {
    this.state.match = match;
    this.trigger(this.state);
  },
});

export default ReplayStore;
