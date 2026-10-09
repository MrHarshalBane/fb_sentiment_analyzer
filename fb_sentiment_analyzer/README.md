# 🚀 FB Sentiment AI Bot - Facebook Topic Sentiment Analysis Engine

An AI-powered web application designed to scan Facebook data for specific user-provided topics (such as **Bitcoin**, **AI**, or **Stocks**) and analyze post sentiment using **NLTK (Natural Language Toolkit) VADER**.

---

## 🌟 Key Features & Filtering Parameters

- **🎯 Topic-Based Data Fetching**: Target specific topics or keywords (e.g., *Bitcoin*, *AI*, *Stocks*, *Tech*) instead of scanning the full web.
- **👍 Minimum Likes Filter**: Exclude low-engagement posts (Default threshold: `10 likes`).
- **🔁 Minimum Reposts / Shares Filter**: Focus on viral, widely-shared posts (Default threshold: `2 shares`).
- **💬 Reply / Comment Filter**: Toggle to exclude sub-replies/comments and analyze main topic posts.
- **🌐 Language Filtering**: Filters English posts for optimal sentiment classification accuracy.
- **📊 NLTK VADER Polarity Scoring**: Determines tone (`Positive`, `Negative`, or `Neutral`) with compound polarity scores (-1.0 to +1.0) and adjustable strength threshold.
- **📈 Interactive Analytics Dashboard**: Built with **Tailwind CSS**, **Chart.js** (Doughnut & Bar charts), and live parameter controls.
- **🔑 Dual Operating Mode**:
  - **Live Graph API Mode**: Supply a Facebook Graph API Access Token to query live FB posts.
  - **Instant Simulation Mode**: Out-of-the-box realistic simulation mode for instant local testing without needing a Meta Developer App.

---

## 📂 Project Architecture

```
fb_sentiment_analyzer/
├── app.py                # Flask Web Backend & REST API routes
├── analyzer.py           # NLTK VADER Sentiment Analyzer & custom filtering engine
├── fb_client.py          # Facebook Graph API Client & Mock Post Generator
├── requirements.txt      # Python dependencies (Flask, NLTK, Requests)
├── templates/
│   └── index.html        # Modern Tailwind CSS + Chart.js Dashboard UI
└── README.md             # Detailed documentation & deployment guide
```

---

## ⚡ Quickstart - Launching Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Web Application
```bash
python app.py
```

### 3. Open in Browser
Navigate to **`http://127.0.0.1:5000`** or **`http://localhost:5000`**.

---

## 🔑 Facebook Graph API Setup (Optional for Live Data)

To connect live Facebook Graph API data:
1. Go to the [Meta for Developers Portal](https://developers.facebook.com/).
2. Create an App (Select **Business** or **Consumer**).
3. Access the **Tools -> Graph API Explorer**.
4. Generate a **User Access Token** with `public_profile` and `user_posts` or `pages_read_engagement` permissions.
5. Paste your token into the **FB Graph API Access Token** input field in the web app UI.

---

## 🌐 Deploying & Hosting Your Website

### Option 1: Render (Recommended - Free Tier)
1. Push this project to GitHub.
2. Create a new **Web Service** on [Render.com](https://render.com).
3. Set Build Command: `pip install -r requirements.txt`
4. Set Start Command: `gunicorn app:app` (or `python app.py`)

### Option 2: Railway / Heroku / DigitalOcean
1. Add a `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Deploy directly via CLI or GitHub integration.
