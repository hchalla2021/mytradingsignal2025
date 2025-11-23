# ✅ Render.com Deployment - Ready!

Your code is now **100% ready** for Render.com deployment!

## 📦 Files Created

### Configuration Files
- ✅ `render.yaml` - Blueprint for automated deployment
- ✅ `Procfile` - Process configuration
- ✅ `runtime.txt` - Python version specification
- ✅ `.github/workflows/deploy-render.yml` - CI/CD workflow

### Documentation
- ✅ `docs/RENDER_DEPLOY.md` - Complete deployment guide
- ✅ `docs/RENDER_CHECKLIST.md` - Step-by-step checklist

### Scripts
- ✅ `scripts/render-build.sh` - Build script
- ✅ `scripts/test-render-build.bat` - Local build test
- ✅ `scripts/git-commit.bat` - Quick commit helper

### Code Updates
- ✅ Backend CORS configured for production
- ✅ Frontend build scripts updated
- ✅ Environment variable support added

## 🚀 Deploy in 3 Steps

### Step 1: Push to GitHub

```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Ready for Render deployment"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/market-signals-zerodha.git
git branch -M main
git push -u origin main
```

**OR use the helper script:**
```bash
scripts\git-commit.bat
```

### Step 2: Deploy to Render

1. Go to https://dashboard.render.com/
2. Click **"New +" → "Blueprint"**
3. Connect your GitHub repository
4. Click **"Apply"**

Render will automatically:
- Create backend service
- Create frontend service
- Set up environment variables
- Deploy both services

**That's it!** ✅

### Step 3: Update URLs

After deployment, update these in Render dashboard:

**Backend Environment Variables:**
- `REDIRECT_URL` = `https://YOUR-BACKEND.onrender.com/auth/callback`

**Frontend Environment Variables:**
- `NEXT_PUBLIC_BACKEND_URL` = `https://YOUR-BACKEND.onrender.com`

## 📋 What Render Will Deploy

### Backend API
- **URL**: `https://market-signals-backend.onrender.com`
- **API Docs**: `https://market-signals-backend.onrender.com/docs`
- **Health Check**: `https://market-signals-backend.onrender.com/health`
- **Plan**: Free tier (750 hours/month)
- **Build**: ~3-5 minutes
- **Auto-sleep**: After 15 min inactivity

### Frontend Dashboard
- **URL**: `https://market-signals-frontend.onrender.com`
- **Plan**: Free tier
- **Build**: ~5-7 minutes
- **Static**: Always-on (no sleep)

## 🎯 Post-Deployment Tasks

1. ✅ Test health endpoint: `/health`
2. ✅ Test API docs: `/docs`
3. ✅ Update Zerodha redirect URL in Kite console
4. ✅ Test signal generation: `/api/signal?symbol=NIFTY`
5. ✅ Visit frontend and select symbol
6. ✅ Verify 10-second updates working

## 💡 Pro Tips

### Custom Domain (Optional)
- Add in Render dashboard
- Free SSL included
- Example: `api.yourdomain.com` → Backend

### Monitoring
- Check Render dashboard for logs
- Set up email alerts
- Monitor `/health` endpoint

### Performance
- Free tier: 30-60 sec cold start
- Upgrade to $7/mo: Instant response, always-on
- Singapore region: Best for India latency

### Auto-Deploy
- Every push to `main` branch → Auto redeploy
- See deployment status in Render dashboard
- Rollback available if needed

## 🐛 Common Issues

**Build Failed?**
```bash
# Test locally first
scripts\test-render-build.bat
```

**CORS Errors?**
- Update `allow_origins` in `backend/main.py`
- Commit and push (auto-redeploy)

**Service Sleeping?**
- Free tier sleeps after 15 min
- First request wakes it up (30-60 sec)
- Upgrade to paid plan for always-on

## 📊 Cost Breakdown

**Free Tier:**
- Backend: $0 (750 hrs/month)
- Frontend: $0 (free static hosting)
- SSL: $0 (included)
- **Total: $0/month**

**Paid Tier (Always-On):**
- Backend: $7/month
- Frontend: $0 (static)
- **Total: $7/month**

## ⏱️ Deployment Timeline

- Git push: 1 minute
- Render build: 5-10 minutes
- Testing: 2-3 minutes
- **Total: ~15 minutes**

## 🎉 You're Ready!

Your code is **production-ready** for Render.com deployment!

Follow the guides:
1. **Quick**: `docs/RENDER_CHECKLIST.md` (step-by-step)
2. **Detailed**: `docs/RENDER_DEPLOY.md` (full guide)

---

**Questions?** Check Render docs: https://render.com/docs
