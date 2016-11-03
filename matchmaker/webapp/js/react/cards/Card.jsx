import React from 'react';

import { fromString } from './Parser';

const Card = props => {
  const card = fromString(props.cardString);
  return (
    <div>
      {card.rankName} of {card.suitName}
    </div>
  );
};

Card.propTypes = {
  cardString: React.PropTypes.string.isRequired,
};

export default Card;
