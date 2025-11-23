# Render.com Deployment Guide

## 🚀 Quick Deploy to Render.com

### Step 1: Prepare Repository

1. **Initialize Git** (if not done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Render deployment"
   ```

2. **Push to GitHub** (or GitLab/Bitbucket):
   ```bash
   git remote add origin https://github.com/yourusername/market-signals-zerodha.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy Backend API

1. Go to https://dashboard.render.com/
2. Click **"New +" → "Web Service"**
3. Connect your Git repository
4. Configure:
   - **Name**: `market-signals-backend`
   - **Region**: Singapore (closest to India)
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start Command**: 
     ```bash
     cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: Free

5. **Add Environment Variables**:
   - `ZERODHA_API_KEY` = `g5tyrnn1mlckrb6f`
   - `ZERODHA_API_SECRET` = `9qlzwmum5f7pami0gacyxc7uxa6w823s`
   - `REDIRECT_URL` = `https://market-signals-backend.onrender.com/auth/callback`
   - `PYTHON_VERSION` = `3.11.0`

6. Click **"Create Web Service"**

**Backend URL**: `https://market-signals-backend.onrender.com`

### Step 3: Deploy Frontend

1. Click **"New +" → "Static Site"**
2. Connect same repository
3. Configure:
   - **Name**: `market-signals-frontend`
   - **Region**: Singapore
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: 
     ```bash
     npm install && npm run build
     ```
   - **Publish Directory**: `.next`
   - **Plan**: Free

4. **Add Environment Variables**:
   - `NEXT_PUBLIC_BACKEND_URL` = `https://market-signals-backend.onrender.com`
   - `NODE_VERSION` = `18.17.0`

5. Click **"Create Static Site"**

**Frontend URL**: `https://market-signals-frontend.onrender.com`

### Step 4: Update CORS

After backend deploys, update `backend/main.py` CORS settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://market-signals-frontend.onrender.com",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Push changes:
```bash
git add .
git commit -m "Update CORS for Render deployment"
git push
```

Render will auto-redeploy! ✅

## 🔧 Alternative: Deploy Using Blueprint

Upload `render.yaml` to your repository, then:

1. Go to https://dashboard.render.com/
2. Click **"New +" → "Blueprint"**
3. Connect repository
4. Render will automatically create both services!

## 📊 After Deployment

**Your URLs:**
- Frontend: `https://market-signals-frontend.onrender.com`
- Backend: `https://market-signals-backend.onrender.com`
- API Docs: `https://market-signals-backend.onrender.com/docs`

**Update Zerodha Console:**
1. Go to https://developers.kite.trade/apps
2. Update Redirect URL: `https://market-signals-backend.onrender.com/auth/callback`

## ⚠️ Free Tier Limitations

- Services spin down after 15 minutes of inactivity
- Cold start takes 30-60 seconds
- 750 hours/month free

**Upgrade to Paid ($7/month per service) for:**
- Always-on services
- No cold starts
- Better performance

## 🐛 Troubleshooting

**Build Failed?**
- Check logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure Python version is 3.11

**CORS Errors?**
- Update `allow_origins` in `backend/main.py`
- Redeploy backend

**Frontend Can't Connect?**
- Verify `NEXT_PUBLIC_BACKEND_URL` is set correctly
- Check backend is running: visit `/health` endpoint

**Zerodha Auth Fails?**
- Update redirect URL in Kite console
- Check `REDIRECT_URL` environment variable

## 💡 Tips

1. **Monitor Deployments**: Check Render dashboard for build logs
2. **Free Plan**: Backend sleeps after 15 min inactivity
3. **Custom Domain**: Add in Render settings (free on paid plans)
4. **Auto-Deploy**: Push to Git → Auto redeploy

## 🎯 Cost

**Free Tier:**
- Backend: Free (sleeps when inactive)
- Frontend: Free
- Total: $0/month

**Paid Tier (Always-On):**
- Backend: $7/month
- Frontend: $7/month
- Total: $14/month

---

**Deployment Time: ~5-10 minutes** ⚡
