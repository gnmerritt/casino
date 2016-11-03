
const SUITS = {
  d: 'Diamonds',
  h: 'Hearts',
  s: 'Spades',
  c: 'Clubs',
};

const RANKS = {
  A: 'Ace',
  K: 'King',
  Q: 'Queen',
  J: 'Jack',
  T: 'Ten',
};

class Card {
  constructor(rank, suit) {
    this._rank = rank;
    this._suit = suit;
  }

  get rank() {
    return this._rank;
  }

  get rankName() {
    return RANKS[this._rank] || this._rank;
  }

  get suit() {
    return this._suit;
  }

  get suitName() {
    return SUITS[this._suit];
  }
}

/**
 * Returns a card object from a card string
 */
const fromString = cardString => {
  if (!typeof(cardString) === 'string' || cardString.length < 2) {
    throw new Error(`Invalid cardstring '${cardString}'`);
  }
  const rank = cardString.slice(0, -1);
  const suit = cardString.slice(-1);
  return new Card(rank, suit);
};

export {
  Card,
  fromString,
};
