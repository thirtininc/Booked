import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import ExampleComponent from './components/ExampleComponent';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={ExampleComponent} />
          {/* Add more routes here as needed */}
        </Switch>
      </div>
    </Router>
  );
}

export default App;