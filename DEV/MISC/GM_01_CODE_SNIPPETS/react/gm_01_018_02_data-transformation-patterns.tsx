// PATTERN: Data Transformation Patterns

import React from 'react';

const products = [
  { id: 1, name: 'Laptop', category: 'Electronics', price: 1200 },
  { id: 2, name: 'Keyboard', category: 'Electronics', price: 75 },
  { id: 3, name: 'Desk Chair', category: 'Furniture', price: 300 },
];

function ProductList({ categoryFilter }) {
  const filteredAndMappedProducts = products
    .filter(product => product.category === categoryFilter)
    .map(product => ({ name: product.name, displayPrice: `$${product.price}` }));

  return (
    <ul>
      {filteredAndMappedProducts.map((p, index) => (
        <li key={index}>{p.name} - {p.displayPrice}</li>
      ))}
    </ul>
  );
}

// PATTERN: Data Transformation Patterns

import React from 'react';

const tasks = [
  { id: 1, name: 'Buy groceries', status: 'pending' },
  { id: 2, name: 'Finish report', status: 'completed' },
  { id: 3, name: 'Call client', status: 'pending' },
];

function TaskGroups() {
  const groupedTasks = tasks.reduce((acc, task) => {
    (acc[task.status] = acc[task.status] || []).push(task);
    return acc;
  }, {});

  return (
    <div>
      {Object.entries(groupedTasks).map(([status, taskList]) => (
        <div key={status}>
          <h3>{status.toUpperCase()}</h3>
          <ul>{taskList.map(task => <li key={task.id}>{task.name}</li>)}</ul>
        </div>
      ))}
    </div>
  );
}

// PATTERN: Data Transformation Patterns

import React, { useState } from 'react';

const initialUsers = [
  { id: 1, name: 'Alice', age: 30 },
  { id: 2, name: 'Bob', age: 25 },
  { id: 3, name: 'Charlie', age: 35 },
];

function UserSorter() {
  const [users] = useState(initialUsers);
  const sortedUsers = [...users].sort((a, b) => a.age - b.age);

  return (
    <ul>
      {sortedUsers.map(user => (
        <li key={user.id}>{user.name} ({user.age})</li>
      ))}
    </ul>
  );
}

// PATTERN: Data Transformation Patterns

import React from 'react';

const productTags = ['electronics', 'gadgets', 'home', 'electronics', 'kitchen', 'gadgets'];

function UniqueTagsDisplay() {
  const uniqueTags = [...new Set(productTags)];

  return (
    <div>
      <h3>Available Tags:</h3>
      <ul>
        {uniqueTags.map(tag => <li key={tag}>{tag}</li>)}
      </ul>
    </div>
  );
}

// PATTERN: Data Transformation Patterns

import React from 'react';

function UserProfile({ name, email, age }) {
  return (
    <div>
      <h2>{name}</h2>
      <p>Email: {email}</p>
      <p>Age: {age}</p>
    </div>
  );
}

// PATTERN: Data Transformation Patterns

import React, { useState } from 'react';

function UserEditor() {
  const [user, setUser] = useState({ name: 'John Doe', email: 'john@example.com', age: 30 });

  const updateAge = () => {
    setUser(prevUser => ({ ...prevUser, age: prevUser.age + 1 }));
  };

  return (
    <div>
      <p>Name: {user.name}</p>
      <p>Age: {user.age}</p>
      <button onClick={updateAge}>Increase Age</button>
    </div>
  );
}