import React from 'react';
import ReactDOM from 'react-dom';

import MatchSelector from './components/MatchSelector';

function ReplayApp() {
  return (
    <div>
      <div>Hello, react (with selector)?</div>
      <MatchSelector />
    </div>
  );
}

ReactDOM.render(
  <ReplayApp />,
  document.getElementById('replay-app')
);
