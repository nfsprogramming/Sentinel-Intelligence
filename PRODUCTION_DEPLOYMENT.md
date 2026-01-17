# 🚀 SENTINEL Production Deployment (Hybrid Architecture)

To unleash the **full Transcendent Tier potential online**, you need a Hybrid Architecture because Vercel (Frontend) cannot run the heavy Python AI backend.

---

## 🏗️ Architecture
1.  **Frontend (Vercel):** Hosts the Next.js UI.
2.  **AI Cortex (Render/Railway):** Hosts the Python FastAPI Backend (runs PyTorch, keeps "Budget" state).
3.  **Communication:** Frontend calls Backend via HTTP API.

---

## 📦 Phase 1: Deploy Backend (The "Brain")
We will use **Render** (easiest free/cheap option for Python).

### 1. Update `backend/requirements.txt`
Ensure `fastapi`, `uvicorn`, `python-multipart` are in it.

### 2. Push Code to GitHub
Ensure your latest changes (including `backend/main.py`) are pushed.
```bash
git add .
git commit -m "Add FastAPI Server for Production"
git push
```

### 3. Deploy on Render.com
1.  Sign up at [Render.com](https://render.com).
2.  Click **New +** -> **Web Service**.
3.  Connect your `sentinel-intelligence` GitHub repo.
4.  **Settings:**
    *   **Root Directory:** `backend`
    *   **Runtime:** Python 3
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `python main.py`
5.  Click **Create Web Service**.
6.  **Wait:** Render will build it. Once done, it will give you a URL (e.g., `https://sentinel-backend.onrender.com`).
    *   *Copy this URL.*

---

## ⚡ Phase 2: Connect Frontend (The "Face")

### 1. Update Vercel Environment Variables
1.  Go to your Vercel Project Dashboard.
2.  Click **Settings** -> **Environment Variables**.
3.  Add a new variable:
    *   **Key:** `NEXT_PUBLIC_API_URL`
    *   **Value:** `https://your-backend-url.onrender.com` (The URL you copied from Render).
4.  Click **Save**.

### 2. Redeploy Vercel
1.  Go to **Deployments**.
2.  Click **Redeploy** on the latest commit.

---

## ✅ Usage
Now, when you open your Vercel site:
1.  Browser sends request to Vercel UI.
2.  Vercel UI sends request to Render Backend.
3.  Render Backend runs `fusion.py` (Real AI, PyTorch, Persistence).
4.  Results allow you to see the real **Intelligence Budget** count down!

---

**Note:** The Free Tier on Render spins down after inactivity. The first request might take 50 seconds to "wake up" the brain. Upgrading ($7/mo) fixes this.
