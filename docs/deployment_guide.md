# 🌐 Live Deployment Guide – DevScope

This guide provides step-by-step instructions for deploying **DevScope** live to the web.

---

## 🚀 Option 1: Streamlit Community Cloud (Recommended - Free & 1-Click)

Streamlit Community Cloud hosts Streamlit applications directly from GitHub for free.

### Step-by-Step Deployment:
1. Push your DevScope repository to GitHub:
   ```bash
   git add .
   git commit -m "Deploy DevScope v4 Product Analytics Platform"
   git push origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **"New App"**.
4. Select your `DevScope` repository, `main` branch, and set Main file path to:
   ```
   dashboard/app.py
   ```
5. Click **"Deploy!"**. Your live application will be available in under 2 minutes at `https://devscope.streamlit.app`.

---

## 🐳 Option 2: Render / Railway / Docker Hosting

DevScope includes a production `Dockerfile` and `docker-compose.yml` for single-command cloud hosting on Render, Railway, or AWS App Runner.

### Deployment Commands:
```bash
docker-compose up --build -d
```

The container automatically executes `etl.pipeline` on startup, builds the database, and serves the Streamlit dashboard on port `8501`.
