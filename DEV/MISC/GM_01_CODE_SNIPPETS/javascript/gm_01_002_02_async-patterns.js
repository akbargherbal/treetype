// PATTERN: Async Patterns

const fetchData = new Promise((resolve, reject) => {
  const success = true; // Simulate an operation
  if (success) {
    setTimeout(() => resolve("Data fetched successfully!"), 100);
  } else {
    setTimeout(() => reject("Failed to fetch data."), 100);
  }
});

fetchData.then(message => console.log(message));

// PATTERN: Async Patterns

const fetchUserData = () => Promise.resolve({ id: 1, name: "Alice" });
const fetchUserPosts = (userId) => Promise.resolve([`Post ${userId}-1`, `Post ${userId}-2`]);

fetchUserData()
  .then(user => {
    console.log("User:", user.name);
    return fetchUserPosts(user.id);
  })
  .then(posts => {
    console.log("Posts:", posts);
    return posts.length;
  })
  .then(postCount => console.log("Total posts:", postCount));

// PATTERN: Async Patterns

const performOperation = (shouldSucceed) => new Promise((resolve, reject) => {
  if (shouldSucceed) {
    resolve("Operation completed.");
  } else {
    reject(new Error("Operation failed!"));
  }
});

performOperation(false)
  .then(result => console.log(result))
  .catch(error => console.error("Caught error:", error.message));

performOperation(true)
  .then(result => console.log(result))
  .catch(error => console.error("This won't be called:", error.message));

// PATTERN: Async Patterns

const processData = (shouldSucceed) => new Promise((resolve, reject) => {
  setTimeout(() => shouldSucceed ? resolve("Data processed.") : reject(new Error("Processing failed.")), 100);
});

processData(true)
  .then(result => console.log(result))
  .catch(error => console.error(error.message))
  .finally(() => console.log("Cleanup: Data processing finished."));

// PATTERN: Async Patterns

const simulateFetch = (data, delay = 100) => {
  return new Promise(resolve => setTimeout(() => resolve(data), delay));
};

async function getUserData() {
  console.log("Fetching user...");
  const user = await simulateFetch({ id: 1, name: "Jane Doe" });
  console.log("User fetched:", user.name);

  console.log("Fetching user details...");
  const details = await simulateFetch({ email: "jane@example.com" });
  console.log("Details fetched:", details.email);
  return { ...user, ...details };
}

getUserData().then(data => console.log("Combined data:", data));

// PATTERN: Async Patterns

const simulateFailedFetch = (shouldFail) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (shouldFail) {
        reject(new Error("Network error!"));
      } else {
        resolve("Data received.");
      }
    }, 100);
  });
};

async function fetchDataWithErrorHandling() {
  try {
    console.log("Attempting to fetch data...");
    const data = await simulateFailedFetch(true);
    console.log(data);
  } catch (error) {
    console.error("Error during fetch:", error.message);
  } finally {
    console.log("Fetch attempt finished.");
  }
}

fetchDataWithErrorHandling();

// PATTERN: Async Patterns

const fetchResource = (name, delay) => {
  return new Promise(resolve => {
    setTimeout(() => resolve(`${name} fetched`), delay);
  });
};

const promise1 = fetchResource("User data", 200);
const promise2 = fetchResource("Product list", 100);
const promise3 = fetchResource("Order history", 300);

Promise.all([promise1, promise2, promise3])
  .then(results => {
    console.log("All resources fetched:", results);
  })
  .catch(error => {
    console.error("One of the fetches failed:", error.message);
  });

// PATTERN: Async Patterns

const fetchFast = (data, delay) => new Promise(resolve => setTimeout(() => resolve(data), delay));
const fetchSlow = (data, delay) => new Promise(resolve => setTimeout(() => resolve(data), delay));

Promise.race([
  fetchFast("Fast data", 50),
  fetchSlow("Slow data", 200)
])
  .then(result => console.log("First to resolve:", result))
  .catch(error => console.error("First to reject:", error));

// PATTERN: Async Patterns

const promiseSuccess = Promise.resolve("Success!");
const promiseFailure = Promise.reject(new Error("Failed!"));
const promisePending = new Promise(resolve => setTimeout(() => resolve("Pending resolved"), 100));

Promise.allSettled([promiseSuccess, promiseFailure, promisePending])
  .then(results => {
    results.forEach(result => {
      if (result.status === "fulfilled") {
        console.log(`Fulfilled: ${result.value}`);
      } else {
        console.error(`Rejected: ${result.reason.message}`);
      }
    });
  });

// PATTERN: Async Patterns

const fetchUser = (id) => Promise.resolve({ id: id, name: `User ${id}` });
const fetchOrders = (id) => Promise.resolve([`Order ${id}-A`, `Order ${id}-B`]);

const processUserRequest = async (userId) => {
  try {
    const [user, orders] = await Promise.all([fetchUser(userId), fetchOrders(userId)]);
    console.log(`User: ${user.name}, Orders: ${orders.join(", ")}`);
  } catch (error) {
    console.error("Error processing request:", error.message);
  }
};

processUserRequest(123);

// PATTERN: Async Patterns

const fetchItemDetails = async (itemId) => {
  return new Promise(resolve => {
    setTimeout(() => resolve({ id: itemId, price: itemId * 10 }), 50 * itemId);
  });
};

async function processItems(itemIds) {
  const itemDetailPromises = itemIds.map(id => fetchItemDetails(id));
  const allDetails = await Promise.all(itemDetailPromises);
  console.log("All item details fetched:", allDetails);
  return allDetails;
}

processItems([1, 2, 3]);