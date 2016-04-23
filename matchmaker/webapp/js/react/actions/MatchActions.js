import Reflux from 'reflux';

const MatchActions = Reflux.createActions({
  fetchMatches: { asyncResult: true },
});

export default MatchActions;
