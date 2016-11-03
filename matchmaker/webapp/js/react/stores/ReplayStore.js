import Reflux from 'reflux';

import ReplayActions from '../actions/ReplayActions';
import ActiveMatchStore from './ActiveMatchStore';

/**
 * Keeps track of what hand/phase we're on in the active match
 */
const ReplayStore = Reflux.createStore({
  listenables: [ReplayActions],
  state: {
    handNumber: 0,
    handPhase: 0,
    hands: [],
    currentHand: null,
    currentPhase: null,
    match: {},
    loading: false,
  },

  getInitialState() {
    return this.state;
  },

  init() {
    this.listenTo(ActiveMatchStore, this.updateActiveMatch);
  },

  updateActiveMatch(activeMatchStore) {
    if (!activeMatchStore.loading) {
      const fullMatch = activeMatchStore.match;
      this.state.hands = fullMatch.hands;
      this.trigger(this.state);
    }
  },

  onSelectMatch(match) {
    this.state.match = match;
    this.trigger(this.state);
  },

  onNextHand() {
    this.state.handNumber = this.state.handNumber + 1;
    this.newHand();
    this.trigger(this.state);
  },

  onPreviousHand() {
    this.state.handNumber = Math.max(0, this.state.handNumber - 1);
    this.newHand();
    this.trigger(this.state);
  },

  newHand() {
    this.state.handPhase = 0;
    this.state.currentHand = this.state.hands[this.state.handNumber];
    this.newPhase();
  },

  newPhase() {
    this.state.currentPhase = this.state.currentHand.actions[this.state.handPhase];
  },

  onAdvancePhase() {
    if (this.state.handNumber === this.state.hands.length) {
      return;
    }
    if (!this.state.currentHand) {
      this.newHand();
    }
    // advance the hand phase if there are more, or go to the next hand
    const hand = this.state.currentHand;
    const handFinished = this.state.handPhase === hand.actions.length;
    if (handFinished) {
      this.onNextHand();
    } else {
      this.state.handPhase = this.state.handPhase + 1;
      this.newPhase();
      this.trigger(this.state);
    }
  },
});

export default ReplayStore;
