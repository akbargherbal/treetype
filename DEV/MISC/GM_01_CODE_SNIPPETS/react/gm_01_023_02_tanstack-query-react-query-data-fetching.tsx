// PATTERN: TanStack Query / React Query (Data Fetching)

import { useQuery } from '@tanstack/react-query';

async function fetchProducts() {
  const response = await fetch('/api/products');
  if (!response.ok) throw new Error('Failed to fetch products');
  return response.json();
}

function ProductList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
  });

  if (isLoading) return <div>Loading products...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {data.map(product => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  );
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import { useQuery } from '@tanstack/react-query';

async function fetchProductById(productId) {
  const response = await fetch(`/api/products/${productId}`);
  if (!response.ok) throw new Error('Failed to fetch product');
  return response.json();
}

function ProductDetail({ productId }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['product', productId],
    queryFn: () => fetchProductById(productId),
  });

  if (isLoading) return <div>Loading product...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>Product: {data.name}</div>;
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import { useMutation } from '@tanstack/react-query';

async function createProduct(newProduct) {
  const response = await fetch('/api/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newProduct),
  });
  if (!response.ok) throw new Error('Failed to create product');
  return response.json();
}

function CreateProductForm() {
  const mutation = useMutation({
    mutationFn: createProduct,
    onSuccess: () => alert('Product created!'),
    onError: (error) => alert(`Error: ${error.message}`),
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate({ name: 'New Gadget', price: 99.99 });
  };

  return (
    <form onSubmit={handleSubmit}>
      <button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? 'Creating...' : 'Create Product'}
      </button>
    </form>
  );
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import { useMutation, useQueryClient } from '@tanstack/react-query';

async function addProduct(newProduct) {
  const response = await fetch('/api/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newProduct),
  });
  if (!response.ok) throw new Error('Failed to add product');
  return response.json();
}

function AddProductButton() {
  const queryClient = useQueryClient();
  const mutation = useMutation({
    mutationFn: addProduct,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });

  return (
    <button onClick={() => mutation.mutate({ name: 'New Item' })}>
      Add Product
    </button>
  );
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import { useQuery } from '@tanstack/react-query';

async function fetchUsers() {
  const response = await fetch('/api/users');
  if (!response.ok) throw new Error('Failed to fetch users');
  return response.json();
}

function UserList() {
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  if (isLoading) return <div>Loading users...</div>;
  if (isError) return <div>An error occurred: {error.message}</div>;

  return (
    <ul>
      {data.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import { useQuery } from '@tanstack/react-query';

async function fetchUserDetails(userId) {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) throw new Error('Failed to fetch user details');
  return response.json();
}

function UserProfile({ userId }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['userProfile', userId],
    queryFn: () => fetchUserDetails(userId),
    enabled: !!userId, // Only run if userId is truthy
  });

  if (!userId) return <div>Select a user to view details.</div>;
  if (isLoading) return <div>Loading user profile...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>User: {data.name}, Email: {data.email}</div>;
}

// PATTERN: TanStack Query / React Query (Data Fetching)

import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      {/* Your application components go here */}
      <MyComponent />
    </QueryClientProvider>
  );
}

function MyComponent() {
  return <div>Application content</div>;
}