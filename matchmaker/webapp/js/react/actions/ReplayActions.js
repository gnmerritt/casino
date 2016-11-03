import Reflux from 'reflux';

const ReplayActions = Reflux.createActions([
  'selectMatch',
  'advancePhase',
  'nextHand',
  'previousHand',
]);

export default ReplayActions;
