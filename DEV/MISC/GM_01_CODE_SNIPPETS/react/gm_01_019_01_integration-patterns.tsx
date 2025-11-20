// PATTERN: Integration Patterns

// src/api/apiClient.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://api.example.com/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
  }
});

export default apiClient;

// PATTERN: Integration Patterns

// src/components/DataFetcher.jsx
import React, { useState, useEffect } from 'react';
import apiClient from '../api/apiClient'; // Assuming apiClient from pattern 1

function DataFetcher() {
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        await apiClient.get('/secure-data');
        setError(null); // Clear any previous errors
      } catch (err) {
        setError(err.response?.data?.message || 'An unexpected error occurred.');
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {!error && <p>Data loaded successfully (or loading).</p>}
    </div>
  );
}

export default DataFetcher;

// PATTERN: Integration Patterns

// src/App.jsx or a component
import React from 'react';
import toast, { Toaster } from 'react-hot-toast'; // npm install react-hot-toast

function App() {
  const notifySuccess = () => toast.success('Operation completed successfully!');
  const notifyError = () => toast.error('Something went wrong. Please try again.');

  return (
    <div>
      <button onClick={notifySuccess}>Show Success</button>
      <button onClick={notifyError}>Show Error</button>
      <Toaster />
    </div>
  );
}

export default App;

// PATTERN: Integration Patterns

// src/components/LoadingSpinner.jsx
import React from 'react';

function LoadingSpinner({ isLoading }) {
  if (!isLoading) return null;

  return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: '20px' }}>
      <div className="spinner"></div>
      {/* Basic CSS for spinner (e.g., in App.css):
      .spinner { border: 4px solid rgba(0,0,0,.1); width: 36px; height: 36px; border-radius: 50%; border-left-color: #09f; animation: spin 1s ease infinite; }
      @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
      */}
    </div>
  );
}

export default LoadingSpinner;