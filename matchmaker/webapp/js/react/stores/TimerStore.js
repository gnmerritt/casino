import Reflux from 'reflux';

import TimerActions from '../actions/TimerActions';
import ReplayActions from '../actions/ReplayActions';

/**
 * Maintains the interval that advances the hand phase
 */
const TimerStore = Reflux.createStore({
  listenables: [TimerActions],
  state: {
    playing: false,
    speed: 1500, // ms between hand phases
  },

  phaseAdvanceInterval: null,

  getInitialState() {
    return this.state;
  },

  stopTicking() {
    if (this.handAdvanceInterval !== null) {
      clearInterval(this.phaseAdvanceInterval);
    }
  },

  setupInterval() {
    this.stopTicking();
    if (this.state.playing) {
      this.phaseAdvanceInterval = setInterval(ReplayActions.advancePhase, this.state.speed);
    }
  },

  onTogglePlaying() {
    this.state.playing = !this.state.playing;
    this.setupInterval();
    this.trigger(this.state);
  },

  onSetSpeed(speed) {
    this.state.speed = speed;
    this.setupInterval();
    this.trigger(this.state);
  },
});

export default TimerStore;
