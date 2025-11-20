// PATTERN: API/Data Patterns

interface Product {
  id: string;
  name: string;
  price: number;
  available: boolean;
}

interface ApiResponse<T> {
  status: 'success' | 'error';
  data: T;
  message?: string;
}

type ProductListResponse = ApiResponse<Product[]>;

const response: ProductListResponse = {
  status: 'success',
  data: [{ id: 'p1', name: 'Laptop', price: 1200, available: true }],
};

// PATTERN: API/Data Patterns

interface CreateProductPayload {
  name: string;
  description: string;
  price: number;
  categoryId: string;
}

const newProduct: CreateProductPayload = {
  name: "Wireless Mouse",
  description: "Ergonomic wireless mouse",
  price: 29.99,
  categoryId: "CAT-123",
};

// Example usage (conceptual)
// await api.post('/products', newProduct);

// PATTERN: API/Data Patterns

enum OrderStatus {
  Pending = "PENDING",
  Processing = "PROCESSING",
  Shipped = "SHIPPED",
  Delivered = "DELIVERED",
  Cancelled = "CANCELLED",
}

const currentStatus: OrderStatus = OrderStatus.Processing;

if (currentStatus === OrderStatus.Delivered) {
  console.log("Order has been delivered.");
} else {
  console.log(`Order is currently ${currentStatus}.`);
}

// PATTERN: API/Data Patterns

const API_ENDPOINTS = {
  PRODUCTS: "/api/products",
  USERS: "/api/users",
  ORDERS: "/api/orders",
} as const;

type ApiEndpoint = typeof API_ENDPOINTS[keyof typeof API_ENDPOINTS];

const endpoint: ApiEndpoint = API_ENDPOINTS.PRODUCTS;

// endpoint = "/api/settings"; // Error: Type '"/api/settings"' is not assignable to type '"/api/products" | "/api/users" | "/api/orders"'.

// PATTERN: API/Data Patterns

interface UserSchemaType {
  id: string;
  username: string;
  email: string;
  isActive: boolean;
  roles: string[];
}

const newUser: UserSchemaType = {
  id: "usr_123",
  username: "john_doe",
  email: "john.doe@example.com",
  isActive: true,
  roles: ["admin", "editor"],
};

const anotherUser: UserSchemaType = {
  id: "usr_456",
  username: "jane_smith",
  email: "jane.smith@example.com",
  isActive: false,
  roles: ["viewer"],
};

// PATTERN: API/Data Patterns

import { z } from 'zod';

const ProductSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(3).max(255),
  price: z.number().positive(),
  description: z.string().optional(),
  createdAt: z.string().datetime(),
});

type Product = z.infer<typeof ProductSchema>;

const productData: Product = {
  id: "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  name: "Laptop Pro",
  price: 1200.00,
  createdAt: "2023-10-27T10:00:00Z",
};

// const invalidProduct: Product = { id: "123", name: "A", price: -1 }; // Zod validation would fail

// PATTERN: API/Data Patterns

import axios, { AxiosResponse } from 'axios';

interface User {
  id: number;
  name: string;
  email: string;
}

async function fetchUser(userId: number): Promise<User> {
  const response: AxiosResponse<User> = await axios.get(`/api/users/${userId}`);
  return response.data;
}

fetchUser(1).then(user => console.log(`Fetched user: ${user.name}`));
// .catch(error => console.error("Error fetching user:", error));

// PATTERN: API/Data Patterns

interface Post {
  userId: number;
  id: number;
  title: string;
  body: string;
}

async function fetchPosts(): Promise<Post[]> {
  const response = await fetch('https://jsonplaceholder.typicode.com/posts');
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const data: Post[] = await response.json();
  return data;
}

fetchPosts().then(posts => console.log(`Fetched ${posts.length} posts.`));
// .catch(error => console.error("Error fetching posts:", error));