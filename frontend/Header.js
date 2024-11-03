import React, { Component } from 'react';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI.
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // You can also log the error to an error reporting service
    console.error('Uncaught error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return <h2>Something went wrong.</h2>;
    }

    return this.props.children; 
  }
}

export default ErrorBoundary;
```
```javascript
import React from 'react';
import ErrorBoundary from './ErrorBoundary'; // Ensure the path is correct
import Header from './Header'; // Ensure the path is correct

function App() {
  return (
    <div>
      <ErrorBoundary>
        <Header />
      </ErrorBoundary>
      {/* Other components can also be wrapped in ErrorBoundary */}
    </div>
  );
}

export default App;