// PATTERN: Module Patterns

const shoppingCart = (() => {
  let items = []; // Private variable

  const addItem = (item) => {
    items.push(item);
    return `${item.name} added.`;
  };

  const getItems = () => {
    return [...items]; // Return a copy to prevent external modification
  };

  const getTotal = () => {
    return items.reduce((sum, item) => sum + item.price, 0);
  };

  return {
    addItem,
    getItems,
    getTotal
  };
})();

// PATTERN: Module Patterns

const Logger = (() => {
  let instance;
  let logs = []; // Private state

  function init() {
    // Private methods and properties
    const logMessage = (message) => {
      const timestamp = new Date().toISOString();
      logs.push(`${timestamp}: ${message}`);
      console.log(`LOG: ${message}`);
    };

    const getLogs = () => [...logs];

    return {
      log: logMessage,
      getLogs: getLogs
    };
  }

  return {
    getInstance: () => {
      if (!instance) {
        instance = init();
      }
      return instance;
    }
  };
})();

// PATTERN: Module Patterns

const createProduct = (name, price, category) => {
  return {
    id: Math.random().toString(36).substr(2, 9),
    name,
    price,
    category,
    displayInfo() {
      return `${this.name} (${this.category}) - $${this.price.toFixed(2)}`;
    }
  };
};