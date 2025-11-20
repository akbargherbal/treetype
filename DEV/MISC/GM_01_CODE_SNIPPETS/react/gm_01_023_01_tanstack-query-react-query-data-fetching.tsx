// PATTERN: TanStack Query / React Query (Data Fetching)

import { useQuery } from '@tanstack/react-query';

const fetchTodos = async () => {
  const res = await fetch('/api/todos');
  return res.json();
};

function TodosList() {
  const { data, isLoading, error } = useQuery({ queryKey: ['todos'], queryFn: fetchTodos });

  if (isLoading) return <div>Loading todos...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {data.map(todo => <li key={todo.id}>{todo.title}</li>)}
    </ul>
  );
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import { useQuery } from '@tanstack/react-query';

const fetchTodoById = async (todoId) => {
  const res = await fetch(`/api/todos/${todoId}`);
  return res.json();
};

function TodoDetail({ todoId }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['todo', todoId],
    queryFn: () => fetchTodoById(todoId),
  });

  if (isLoading) return <div>Loading todo...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>{data.title}</div>;
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import { useMutation } from '@tanstack/react-query';

const createTodo = async (newTodo) => {
  const res = await fetch('/api/todos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newTodo),
  });
  return res.json();
};

function AddTodoForm() {
  const mutation = useMutation({ mutationFn: createTodo });

  const handleSubmit = (event) => {
    event.preventDefault();
    mutation.mutate({ title: 'New Task', completed: false });
  };

  return (
    <form onSubmit={handleSubmit}>
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Adding...' : 'Add Todo'}
      </button>
      {mutation.isError && <div>Error: {mutation.error.message}</div>}
      {mutation.isSuccess && <div>Todo added!</div>}
    </form>
  );
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import { useMutation, useQueryClient } from '@tanstack/react-query';

const addTodo = async (newTodo) => {
  const res = await fetch('/api/todos', { method: 'POST', body: JSON.stringify(newTodo) });
  return res.json();
};

function AddTodoButton() {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: addTodo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  return (
    <button onClick={() => mutation.mutate({ title: 'New Item' })} disabled={mutation.isPending}>
      Add Todo
    </button>
  );
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import { useQuery } from '@tanstack/react-query';

const fetchUsers = async () => {
  const res = await fetch('/api/users');
  return res.json();
};

function UsersList() {
  const { data, isLoading, isError, error } = useQuery({ queryKey: ['users'], queryFn: fetchUsers });

  if (isLoading) {
    return <div>Loading users...</div>;
  }

  if (isError) {
    return <div>An error occurred: {error.message}</div>;
  }

  return (
    <ul>
      {data.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  );
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import { useQuery } from '@tanstack/react-query';

const fetchUserDetails = async (userId) => {
  const res = await fetch(`/api/users/${userId}`);
  return res.json();
};

function UserProfile({ userId }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUserDetails(userId),
    enabled: !!userId, // Only run query if userId is truthy
  });

  if (!userId) return <div>Select a user to view details.</div>;
  if (isLoading) return <div>Loading user profile...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>User: {data.name}</div>;
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      {/* Your application components go here */}
      <div>Hello TanStack Query!</div>
    </QueryClientProvider>
  );
}

export default App;