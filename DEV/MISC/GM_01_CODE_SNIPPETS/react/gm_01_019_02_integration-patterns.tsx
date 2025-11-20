// PATTERN: Integration Patterns

import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://api.example.com',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
  },
  timeout: 5000,
});

export default apiClient;

// PATTERN: Integration Patterns

import React, { useState } from 'react';

function DataFetcher() {
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const response = await fetch('https://api.example.com/data');
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      await response.json(); // Process data, or just consume
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <button onClick={fetchData}>Fetch Data</button>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
    </div>
  );
}

export default DataFetcher;

// PATTERN: Integration Patterns

import React from 'react';
import toast, { Toaster } from 'react-hot-toast'; // npm install react-hot-toast

function NotificationButton() {
  const showToast = () => {
    toast.success('Item added to cart!', {
      duration: 3000,
      position: 'top-right',
    });
  };

  return (
    <div>
      <button onClick={showToast}>Add to Cart</button>
      <Toaster />
    </div>
  );
}

export default NotificationButton;

// PATTERN: Integration Patterns

import React from 'react';

function LoadingSpinner({ isLoading }) {
  if (!isLoading) return null;

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      padding: '20px',
      color: '#007bff'
    }}>
      Loading data...
    </div>
  );
}

export default LoadingSpinner;