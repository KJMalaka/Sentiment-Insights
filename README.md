# Social Sentiment & Brand Ambassador Fit Analyzer

A full-stack web app that takes a YouTube video URL, pulls its comments, runs them through a three-layer sentiment analysis pipeline, and turns the result into a sentiment breakdown, key themes, and a **Brand Ambassador Fit Score** — a quick read on whether a creator's audience sentiment makes them a good fit to represent a brand.

![Pipeline](https://img.shields.io/badge/pipeline-VADER%20%2B%20ML%20%2B%20LLM-informational)

Live link : https://sentiment-insights.vercel.app/

## Features

- **Three-layer sentiment analysis** on every comment — a rule-based layer, a classic ML model, and an LLM layer for nuance (sarcasm, mixed sentiment, themes)
- **Brand Ambassador Fit Score** (0–100) with a plain-language rationale, computed from sentiment, engagement rate, and controversy
- **Video hero header** with thumbnail, channel name, views/likes/subscribers, publish date, and a platform badge
- **Sentiment distribution chart** comparing all three layers side by side
- **Filterable comments table** (by sentiment, or by sarcastic/mixed-sentiment "nuanced" comments), with per-comment themes
- **PDF export** of the full dashboard
- **Result caching** — re-analyzing the same video returns instantly from a local SQLite cache instead of re-querying every API
- **Live analyzing progress panel** while a video is being processed

## Architecture

- **Backend**: Python, FastAPI, SQLAlchemy (SQLite for caching)
- **Frontend**: React 19, Vite, Tailwind CSS 4, Recharts
- **Sentiment pipeline** (`backend/services/sentiment/`):
  1. **VADER** — fast, rule-based, runs on every comment
  2. **Scikit-learn** — TF-IDF + Logistic Regression, trained on the IMDB dataset, runs on every comment
  3. **Groq LLM** (`llama-3.1-8b-instant`) — catches sarcasm, mixed sentiment, and extracts themes; capped at the first 50 comments per video to stay within Groq's free-tier rate limit (the rest fall back to a neutral placeholder)
- **Platform support**: YouTube is fully implemented (video metadata + up to 500 comments via the YouTube Data API v3). TikTok and Instagram adapters exist but currently return "not yet supported."

## Project Structure

```
backend/
  adapters/            Platform adapters (YouTube implemented; TikTok/Instagram stubbed)
  models/               SQLAlchemy models (cache table)
  services/
    sentiment/          The 3-layer pipeline + sklearn training script
    insights.py          Distributions, agreement rate, themes, ambassador score
  main.py                FastAPI app, /api/analyze endpoint
  database.py            SQLite engine/session setup

frontend/
  src/
    components/          Dashboard, charts, comments table, score gauge, PDF export
    App.jsx               App shell, URL input, loading state
```

## Setup Instructions

### 1. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows (PowerShell: venv\Scripts\Activate.ps1)
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory (copy `.env.example`):

```
YOUTUBE_API_KEY=your_youtube_api_key
GROQ_API_KEY=your_groq_api_key
```

- **YouTube Data API v3 key**: create a project in the [Google Cloud Console](https://console.cloud.google.com/), enable the "YouTube Data API v3", then create an API key under Credentials.
- **Groq API key**: sign up at [console.groq.com](https://console.groq.com/) and create a key under API Keys. Groq's free tier has a tokens-per-minute limit, which is why the LLM layer caps analysis at 50 comments per video (`MAX_LLM_COMMENTS` in `services/sentiment/__init__.py`).

Train the classic ML layer (only needs to be run once — the trained model is checked into `services/sentiment/sentiment_model.joblib`, so this step is only needed if you want to retrain it):

```bash
python -m services.sentiment.train_sklearn_model
```

Run the backend server:

```bash
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

## API

**`POST /api/analyze`**

```json
{ "url": "https://www.youtube.com/watch?v=..." }
```

Returns `video_data` (title, channel, thumbnail, stats), `comments` (each tagged with all three layers' output), `insights` (distributions, agreement rate, top themes, ambassador score), and `platform`. Results are cached by video ID in SQLite — analyzing the same video twice returns the cached result immediately.

## Notes

- Without API keys, the app still starts and the UI loads — you just can't analyze a real video until `YOUTUBE_API_KEY` is set, and the Groq layer silently returns neutral/no-theme results until `GROQ_API_KEY` is set.
- The SQLite cache (`backend/sentiment_app.db`) and `.env` are gitignored.
