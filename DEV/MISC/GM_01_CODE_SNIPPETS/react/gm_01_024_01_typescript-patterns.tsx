// PATTERN: TypeScript Patterns

interface UserProfileProps {
  userName: string;
  userAge: number;
}

const UserProfile: React.FC<UserProfileProps> = ({ userName, userAge }) => {
  return (
    <div>
      <h2>{userName}</h2>
      <p>Age: {userAge}</p>
    </div>
  );
};

// PATTERN: TypeScript Patterns

import React, { useState } from 'react';

const NameInput: React.FC = () => {
  const [name, setName] = useState<string>('');

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setName(event.target.value);
  };

  return (
    <div>
      <input type="text" value={name} onChange={handleChange} placeholder="Enter your name" />
      <p>Hello, {name || 'Guest'}!</p>
    </div>
  );
};

// PATTERN: TypeScript Patterns

import { useState } from 'react';

interface UserProfile {
  id: number;
  name: string;
  email: string;
}

const UserDisplay = () => {
  const [user, setUser] = useState<UserProfile | null>(null);

  // Example: setUser({ id: 1, name: 'Jane Doe', email: 'jane@example.com' });

  return (
    <div>
      {user ? <p>{user.name} ({user.email})</p> : <p>Loading user...</p>}
    </div>
  );
};