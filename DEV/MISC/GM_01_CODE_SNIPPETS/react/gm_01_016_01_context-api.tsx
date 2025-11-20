// PATTERN: Context API

import React, { useState } from 'react';

export const AuthContext = React.createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // e.g., { name: 'Jane Doe', id: 'user123' }

  const authContextValue = {
    user,
    login: (userData) => setUser(userData),
    logout: () => setUser(null),
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// PATTERN: Context API

import React, { useContext } from 'react';
import { AuthContext } from './AuthContext'; // Assuming AuthContext is defined here

const UserProfile = () => {
  const { user, logout } = useContext(AuthContext);

  if (!user) {
    return <p>Please log in to view your profile.</p>;
  }

  return (
    <div>
      <h3>Welcome, {user.name}!</h3>
      <p>User ID: {user.id}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

export default UserProfile;