// PATTERN: Zustand (State Management)

import { create } from 'zustand';

const useCounterStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));

export default useCounterStore;

// PATTERN: Zustand (State Management)

import useCounterStore from './store/counterStore'; // Assuming path

function CounterDisplay() {
  const count = useCounterStore((state) => state.count);

  return (
    <div>
      <p>Current Count: {count}</p>
    </div>
  );
}

export default CounterDisplay;

// PATTERN: Zustand (State Management)

import useCounterStore from './store/counterStore'; // Assuming path

function CounterControls() {
  const increment = useCounterStore((state) => state.increment);
  const decrement = useCounterStore((state) => state.decrement);

  return (
    <div>
      <button onClick={increment}>Increment</button>
      <button onClick={decrement}>Decrement</button>
    </div>
  );
}

export default CounterControls;

// PATTERN: Zustand (State Management)

import { create } from 'zustand';

const useTodoStore = create((set, get) => ({
  todos: [
    { id: 1, text: 'Learn Zustand', completed: true },
    { id: 2, text: 'Build a project', completed: false },
  ],
  addTodo: (text) => set((state) => ({
    todos: [...state.todos, { id: Date.now(), text, completed: false }],
  })),
  getCompletedCount: () => get().todos.filter(todo => todo.completed).length,
}));

export default useTodoStore;

// PATTERN: Zustand (State Management)

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useUserStore = create(
  persist(
    (set) => ({
      username: 'Guest',
      email: '',
      login: (name, email) => set({ username: name, email: email }),
      logout: () => set({ username: 'Guest', email: '' }),
    }),
    {
      name: 'user-storage', // unique name for local storage
    }
  )
);

export default useUserStore;