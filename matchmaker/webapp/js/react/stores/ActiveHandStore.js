import Reflux from 'reflux';
import $ from 'jquery';
import _ from 'underscore';

import ReplayStore from './ReplayStore';

const RESET = {
  players: [],
  remaining_players: [],
  player_cards: {},
  chips: {},
  table_cards: [],
  pot: 0,
  bets: {},
  currentPhase: null,
};

/**
 * The state of a hand of poker as constructed by a stream of game events
 */
const ActiveHandStore = Reflux.createStore({
  state: {},
  currentHand: -1,

  getInitialState() {
    return RESET;
  },

  init() {
    this.listenTo(ReplayStore, this.replayTick);
    this.reset();
  },

  reset() {
    this.state = $.extend({}, RESET);
    this.trigger(this.state);
  },

  replayTick(replayStore) {
    const hand = replayStore.currentHand;
    const phase = replayStore.currentPhase;
    if (!hand || !phase) {
      return;
    }
    if (replayStore.currentHand !== this.currentHand) {
      this.reset();
      this.consumeHand(hand);
      this.currentHand = replayStore.currentHand;
    }
    this.consumePhase(phase);
    this.trigger(this.state);
  },

  consumeHand(hand) {
    this.state.chips = $.extend({}, hand.initial_stacks);
    this.state.players = _.keys(hand.initial_stacks).sort();
    this.state.remaining_players = this.state.players;
  },

  consumePhase(phase) {
    this.state.currentPhase = phase;
    switch (phase.event) {
      case 'CARDS':
        this.state.player_cards[phase.player] = phase.data;
        break;
      case 'Raise':
        this.recordBet(phase.player, phase.data);
        break;
      case 'Check':
        // {data: 0, event: "Check", player: "bot_1", ts: 1459133258}
        break;
      case 'Fold':
        this.recordFold(phase.player);
        break;
      case 'REMAINING':
        this.state.remaining_players = phase.data;
        break;
      case 'POT':
        this.state.pot = phase.data;
        break;
      default:
        console.error(`Didn't handle phase ${phase.event}`);
        break;
    }
    console.warn(`After event: ${JSON.stringify(this.state)}`);
  },

  recordBet(player, bet) {
    const currentBet = this.state.bets[player] || 0;
    this.state.bets[player] = bet + currentBet;
  },

  recordFold(player) {
    const remaining = this.state.remaining_players;
    const playerIndex = _.findIndex(remaining, player);
    if (playerIndex >= 0) {
      this.state.remaining_players = remaining.splice(playerIndex, 1);
    }
  },
});

export default ActiveHandStore;
