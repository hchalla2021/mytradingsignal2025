# 🚀 Render.com Deployment Checklist

## ✅ Pre-Deployment

- [ ] Code pushed to GitHub/GitLab
- [ ] `render.yaml` configured
- [ ] Environment variables ready
- [ ] Zerodha API credentials confirmed

## 📋 Deployment Steps

### 1. Backend Service (5 min)

- [ ] Go to https://dashboard.render.com
- [ ] New Web Service → Connect repository
- [ ] **Settings:**
  - Name: `market-signals-backend`
  - Environment: Python 3
  - Build: `pip install -r backend/requirements.txt`
  - Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] **Environment Variables:**
  - `ZERODHA_API_KEY` = `g5tyrnn1mlckrb6f`
  - `ZERODHA_API_SECRET` = `9qlzwmum5f7pami0gacyxc7uxa6w823s`
  - `REDIRECT_URL` = `https://YOUR-SERVICE.onrender.com/auth/callback`
- [ ] Create Service
- [ ] Wait for deployment (~3-5 min)
- [ ] Test: Visit `https://YOUR-SERVICE.onrender.com/health`

### 2. Frontend Service (5 min)

- [ ] New Static Site → Same repository
- [ ] **Settings:**
  - Name: `market-signals-frontend`
  - Root: `frontend`
  - Build: `npm install && npm run build`
  - Publish: `.next`
- [ ] **Environment Variables:**
  - `NEXT_PUBLIC_BACKEND_URL` = (backend URL from step 1)
- [ ] Create Service
- [ ] Wait for build (~5-7 min)
- [ ] Test: Visit frontend URL

### 3. Post-Deployment

- [ ] Update CORS in `backend/main.py`:
  ```python
  allow_origins=["https://YOUR-FRONTEND.onrender.com"]
  ```
- [ ] Commit and push (auto-redeploy)
- [ ] Update Zerodha Console redirect URL
- [ ] Test authentication flow
- [ ] Verify signals are updating

## 🎯 Your Deployed URLs

**Backend API:**
```
https://market-signals-backend.onrender.com
```

**Frontend Dashboard:**
```
https://market-signals-frontend.onrender.com
```

**API Documentation:**
```
https://market-signals-backend.onrender.com/docs
```

## 🐛 Troubleshooting

**Build Failed?**
- Check Render logs
- Verify file paths in build commands
- Test locally: `scripts\test-render-build.bat`

**App Won't Load?**
- Free tier sleeps after 15 min
- First request takes 30-60 sec to wake up
- Check `/health` endpoint

**CORS Errors?**
- Update `allow_origins` in backend
- Push to trigger redeploy
- Clear browser cache

**No Signals?**
- Check backend logs
- Verify environment variables
- Test API: `/api/signal?symbol=NIFTY`

## 💰 Costs

**Free Tier:**
- ✅ 750 hours/month per service
- ✅ Auto-sleep after 15 min
- ✅ Free SSL
- ⚠️ Cold starts

**Upgrade ($7/service/month):**
- Always-on (no sleep)
- Instant response
- Better performance

## ⏱️ Deployment Time

- Backend: ~3-5 minutes
- Frontend: ~5-7 minutes
- **Total: ~10 minutes**

---

**Ready to deploy?** Follow `docs/RENDER_DEPLOY.md` for detailed instructions!
