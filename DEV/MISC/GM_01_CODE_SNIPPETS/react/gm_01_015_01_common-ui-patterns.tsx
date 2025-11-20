// PATTERN: Common UI Patterns

import React, { useState } from 'react';

function ModalToggle() {
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <button onClick={() => setShowModal(true)}>Open Dialog</button>
      {showModal && (
        <div style={{ padding: '20px', border: '1px solid #ccc', background: 'white' }}>
          <h3>Dialog Content</h3>
          <button onClick={() => setShowModal(false)}>Close</button>
        </div>
      )}
    </>
  );
}

// PATTERN: Common UI Patterns

import React, { useState } from 'react';

function AccordionItem() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)} style={{ width: '100%', textAlign: 'left', padding: '10px' }}>
        Toggle Section
      </button>
      {isOpen && (
        <div style={{ padding: '10px', border: '1px solid #eee' }}>
          This is the collapsible content.
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
      <div style={{ border: '1px solid #ccc', padding: '10px', marginTop: '10px' }}>
        {activeTab === 'tab1' && <p>Content for Tab 1</p>}
        {activeTab === 'tab2' && <p>Content for Tab 2</p>}
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
    <div>
      <input value={inputValue} onChange={e => setInputValue(e.target.value)} />
      <p>Debounced: {debouncedValue}</p>
    </div>
  );
}

// PATTERN: Common UI Patterns

import React, { useState, useEffect, useRef } from 'react';

function InfiniteScroll() {
  const [items, setItems] = useState([]);
  const [page, setPage] = useState(0);
  const loaderRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) setPage(p => p + 1);
    }, { threshold: 1.0 });
    if (loaderRef.current) observer.observe(loaderRef.current);
    return () => { if (loaderRef.current) observer.unobserve(loaderRef.current); };
  }, [loaderRef]);

  useEffect(() => {
    setItems(prev => [...prev, ...Array.from({ length: 5 }, (_, i) => `Item ${page * 5 + i + 1}`)]);
  }, [page]);

  return (
    <div style={{ height: '200px', overflowY: 'scroll', border: '1px solid #ccc' }}>
      {items.map((item, i) => <p key={i}>{item}</p>)}
      <div ref={loaderRef} style={{ height: '10px', background: '#eee' }}></div>
    </div>
  );
}