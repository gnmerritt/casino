import React from 'react';
import ReactDOM from 'react-dom';

import MatchControls from './components/MatchControls';
import MatchWindow from './components/MatchWindow';

function ReplayApp() {
  return (
    <div>
      <MatchControls />
      <MatchWindow />
    </div>
  );
}

ReactDOM.render(
  <ReplayApp />,
  document.getElementById('replay-app')
);
