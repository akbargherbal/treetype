// PATTERN: Async Patterns

import React, { useState, useEffect } from 'react';

function DataDisplay() {
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadItem = async () => {
      const response = await fetch('https://api.example.com/item');
      const data = await response.json();
      setItem(data);
      setLoading(false);
    };
    loadItem();
  }, []);

  if (loading) return <p>Loading item...</p>;
  return <p>Item name: {item.name}</p>;
}

// PATTERN: Async Patterns

import React, { useState } from 'react';

function ActionButton() {
  const [isProcessing, setIsProcessing] = useState(false);

  const handleClick = async () => {
    setIsProcessing(true);
    // Simulate an async operation
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsProcessing(false);
  };

  return (
    <button onClick={handleClick} disabled={isProcessing}>
      {isProcessing ? 'Working...' : 'Start Action'}
    </button>
  );
}

// PATTERN: Async Patterns

import React from 'react';

class ErrorBoundary extends React.Component {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error, info) { /* Log error to a service */ }

  render() {
    if (this.state.hasError) return <h1>Something went wrong.</h1>;
    return this.props.children;
  }
}

function App() {
  const Buggy = () => { throw new Error('Crash!'); };
  return (
    <ErrorBoundary>
      <Buggy />
    </ErrorBoundary>
  );
}