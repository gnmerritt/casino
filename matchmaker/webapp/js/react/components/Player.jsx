import React from 'react';
import Reflux from 'reflux';

import Card from '../cards/Card';
import ActiveHandStore from '../stores/ActiveHandStore';

const Player = React.createClass({
  propTypes: {
    name: React.PropTypes.string.isRequired,
  },
  mixins: [Reflux.connect(ActiveHandStore, 'hand')],

  render() {
    const name = this.props.name;
    const chips = this.state.hand.chips[name];
    const hand = this.state.hand.player_cards[name] || [];
    return (
      <div>
        <div>Name: {this.props.name}</div>
        <div>Chips: {chips}</div>
        <div>Cards: {hand.map(card => <Card key={card} cardString={card} />)}</div>
      </div>
    );
  },
});

export default Player;
