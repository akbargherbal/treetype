// PATTERN: Performance Patterns

import React, { useState, useMemo } from 'react';

function ProductFilter({ products }) {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredProducts = useMemo(() => {
    // This calculation runs only when products or searchTerm changes
    return products.filter(product =>
      product.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [products, searchTerm]);

  return (
    <div>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      {filteredProducts.map(product => (
        <div key={product.id}>{product.name}</div>
      ))}
    </div>
  );
}

// PATTERN: Performance Patterns

import React, { useState, useCallback, memo } from 'react';

const MemoizedButton = memo(({ onClick, label }) => {
  // This component only re-renders if onClick or label props change
  return <button onClick={onClick}>{label}</button>;
});

function ParentComponent() {
  const [count, setCount] = useState(0);
  const [toggle, setToggle] = useState(false);

  const handleClick = useCallback(() => {
    setCount(prevCount => prevCount + 1);
  }, []); // Memoizes the function, preventing re-creation on parent re-renders

  return (
    <div>
      <p>Count: {count}</p>
      <MemoizedButton onClick={handleClick} label="Increment" />
      <button onClick={() => setToggle(!toggle)}>Toggle Parent State</button>
    </div>
  );
}

// PATTERN: Performance Patterns

import React, { useState, memo } from 'react';

const MemoizedDisplay = memo(({ value }) => {
  // This component only re-renders if its 'value' prop changes
  return <p>Current Value: {value}</p>;
});

function App() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState('');

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Increment Count</button>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <MemoizedDisplay value={count} />
      <p>Input Text: {text}</p>
    </div>
  );
}