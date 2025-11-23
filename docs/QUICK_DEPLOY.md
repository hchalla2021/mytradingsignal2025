# 🚀 Quick Deployment Guide

## Fastest Way to Deploy (5 minutes)

### Option 1: Vercel (Recommended)

**1. Install Vercel CLI:**
```bash
npm i -g vercel
```

**2. Deploy:**
```bash
cd market-signals-zerodha
vercel --prod
```

**3. Add Environment Variables:**
Go to https://vercel.com/dashboard → Your Project → Settings → Environment Variables

Add:
- `ZERODHA_API_KEY` = `g5tyrnn1mlckrb6f`
- `ZERODHA_API_SECRET` = `9qlzwmum5f7pami0gacyxc7uxa6w823s`

**4. Redeploy:**
```bash
vercel --prod
```

**Your app is now live!** 🎉

---

### Option 2: Railway.app

**1. Install Railway CLI:**
```bash
npm i -g @railway/cli
```

**2. Deploy:**
```bash
railway login
railway init
railway up
```

**3. Add Environment Variables in Railway Dashboard**

---

## What You'll Get

✅ Live URL: `https://your-app.vercel.app`  
✅ Auto HTTPS/SSL  
✅ Global CDN  
✅ Auto-scaling  
✅ 10-second signal updates  
✅ Real-time Zerodha data support  

---

## Post-Deployment Setup

1. **Update Zerodha Console:**
   - Go to: https://developers.kite.trade/apps
   - Add redirect URL: `https://your-app.vercel.app/auth/callback`

2. **Authenticate:**
   - Visit: `https://your-app.vercel.app/api/auth/login`
   - Complete Zerodha login
   - Start seeing live signals!

---

## Troubleshooting

**CORS Errors?**
Update `backend/main.py`:
```python
allow_origins=["https://your-app.vercel.app"]
```

**Not seeing signals?**
- Check browser console
- Visit: `https://your-app.vercel.app/api/health`
- Check logs in Vercel dashboard

---

**That's it! Your trading signals app is now live!** 🎯

For more deployment options, see [DEPLOYMENT.md](DEPLOYMENT.md)
