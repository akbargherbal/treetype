# Firebase Course: Deploy a Tree-Sitter Typing Game

## Table of Contents

### Module 1: Firebase Fundamentals for Python Developers

**Duration: 2-3 hours**

1.1 **Firebase Platform Overview**

- What Firebase offers (Hosting, Firestore, Cloud Functions, Storage)
- Firebase vs traditional backends
- When to use Firebase vs Cloud Run
- Project setup and Firebase CLI installation

  1.2 **Firebase Hosting Basics**

- Deploying static sites (HTML, CSS, JS)
- Local development with `firebase serve`
- Production deployment with `firebase deploy`
- Custom domains and SSL

  1.3 **Firebase Project Structure**

```
my-app/
├── public/              # Static files (your HTML, CSS, JS)
├── functions/           # Cloud Functions (Node.js)
├── firebase.json        # Firebase configuration
└── .firebaserc          # Project aliases
```

---

### Module 2: Architecture Decision for Your App

**Duration: 1 hour**

2.1 **Option A: Pre-generate JSON Files (Recommended for MVP)**

- Run `parse_json.py` locally during development
- Commit generated JSON files to `public/output/json_samples/`
- Deploy as static files with Firebase Hosting
- **Pros**: Simple, fast, no backend costs
- **Cons**: Must regenerate manually when parser changes

  2.2 **Option B: Cloud Functions (Node.js)**

- Rewrite parser logic in JavaScript/TypeScript
- Use Cloud Functions to generate JSON on-demand
- **Pros**: Dynamic generation
- **Cons**: Must port Python logic to Node.js

  2.3 **Option C: Cloud Run + Firebase Hosting (Hybrid)**

- Keep your Python parser as-is
- Deploy Python parser to Cloud Run
- Call Cloud Run from frontend or Firebase Functions
- **Pros**: Keep Python code, dynamic generation
- **Cons**: More complex setup, higher costs

**Recommendation for this project**: Start with **Option A**, then upgrade to **Option C** if you need dynamic parsing.

---

### Module 3: Deploying Your App (Static Approach)

**Duration: 1 hour**

3.1 **Prepare Your Project**

```bash
# Generate JSON files locally
python parse_json.py

# Your directory structure:
public/
├── render_code.html          # Your main HTML file
├── output/
│   └── json_samples/
│       ├── python_sample.json
│       ├── javascript_sample.json
│       ├── typescript_sample.json
│       └── tsx_sample.json
```

3.2 **Initialize Firebase**

```bash
npm install -g firebase-tools
firebase login
firebase init hosting
```

3.3 **Configure firebase.json**

```json
{
  "hosting": {
    "public": "public",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      {
        "source": "/",
        "destination": "/render_code.html"
      }
    ]
  }
}
```

3.4 **Deploy**

```bash
firebase deploy
```

---

### Module 4: Adding Cloud Run (Dynamic Parser)

**Duration: 2-3 hours**

4.1 **Why Cloud Run for Python?**

- Cloud Functions only supports Node.js, Python (beta, limited), Go, Java
- Cloud Run supports any containerized app (full Python support)
- Pay-per-use pricing model

  4.2 **Containerize Your Parser**

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY parse_json.py .
COPY . .

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
```

4.3 **Create Flask API Wrapper**

```python
# app.py
from flask import Flask, request, jsonify
from parse_json import parse_code_to_dataframe, dataframe_to_json, PARSERS

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_code():
    data = request.json
    code = data.get('code')
    language = data.get('language', 'python')

    # Your existing parsing logic
    lang, parser = PARSERS[language]
    df = parse_code_to_dataframe(code, parser, language)
    result = dataframe_to_json(df, code, language)

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

4.4 **Deploy to Cloud Run**

```bash
gcloud run deploy parse-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

4.5 **Call from Frontend**

```javascript
// In render_code.html
async function loadLanguage(language) {
  // Option 1: Load pre-generated static files
  const response = await fetch(`output/json_samples/${language}_sample.json`);

  // Option 2: Call Cloud Run to generate dynamically
  // const response = await fetch('https://your-cloud-run-url/parse', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ language, code: sampleCode })
  // });

  currentData = await response.json();
}
```

---

### Module 5: Firestore for User Progress (Optional)

**Duration: 2 hours**

5.1 **Add Firestore Database**

- Store user typing stats
- Track progress across sessions
- Leaderboards

  5.2 **Security Rules**

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

5.3 **Frontend Integration**

```javascript
import { initializeApp } from "firebase/app";
import { getFirestore, doc, setDoc } from "firebase/firestore";

const db = getFirestore();

function saveProgress(wpm, accuracy) {
  setDoc(doc(db, "users", userId), {
    lastWpm: wpm,
    lastAccuracy: accuracy,
    timestamp: Date.now(),
  });
}
```

---

### Module 6: Cost Optimization & Monitoring

**Duration: 1 hour**

6.1 **Firebase Hosting Costs**

- Free tier: 10GB storage, 360MB/day bandwidth
- Your app: ~50KB HTML + 4 JSON files (~10KB each) = negligible

  6.2 **Cloud Run Costs**

- Free tier: 2 million requests/month
- Cost estimator for your usage

  6.3 **Monitoring**

- Firebase Console metrics
- Cloud Run request logs
- Performance monitoring

---

## Recommended Learning Path

### Week 1: Static Deployment (Fastest Path to Production)

1. Complete Module 1 & 3
2. Deploy your current app as-is
3. **Deliverable**: Live app on Firebase Hosting

### Week 2: Dynamic Parser (If Needed)

1. Complete Module 2 & 4
2. Add Cloud Run backend
3. **Deliverable**: Dynamic code parsing

### Week 3: Enhancements (Optional)

1. Complete Module 5
2. Add user authentication and progress tracking
3. **Deliverable**: Persistent user data

---

## Quick Start Command Sequence

```bash
# 1. Generate static files
python parse_json.py

# 2. Setup Firebase
npm install -g firebase-tools
firebase login
firebase init hosting  # Select "public" as directory

# 3. Deploy
firebase deploy

# Done! Your app is live at https://your-project.web.app
```

---

## Key Takeaways for Python Devs

1. **Firebase Hosting ≠ Backend Hosting**: It's a CDN for static files (like Netlify/Vercel)
2. **Cloud Functions limitations**: Node.js preferred; Python support is limited
3. **Cloud Run is your friend**: Full Python support, containerized apps
4. **For this app**: Static JSON files are perfectly fine (regenerate when needed)
5. **Cost**: Firebase Hosting is essentially free for small projects

Would you like me to create detailed step-by-step tutorials for any specific module?
