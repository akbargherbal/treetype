# Firebase Crash Course for TreeType: From GitHub Pages to Professional Platform

## Table of Contents

---

## Part 1: Foundation & Setup (2-3 hours)

### 1.1 Firebase Fundamentals

- **What Firebase Actually Is** (15 min)

  - Backend-as-a-Service (BaaS) overview
  - Which Firebase services TreeType needs vs nice-to-haves
  - Pricing: Free tier limits and when you'd need to pay
  - Firebase vs traditional backend: When to use what

- **Firebase + Static Sites Architecture** (20 min)
  - How Firebase complements your static site (not replaces it)
  - Client SDK vs Admin SDK: What you'll use
  - Security model: Client-side rules (not Python middleware)
  - Your mental model: Firebase is your database + auth + storage API

### 1.2 Project Setup (30 min)

- **Console Setup** (10 min)

  - Creating a Firebase project
  - Connecting to your existing GitHub repo
  - Understanding the Firebase console layout

- **Local Development Setup** (20 min)
  - Installing Firebase CLI: `npm install -g firebase-tools`
  - `firebase login` and `firebase init`
  - Project structure: What files Firebase creates
  - **Critical**: Firebase Hosting vs GitHub Pages (you can use both)

### 1.3 First Deployment (45 min)

- **Firebase Hosting Basics** (20 min)

  - `firebase.json` configuration
  - Deploying your existing Vite build: `firebase deploy --only hosting`
  - Custom domain setup (if desired)
  - Preview channels for testing

- **Hands-On Exercise** (25 min)
  - Deploy current TreeType to Firebase Hosting
  - Verify it works identically to GitHub Pages
  - Set up automatic deploys via GitHub Actions
  - **Goal**: Prove Firebase won't break your existing setup

---

## Part 2: Core Firebase Services for TreeType (3-4 hours)

### 2.1 Firestore Database (90 min)

**Why you need this**: User progress tracking, leaderboards, custom snippets

- **Firestore Mental Model** (20 min)

  - NoSQL structure: Collections → Documents → Fields
  - Real-time listeners vs one-time reads
  - Thinking in documents: How to model TreeType data
  - Security rules: Client-side permissions (not server middleware)

- **Data Modeling for TreeType** (30 min)

  ```
  users/{userId}/
    - profile: { displayName, createdAt, totalTests }
    - testResults/{testId}: { snippetId, wpm, accuracy, mode, timestamp }
    - customSnippets/{snippetId}: { name, language, tokens, ... }

  leaderboards/
    - daily/{date}: { entries: [{userId, wpm, accuracy}] }
    - allTime/global: { ... }

  sharedSnippets/{snippetId}: { authorId, name, upvotes, ... }
  ```

  - Why this structure (optimized for your queries)
  - Denormalization: When to duplicate data
  - Subcollections vs root collections

- **CRUD Operations** (40 min)

  ```typescript
  // Read user's test history
  const q = query(
    collection(db, `users/${userId}/testResults`),
    orderBy("timestamp", "desc"),
    limit(10)
  );

  // Write new test result
  await addDoc(collection(db, `users/${userId}/testResults`), {
    snippetId: "python-sample-1",
    wpm: 65,
    accuracy: 97.5,
    mode: "standard",
    timestamp: serverTimestamp(),
  });

  // Real-time leaderboard listener
  onSnapshot(doc(db, "leaderboards/daily", todayDate), (snapshot) => {
    updateLeaderboardUI(snapshot.data());
  });
  ```

  - **Hands-On**: Add "Save Progress" button to TreeType
  - Error handling patterns
  - Offline persistence (built-in!)

### 2.2 Authentication (60 min)

**Why you need this**: Link test results to users, enable sharing

- **Auth Methods Comparison** (15 min)

  - Anonymous auth (easiest start - just get a userId)
  - Email/password (standard)
  - Google OAuth (recommended for TreeType)
  - GitHub OAuth (fits your audience)
  - **Decision framework**: Start anonymous, add OAuth later

