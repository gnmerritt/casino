import Reflux from 'reflux';
import $ from 'jquery';

import ReplayActions from '../actions/ReplayActions';

const ActiveMatchStore = Reflux.createStore({
  listenables: [ReplayActions],
  state: {
    loading: false,
    match: null,
  },

  onSelectMatch(match) {
    this.state.loading = true;
    this.trigger(this.state);
    const id = match.id;
    $.getJSON(`api/matches/${id}`, fullMatch => {
      this.state.match = fullMatch;
      this.state.loading = false;
      this.trigger(this.state);
    });
  },
});

export default ActiveMatchStore;
