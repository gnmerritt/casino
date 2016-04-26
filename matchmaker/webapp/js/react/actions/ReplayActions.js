import Reflux from 'reflux';

const ReplayActions = Reflux.createActions([
  'selectMatch',
  'togglePlaying',
  'nextHand',
  'previousHand',
  'setSpeed',
]);

export default ReplayActions;
