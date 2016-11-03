import React from 'react';
import { Button, ButtonGroup } from 'react-bootstrap';

import ReplayActions from '../actions/ReplayActions';

const HandPager = props =>
  <ButtonGroup>
    <Button onClick={ReplayActions.previousHand}>Previous</Button>
    {props.children}
    <Button onClick={ReplayActions.nextHand}>Next</Button>
  </ButtonGroup>;

HandPager.propTypes = {
  children: React.PropTypes.node,
};

export default HandPager;