- **Implementation** (30 min)

  ```typescript
  // Anonymous auth (perfect for MVP)
  const { user } = await signInAnonymously(auth);

  // Later: Link to permanent account
  const credential = GoogleAuthProvider.credential(idToken);
  await linkWithCredential(auth.currentUser, credential);

  // Auth state listener (essential)
  onAuthStateChanged(auth, (user) => {
    if (user) {
      // User signed in, load their data
      loadUserProgress(user.uid);
    } else {
      // Show guest mode
      showGuestUI();
    }
  });
  ```

- **Security Rules** (15 min)

  ```javascript
  // Firestore security rules
  match /users/{userId} {
    allow read: if request.auth != null;
    allow write: if request.auth.uid == userId;
  }

  match /users/{userId}/testResults/{testId} {
    allow read, write: if request.auth.uid == userId;
  }
  ```

  - **Critical Python Dev Note**: These run in Google's servers, not your code
  - Testing rules in the Firebase console
  - Common security mistakes to avoid

### 2.3 Cloud Storage (45 min)

**Why you need this**: User-uploaded snippets, avatar images

- **Storage Basics** (15 min)

  - Storage structure: Buckets → Paths
  - vs Firestore: When to use which
  - Security rules for storage (similar to Firestore)

- **Implementation** (30 min)

  ```typescript
  // Upload user's custom snippet
  const snippetRef = ref(storage, `users/${userId}/snippets/${snippetId}.json`);
  await uploadString(snippetRef, JSON.stringify(snippetData), 'raw', {
    contentType: 'application/json'
  });

  // Get download URL
  const url = await getDownloadURL(snippetRef);

  // Security rule
  match /users/{userId}/snippets/{allPaths=**} {
    allow read: if request.auth != null;
    allow write: if request.auth.uid == userId && request.resource.size < 5 * 1024 * 1024;
  }
  ```

  - **Hands-On**: Add "Upload Custom Snippet" feature

---

## Part 3: Advanced Features (2-3 hours)

### 3.1 Cloud Functions (Optional but Powerful) (90 min)

**Why you'd use this**: Server-side logic (leaderboard updates, snippet validation)

- **Functions Mental Model** (20 min)

  - When you need backend code (rare, but sometimes necessary)
  - Triggers: HTTP, Firestore, Auth, Storage events
  - **Python Dev Translation**: Like AWS Lambda, but Firebase-integrated
  - Pricing: Free tier is generous (2M invocations/month)

- **Example Use Cases** (40 min)

  ```typescript
  // Validate uploaded snippet (server-side)
  export const validateSnippet = functions.storage
    .object()
    .onFinalize(async (object) => {
      const filePath = object.name;
      if (!filePath.endsWith(".json")) return;

      // Download, parse, validate
      const [file] = await storage.bucket().file(filePath).download();
      const snippet = JSON.parse(file.toString());

      // Check structure matches your schema
      if (!isValidSnippet(snippet)) {
        await storage.bucket().file(filePath).delete();
        throw new Error("Invalid snippet format");
      }

      // Update Firestore with metadata
      await db.collection("snippets").doc(snippetId).set({
        validated: true,
        totalLines: snippet.total_lines,
        language: snippet.language,
      });
    });

  // Calculate daily leaderboard (scheduled function)
  export const updateLeaderboard = functions.pubsub
    .schedule("0 0 * * *") // Midnight UTC
    .onRun(async () => {
      // Aggregate yesterday's test results
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);

      const results = await db
        .collection("testResults")
        .where("timestamp", ">=", yesterday)
        .orderBy("wpm", "desc")
        .limit(100)
        .get();

      // Write to leaderboard collection
      await db
        .collection("leaderboards")
        .doc(yesterday.toISOString().split("T")[0])
        .set({ entries: results.docs.map((d) => d.data()) });
    });
  ```

- **Deployment** (30 min)
  - Local emulator suite (test before deploying)
  - `firebase deploy --only functions`
  - Monitoring and logs in Firebase console
  - **Debugging**: How to test functions locally

### 3.2 Real-time Features (45 min)

**Use case**: Live leaderboards, collaborative snippet editing

- **Firestore Real-time Listeners** (30 min)

  ```typescript
  // Live leaderboard updates
  const unsubscribe = onSnapshot(
    doc(db, "leaderboards/daily", todayDate),
    (snapshot) => {
      const leaderboard = snapshot.data();
      updateLeaderboardUI(leaderboard.entries);
    },
    (error) => {
      console.error("Leaderboard update failed:", error);
    }
  );

  // Cleanup when component unmounts
  onBeforeUnmount(() => unsubscribe());
  ```

