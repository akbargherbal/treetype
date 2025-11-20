// PATTERN: Common UI Patterns

import React, { useState } from 'react';

function ModalToggle() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? 'Close Modal' : 'Open Modal'}
      </button>
      {isOpen && (
        <div style={{ border: '1px solid black', padding: '20px', margin: '10px', background: 'white' }}>
          <h3>Modal Content</h3>
          <p>This is your modal dialog.</p>
          <button onClick={() => setIsOpen(false)}>Close</button>
        </div>
      )}
    </div>
  );
}

// PATTERN: Common UI Patterns

import React, { useState } from 'react';

function AccordionItem() {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div style={{ border: '1px solid #ccc', margin: '5px' }}>
      <button onClick={() => setIsExpanded(!isExpanded)} style={{ width: '100%', textAlign: 'left', padding: '10px' }}>
        Section Title {isExpanded ? '▲' : '▼'}
      </button>
      {isExpanded && (
        <div style={{ padding: '10px', borderTop: '1px solid #eee' }}>
          <p>Content for the collapsible section.</p>
        </div>
      )}
    </div>
  );
}

// PATTERN: Common UI Patterns

import React, { useState } from 'react';

function Tabs() {
  const [activeTab, setActiveTab] = useState('tab1');

  return (
    <div>
      <div>
        <button onClick={() => setActiveTab('tab1')}>Tab 1</button>
        <button onClick={() => setActiveTab('tab2')}>Tab 2</button>
      </div>
      <div style={{ border: '1px solid #ccc', padding: '10px', marginTop: '5px' }}>
        {activeTab === 'tab1' && <p>Content for Tab 1.</p>}
        {activeTab === 'tab2' && <p>Content for Tab 2.</p>}
      </div>
    </div>
  );
}

// PATTERN: Common UI Patterns

import React, { useState, useEffect } from 'react';

function DebouncedInput() {
  const [inputValue, setInputValue] = useState('');
  const [debouncedValue, setDebouncedValue] = useState('');

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(inputValue), 500);
    return () => clearTimeout(handler);
  }, [inputValue]);

  return (
    <>
      <input value={inputValue} onChange={(e) => setInputValue(e.target.value)} />
      <p>Debounced: {debouncedValue}</p>
    </>
  );
}

// PATTERN: Common UI Patterns

import React, { useState, useEffect, useRef } from 'react';

function InfiniteScrollList() {
  const [items, setItems] = useState(Array.from({ length: 10 }, (_, i) => `Item ${i + 1}`));
  const loaderRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        setItems(prev => [...prev, ...Array.from({ length: 5 }, (_, i) => `Item ${prev.length + i + 1}`)]);
      }
    }, { threshold: 1.0 });
    if (loaderRef.current) observer.observe(loaderRef.current);
    return () => { if (loaderRef.current) observer.unobserve(loaderRef.current); };
  }, [items.length]);

  return (
    <div style={{ height: '200px', overflowY: 'scroll', border: '1px solid #ccc' }}>
      {items.map((item, i) => <div key={i} style={{ padding: '8px' }}>{item}</div>)}
      <div ref={loaderRef} style={{ height: '20px', background: '#f0f0f0' }}>Loading...</div>
    </div>
  );
}