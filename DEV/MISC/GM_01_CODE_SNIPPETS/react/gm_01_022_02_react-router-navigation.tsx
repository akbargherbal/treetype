// PATTERN: React Router (Navigation)

import { createBrowserRouter, RouterProvider } from 'react-router-dom';

const HomePage = () => <div>Welcome Home!</div>;
const AboutPage = () => <div>About Us Page</div>;

const router = createBrowserRouter([
  { path: '/', element: <HomePage /> },
  { path: '/about', element: <AboutPage /> },
]);

function App() {
  return <RouterProvider router={router} />;
}

// PATTERN: React Router (Navigation)

import { Link } from 'react-router-dom';

function NavigationMenu() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/products">Products</Link>
      <Link to="/contact">Contact</Link>
    </nav>
  );
}

// PATTERN: React Router (Navigation)

import { useNavigate } from 'react-router-dom';

function ProductDetail() {
  const navigate = useNavigate();

  const handleGoBack = () => {
    navigate(-1); // Go back one step in history
  };

  const handleGoToCheckout = () => {
    navigate('/checkout', { state: { fromProduct: true } });
  };

  return (
    <div>
      <h1>Product Details</h1>
      <button onClick={handleGoBack}>Back to Products</button>
      <button onClick={handleGoToCheckout}>Proceed to Checkout</button>
    </div>
  );
}

// PATTERN: React Router (Navigation)

import { useParams } from 'react-router-dom';

function UserProfile() {
  const { userId } = useParams(); // Assumes route like /users/:userId

  return (
    <div>
      <h2>User Profile</h2>
      <p>Displaying profile for User ID: {userId}</p>
    </div>
  );
}

// PATTERN: React Router (Navigation)

import { useSearchParams } from 'react-router-dom';

function ProductSearch() {
  const [searchParams, setSearchParams] = useSearchParams();
  const category = searchParams.get('category') || 'all';

  const handleFilterChange = (newCategory) => {
    setSearchParams({ category: newCategory, page: '1' });
  };

  return (
    <div>
      <h2>Products in: {category}</h2>
      <button onClick={() => handleFilterChange('electronics')}>Electronics</button>
      <button onClick={() => handleFilterChange('books')}>Books</button>
    </div>
  );
}

// PATTERN: React Router (Navigation)

import { createBrowserRouter, RouterProvider, redirect } from 'react-router-dom';

const isAuthenticated = () => false; // Simulate authentication status
const DashboardPage = () => <div>Welcome to your Dashboard!</div>;
const LoginPage = () => <div>Please log in to access the dashboard.</div>;

const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    path: '/dashboard',
    element: <DashboardPage />,
    loader: () => {
      if (!isAuthenticated()) {
        return redirect('/login');
      }
      return null; // Allow access
    },
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

// PATTERN: React Router (Navigation)

import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';

const DashboardLayout = () => (
  <div>
    <nav>Dashboard Nav | <a href="/dashboard/profile">Profile</a> | <a href="/dashboard/settings">Settings</a></nav>
    <hr />
    <Outlet /> {/* Renders child routes */}
  </div>
);
const DashboardOverview = () => <h3>Dashboard Overview</h3>;
const UserProfile = () => <h3>User Profile Settings</h3>;
const AppSettings = () => <h3>Application Settings</h3>;

const router = createBrowserRouter([
  {
    path: '/dashboard',
    element: <DashboardLayout />,
    children: [
      { index: true, element: <DashboardOverview /> },
      { path: 'profile', element: <UserProfile /> },
      { path: 'settings', element: <AppSettings /> },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}