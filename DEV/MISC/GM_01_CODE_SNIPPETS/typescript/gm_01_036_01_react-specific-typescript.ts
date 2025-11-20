// PATTERN: React-Specific TypeScript

import React from 'react';

interface GreetingProps {
  name: string;
}

const Greeting: React.FC<GreetingProps> = ({ name }) => {
  return <div>Hello, {name}!</div>;
};

export default Greeting;

// PATTERN: React-Specific TypeScript

import React from 'react';

interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({ label, onClick, disabled = false }) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
};

export default Button;

// PATTERN: React-Specific TypeScript

import React from 'react';

interface CardProps {
  title: string;
  children: React.ReactNode;
}

const Card: React.FC<CardProps> = ({ title, children }) => {
  return (
    <div style={{ border: '1px solid gray', padding: '10px' }}>
      <h3>{title}</h3>
      {children}
    </div>
  );
};

export default Card;

// PATTERN: React-Specific TypeScript

import React, { useState } from 'react';

const InteractiveComponent: React.FC = () => {
  const [inputValue, setInputValue] = useState('');

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    console.log('Button clicked!', event.currentTarget.tagName);
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  return (
    <div>
      <input type="text" value={inputValue} onChange={handleChange} />
      <button onClick={handleClick}>Click Me</button>
    </div>
  );
};

export default InteractiveComponent;

// PATTERN: React-Specific TypeScript

import React, { useState } from 'react';

const Counter: React.FC = () => {
  const [count, setCount] = useState(0); // Type inferred as number
  const [message, setMessage] = useState('Hello'); // Type inferred as string

  return (
    <div>
      <p>Count: {count}</p>
      <p>Message: {message}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
};

export default Counter;

// PATTERN: React-Specific TypeScript

import React, { useState } from 'react';

interface User {
  id: number;
  name: string;
}

const UserProfile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [items, setItems] = useState<string[]>([]);

  const fetchUser = () => {
    setUser({ id: 1, name: 'Alice' });
    setItems(['apple', 'banana']);
  };

  return (
    <div>
      <button onClick={fetchUser}>Load User</button>
      {user && <p>User: {user.name}</p>}
      {items.length > 0 && <p>Items: {items.join(', ')}</p>}
    </div>
  );
};

export default UserProfile;

// PATTERN: React-Specific TypeScript

import React, { useRef } from 'react';

const FocusInput: React.FC = () => {
  const inputRef = useRef<HTMLInputElement>(null);
  const timerId = useRef<NodeJS.Timeout | null>(null);

  const handleFocus = () => {
    inputRef.current?.focus();
  };

  return (
    <div>
      <input type="text" ref={inputRef} />
      <button onClick={handleFocus}>Focus Input</button>
    </div>
  );
};

export default FocusInput;

// PATTERN: React-Specific TypeScript

import React, { useState, useEffect } from 'react';

const DataFetcher: React.FC = () => {
  const [userId, setUserId] = useState<number>(1);
  const [data, setData] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      // Simulate API call
      const response = await new Promise<string>(resolve =>
        setTimeout(() => resolve(`Data for user ${userId}`), 500)
      );
      setData(response);
    };

    fetchData();
  }, [userId]); // userId is correctly typed as number

  return (
    <div>
      <p>{data}</p>
      <button onClick={() => setUserId(prev => prev + 1)}>Next User</button>
    </div>
  );
};

export default DataFetcher;

// PATTERN: React-Specific TypeScript

import { useState, useCallback } from 'react';

interface CounterControls {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

function useCounter(initialValue: number = 0): CounterControls {
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => setCount(prev => prev + 1), []);
  const decrement = useCallback(() => setCount(prev => prev - 1), []);
  const reset = useCallback(() => setCount(initialValue), [initialValue]);

  return { count, increment, decrement, reset };
}

export default useCounter;

// PATTERN: React-Specific TypeScript

import React, { createContext, useState, useContext, ReactNode } from 'react';

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// PATTERN: React-Specific TypeScript

import React, { forwardRef, InputHTMLAttributes } from 'react';

interface CustomInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

const CustomInput = forwardRef<HTMLInputElement, CustomInputProps>(
  ({ label, ...props }, ref) => {
    return (
      <div>
        <label>{label}</label>
        <input ref={ref} {...props} />
      </div>
    );
  }
);

export default CustomInput;