- **Performance Considerations** (15 min)
  - Real-time listeners cost (read per update)
  - When to use polling instead
  - Debouncing UI updates

### 3.3 Analytics (30 min)

**Use case**: Understand user behavior, optimize features

- **Firebase Analytics Setup** (10 min)

  - Automatic tracking (page views, app opens)
  - Custom events for TreeType

- **Custom Events** (20 min)

  ```typescript
  // Track typing test completion
  logEvent(analytics, "test_complete", {
    language: "python",
    mode: "standard",
    wpm: 65,
    accuracy: 97.5,
    snippet_length: 25,
  });

  // Track feature usage
  logEvent(analytics, "mode_changed", {
    from_mode: "minimal",
    to_mode: "standard",
  });

  // View in Firebase console
  // Debug with DebugView in development
  ```

---

## Part 4: Professional Patterns (2-3 hours)

### 4.1 Error Handling & Offline Support (60 min)

- **Firebase Error Patterns** (30 min)

  ```typescript
  // Network errors
  try {
    await setDoc(doc(db, "users", userId), userData);
  } catch (error) {
    if (error.code === "unavailable") {
      // Network offline
      showOfflineMessage();
    } else if (error.code === "permission-denied") {
      // Security rule rejection
      showAuthPrompt();
    } else {
      // Unexpected error
      logToSentry(error);
    }
  }

  // Optimistic updates
  const docRef = doc(db, "users", userId, "testResults", testId);
  updateTestResultUI(newResult); // Show immediately

  try {
    await setDoc(docRef, newResult);
  } catch (error) {
    revertTestResultUI(); // Rollback on failure
    showErrorToast();
  }
  ```

- **Offline Persistence** (30 min)

  ```typescript
  // Enable offline persistence (built-in!)
  enableIndexedDbPersistence(db).catch((err) => {
    if (err.code === "failed-precondition") {
      // Multiple tabs open
      console.warn("Persistence available in one tab only");
    }
  });

  // Works automatically:
  // - Writes queue when offline
  // - Reads from cache
  // - Syncs when online

  // Detect online/offline state
  onSnapshot(
    doc(db, "users", userId),
    { includeMetadataChanges: true },
    (snapshot) => {
      const fromCache = snapshot.metadata.fromCache;
      updateOnlineIndicator(!fromCache);
    }
  );
  ```

### 4.2 Performance Optimization (45 min)

- **Firestore Query Optimization** (25 min)

  ```typescript
  // BAD: Fetching all data
  const allResults = await getDocs(collection(db, "testResults"));
  const userResults = allResults.docs.filter((d) => d.data().userId === userId);

  // GOOD: Query with indexes
  const q = query(
    collection(db, "testResults"),
    where("userId", "==", userId),
    orderBy("timestamp", "desc"),
    limit(50)
  );
  const userResults = await getDocs(q);

  // Create composite indexes in Firebase console
  // Or let Firebase suggest them via error messages
  ```

- **Bundle Size Optimization** (20 min)

  ```typescript
  // Import only what you need (tree-shaking)
  import { doc, getDoc } from "firebase/firestore";
  // NOT: import firebase from 'firebase';

  // Lazy load Firebase modules
  const loadFirebase = async () => {
    const { initializeApp } = await import("firebase/app");
    const { getFirestore } = await import("firebase/firestore");
    // Initialize only when needed
  };

  // Result: ~50KB added to bundle (vs 300KB+ for full SDK)
  ```

### 4.3 Security Best Practices (30 min)

- **Security Rules Deep Dive** (20 min)

  ```javascript
  // Read your own data
  match /users/{userId} {
    allow read: if request.auth.uid == userId;
    allow write: if request.auth.uid == userId
                 && request.resource.data.keys().hasOnly(['displayName', 'avatarUrl'])
                 && request.resource.data.displayName is string
                 && request.resource.data.displayName.size() < 50;
  }

  // Read public leaderboards, but only Firebase can write
  match /leaderboards/{document=**} {
    allow read: if true;
    allow write: if false;  // Only Cloud Functions can write
  }

  // Rate limiting (prevent spam)
  match /users/{userId}/testResults/{testId} {
    allow create: if request.auth.uid == userId
                  && request.time > resource.data.lastSubmit + duration.value(1, 's');
  }
  ```

