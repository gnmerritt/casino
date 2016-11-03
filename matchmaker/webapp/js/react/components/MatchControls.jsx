import React from 'react';

import MatchSelector from './MatchSelector';
import HandPager from './HandPager';
import PlayPause from './PlayPause';

function MatchControls() {
  return (
    <div>
      <MatchSelector />
      <HandPager>
        <PlayPause />
      </HandPager>
    </div>
  );
}

export default MatchControls;
