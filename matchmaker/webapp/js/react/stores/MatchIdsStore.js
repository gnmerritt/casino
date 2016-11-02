import $ from 'jquery';
import Reflux from 'reflux';

import MatchActions from '../actions/MatchActions';

const MatchIdsStore = Reflux.createStore({
  listenables: [MatchActions],
  state: {
    info: ['Loading...'],
  },

  getInitialState() {
    return this.state;
  },

  init() {
    this.onFetchMatches();
  },

  onFetchMatches() {
    $.getJSON('/api/matches/finished', (pagedResp) => {
      this.state.info = pagedResp.data;
      this.trigger(this.state);
      MatchActions.fetchMatches.completed();
    });
  },
});

export default MatchIdsStore;