- **API Key Security** (10 min)
  - **Critical**: Firebase API keys are NOT secret (they're in your client bundle)
  - Security comes from Firestore rules, not hidden keys
  - Use Firebase App Check for abuse prevention
  - Environment variables for sensitive config (if using Cloud Functions)

### 4.4 Testing Firebase Features (45 min)

- **Local Emulator Suite** (25 min)

  ```bash
  # Start emulators
  firebase emulators:start

  # Emulates: Firestore, Auth, Functions, Storage
  # Runs locally, no cost, fast iteration
  ```

  ```typescript
  // Connect to emulators in dev
  if (import.meta.env.DEV) {
    connectFirestoreEmulator(db, "localhost", 8080);
    connectAuthEmulator(auth, "http://localhost:9099");
    connectStorageEmulator(storage, "localhost", 9199);
  }

  // Test with Vitest
  import { initializeTestEnvironment } from "@firebase/rules-unit-testing";

  describe("Security Rules", () => {
    it("allows users to read their own data", async () => {
      const testEnv = await initializeTestEnvironment({
        projectId: "treetype-test",
        firestore: { rules: fs.readFileSync("firestore.rules", "utf8") },
      });

      const alice = testEnv.authenticatedContext("alice");
      await assertSucceeds(getDoc(doc(alice.firestore(), "users/alice")));
    });
  });
  ```

- **Integration Testing** (20 min)
  - Testing Firebase features in your app
  - Mocking Firebase SDK for faster tests
  - Using emulators in CI/CD

---

## Part 5: TreeType-Specific Implementation Plan (1-2 hours)

### 5.1 Phase 1: Add User Progress Tracking (MVP)

**Goal**: Save test results without requiring login

```typescript
// features/progress-tracking.ts
export async function saveTestResult(result: TestResult) {
  // Use anonymous auth to get userId
  if (!auth.currentUser) {
    await signInAnonymously(auth);
  }

  const userId = auth.currentUser.uid;
  await addDoc(collection(db, `users/${userId}/testResults`), {
    ...result,
    timestamp: serverTimestamp(),
  });
}

export async function loadTestHistory() {
  const userId = auth.currentUser?.uid;
  if (!userId) return [];

  const q = query(
    collection(db, `users/${userId}/testResults`),
    orderBy("timestamp", "desc"),
    limit(20)
  );

  const snapshot = await getDocs(q);
  return snapshot.docs.map((d) => ({ id: d.id, ...d.data() }));
}
```

**UI Changes**:

- "View History" button in header
- Modal showing past test results (table/cards)
- Stats: Average WPM, accuracy trend, favorite language

**Time Estimate**: 4-6 hours

---

### 5.2 Phase 2: Leaderboards

**Goal**: Daily and all-time top performers

```typescript
// features/leaderboard.ts
export async function submitToLeaderboard(result: TestResult) {
  const userId = auth.currentUser.uid;
  const todayDate = new Date().toISOString().split("T")[0];

  // Submit to daily leaderboard
  const leaderboardRef = doc(db, "leaderboards/daily", todayDate);
  await updateDoc(leaderboardRef, {
    entries: arrayUnion({
      userId,
      displayName: auth.currentUser.displayName || "Anonymous",
      wpm: result.wpm,
      accuracy: result.accuracy,
      snippetId: result.snippetId,
      timestamp: serverTimestamp(),
    }),
  });
}

// Cloud Function (runs daily at midnight)
export const calculateDailyLeaderboard = functions.pubsub
  .schedule("0 0 * * *")
  .onRun(async () => {
    const yesterday = getYesterdayDate();

    // Get all submissions from yesterday
    const submissions = await db
      .collectionGroup("testResults")
      .where("timestamp", ">=", yesterday)
      .orderBy("wpm", "desc")
      .limit(100)
      .get();

    // Write to leaderboard
    await db
      .collection("leaderboards/daily")
      .doc(yesterday)
      .set({
        entries: submissions.docs.map((d) => ({
          userId: d.ref.parent.parent.id,
          wpm: d.data().wpm,
          accuracy: d.data().accuracy,
        })),
      });
  });
```

**UI Changes**:

- "Leaderboard" tab in navigation
- Filter by time period (today, this week, all time)
- Real-time updates when new entries added

**Time Estimate**: 6-8 hours

---

### 5.3 Phase 3: User-Uploaded Snippets

**Goal**: Let users create and share custom snippets

```typescript
// features/custom-snippets.ts
export async function uploadCustomSnippet(snippet: SnippetData) {
  const userId = auth.currentUser.uid;
  const snippetId = generateId();

  // Upload JSON to Storage
  const storageRef = ref(storage, `users/${userId}/snippets/${snippetId}.json`);
  await uploadString(storageRef, JSON.stringify(snippet), "raw", {
    contentType: "application/json",
  });

  // Store metadata in Firestore
  await setDoc(doc(db, "snippets", snippetId), {
    authorId: userId,
    name: snippet.name,
    language: snippet.language,
    lines: snippet.total_lines,
    isPublic: false, // Private by default
    createdAt: serverTimestamp(),
  });
}

// Cloud Function: Validate uploaded snippet
export const validateSnippet = functions.storage
  .object()
  .onFinalize(async (object) => {
    const snippet = await downloadAndParseSnippet(object.name);

    // Validate structure
    if (!isValidSnippetSchema(snippet)) {
      await deleteFile(object.name);
      throw new Error("Invalid snippet format");
    }

    // Update Firestore
    await updateDoc(doc(db, "snippets", snippetId), {
      validated: true,
      validatedAt: serverTimestamp(),
    });
  });
```

**UI Changes**:

- "Create Snippet" button
- Paste code → Parse with tree-sitter WASM → Preview → Upload
- "My Snippets" library section
- Share button (copy link)

**Time Estimate**: 8-12 hours

---

### 5.4 Phase 4: Social Features

**Goal**: Profiles, follows, snippet sharing

```typescript
// features/social.ts
export async function shareSnippet(snippetId: string) {
  const userId = auth.currentUser.uid;

  // Make snippet public
  await updateDoc(doc(db, "snippets", snippetId), {
    isPublic: true,
    sharedAt: serverTimestamp(),
  });

  // Add to public feed
  await addDoc(collection(db, "publicSnippets"), {
    snippetId,
    authorId: userId,
    authorName: auth.currentUser.displayName,
    timestamp: serverTimestamp(),
    upvotes: 0,
    views: 0,
  });

  return `${window.location.origin}/snippet/${snippetId}`;
}

export async function upvoteSnippet(snippetId: string) {
  const userId = auth.currentUser.uid;

  await runTransaction(db, async (transaction) => {
    const snippetRef = doc(db, "publicSnippets", snippetId);
    const upvoteRef = doc(db, "upvotes", `${userId}_${snippetId}`);

    // Check if already upvoted
    const upvote = await transaction.get(upvoteRef);
    if (upvote.exists()) {
      throw new Error("Already upvoted");
    }

    // Record upvote and increment count
    transaction.set(upvoteRef, {
      userId,
      snippetId,
      timestamp: serverTimestamp(),
    });
    transaction.update(snippetRef, { upvotes: increment(1) });
  });
}
```

**Time Estimate**: 12-16 hours

---

## Part 6: Deployment & Monitoring (1 hour)

### 6.1 CI/CD Setup (30 min)

```yaml
# .github/workflows/firebase-deploy.yml
name: Deploy to Firebase

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Run tests
        run: npm test

      - name: Deploy to Firebase
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: "${{ secrets.GITHUB_TOKEN }}"
          firebaseServiceAccount: "${{ secrets.FIREBASE_SERVICE_ACCOUNT }}"
          channelId: live
          projectId: treetype-prod
```

### 6.2 Monitoring & Debugging (30 min)

- **Firebase Console Overview**

  - Analytics: User engagement, popular features
  - Performance: Page load times, network requests
  - Crashlytics: Error tracking (for web)
  - Usage dashboard: Firestore reads/writes, Storage bandwidth

- **Debugging Tools**
  - Firebase Emulator UI: Local testing
  - Firestore Rules Playground: Test security rules
  - Functions logs: Cloud Function debugging
  - Analytics DebugView: Test events in real-time

---

## Part 7: Cost Management & Scaling (30 min)

### 7.1 Understanding Firebase Pricing

**Free Tier (Spark Plan)**:

- Firestore: 50K reads, 20K writes, 1GB storage/day
- Storage: 1GB stored, 10GB/month downloads
- Authentication: Unlimited
- Functions: 2M invocations, 400K GB-seconds/month

**When you'd upgrade (Blaze Plan)**:

- ~500 daily active users
- ~10K test completions/day
- Heavy leaderboard usage

**Cost Estimation**:

```
Low traffic (100 DAU):
- Firestore: $0-5/month
- Storage: $0-2/month
- Functions: $0-3/month
Total: ~$10/month

Medium traffic (1000 DAU):
- Firestore: $20-40/month
- Storage: $5-10/month
- Functions: $10-20/month
Total: ~$60/month

High traffic (10K DAU):
- Firestore: $200-400/month
- Storage: $50-100/month
- Functions: $100-200/month
Total: ~$600/month
```

### 7.2 Optimization Strategies

- **Reduce Reads**: Cache data, use real-time listeners wisely
- **Batch Writes**: Combine multiple updates
- **CDN for Static Assets**: Keep snippets in GitHub, metadata in Firestore
- **Efficient Queries**: Use indexes, avoid `collectionGroup()` when possible
- **Rate Limiting**: Prevent abuse with security rules

---

## Recommended Learning Path

### Week 1: Foundation

- Day 1-2: Part 1 (Setup) + Part 2.1 (Firestore basics)
- Day 3-4: Part 2.2 (Auth) + Build Phase 1 (Progress tracking)
- Day 5-7: Test, refine, deploy Phase 1

### Week 2: Advanced Features

- Day 1-2: Part 2.3 (Storage) + Part 3.1 (Functions)
- Day 3-5: Build Phase 2 (Leaderboards)
- Day 6-7: Build Phase 3 (Custom snippets)

### Week 3: Professional

- Day 1-3: Part 4 (Security, Performance, Testing)
- Day 4-7: Build Phase 4 (Social features) or focus on polish

---

## Key Takeaways for a Python Developer

1. **Firebase is NOT a traditional backend** - No Flask/Django equivalents, think "database with built-in API"

2. **Security rules replace middleware** - Client-side permissions, not server-side checks

3. **Real-time by default** - Embrace listeners instead of polling

4. **NoSQL mindset** - Denormalize data, optimize for reads, think in documents

5. **Client SDK does heavy lifting** - Your TypeScript code talks directly to Firebase

6. **Cloud Functions for server logic** - When you need Python/Node backend, Functions fill the gap

7. **Cost scales with usage** - Free tier is generous, but monitor reads/writes

8. **Local emulators are essential** - Test everything locally before deploying

---

## Resources

**Official Docs** (bookmark these):

- Firebase Docs: https://firebase.google.com/docs
- Firestore Data Model: https://firebase.google.com/docs/firestore/data-model
- Security Rules Guide: https://firebase.google.com/docs/rules
- Functions Quickstart: https://firebase.google.com/docs/functions

**Video Tutorials** (if you prefer):

- Fireship.io: 100 second Firebase concepts (quick overviews)
- Net Ninja: Firebase Firestore Tutorial (comprehensive series)

**Hands-On Practice**:

- Firebase Codelabs: https://codelabs.developers.google.com/?product=firebase
- Sample Apps: https://github.com/firebase/quickstart-js

---

**Total Time Estimate**: 15-20 hours for crash course + 40-60 hours for TreeType implementation

**Your advantage**: Strong backend fundamentals, TypeScript experience, methodical planning. Firebase will feel foreign initially (no server!), but your database/security thinking transfers directly.

**Start here**: Part 1.2 (Project Setup) → Deploy current TreeType to Firebase Hosting → Part 2.1 (Firestore) → Build Phase 1 (Progress tracking). You'll have a working Firebase feature in ~6 hours.
