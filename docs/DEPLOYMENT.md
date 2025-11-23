# Deployment Guide - Market Signals Zerodha

## 🚀 Deployment Options

### Option 1: Vercel (Recommended for Quick Deploy)

**Best for**: Fast deployment, serverless, automatic scaling

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Configure Environment Variables**:
   - Go to https://vercel.com/dashboard
   - Add your project
   - Settings → Environment Variables:
     ```
     ZERODHA_API_KEY=g5tyrnn1mlckrb6f
     ZERODHA_API_SECRET=9qlzwmum5f7pami0gacyxc7uxa6w823s
     ```

3. **Deploy**:
   ```bash
   cd market-signals-zerodha
   vercel --prod
   ```

4. **Update CORS**: Edit `backend/main.py` to allow your Vercel domain:
   ```python
   allow_origins=["https://your-app.vercel.app"]
   ```

**Live URL**: `https://your-app.vercel.app`

---

### Option 2: Railway.app (Full-Stack Deployment)

**Best for**: Python + Node.js apps, databases, persistent storage

1. **Sign up**: https://railway.app
2. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   ```

3. **Deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

4. **Add Environment Variables** in Railway dashboard:
   - `ZERODHA_API_KEY`
   - `ZERODHA_API_SECRET`
   - `REDIRECT_URL=https://your-app.railway.app/auth/callback`

**Live URL**: `https://your-app.railway.app`

---

### Option 3: Render.com (Free Tier Available)

**Best for**: Free hosting, auto-deploy from Git

**Backend Setup**:
1. Go to https://render.com/dashboard
2. **New → Web Service**
3. Connect your Git repository
4. Settings:
   - **Name**: market-signals-backend
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: Add your Zerodha credentials

**Frontend Setup**:
1. **New → Static Site**
2. Settings:
   - **Name**: market-signals-frontend
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/.next`

**Live URLs**:
- Backend: `https://market-signals-backend.onrender.com`
- Frontend: `https://market-signals-frontend.onrender.com`

---

### Option 4: Docker + Any Cloud (AWS/Azure/GCP/DigitalOcean)

**Best for**: Full control, custom infrastructure

**Using Docker Compose**:

1. **Build and Run**:
   ```bash
   docker-compose up --build
   ```

2. **Deploy to Cloud**:
   ```bash
   # Push to Docker Hub
   docker tag market-signals-backend:latest yourusername/market-signals-backend
   docker push yourusername/market-signals-backend
   
   # Deploy to your cloud provider
   # (Follow provider-specific instructions)
   ```

**Cloud Providers**:
- **DigitalOcean App Platform**: $5/month
- **AWS ECS/Fargate**: Pay-as-you-go
- **Google Cloud Run**: Serverless containers
- **Azure Container Instances**: Pay-per-second

---

### Option 5: Heroku (Classic PaaS)

**Best for**: Simple deployments, Git-based workflow

1. **Install Heroku CLI**:
   ```bash
   npm i -g heroku
   ```

2. **Create Apps**:
   ```bash
   heroku create market-signals-backend
   heroku create market-signals-frontend
   ```

3. **Deploy Backend**:
   ```bash
   cd backend
   git init
   git add .
   git commit -m "Deploy backend"
   heroku git:remote -a market-signals-backend
   git push heroku main
   ```

4. **Set Environment Variables**:
   ```bash
   heroku config:set ZERODHA_API_KEY=your_key -a market-signals-backend
   heroku config:set ZERODHA_API_SECRET=your_secret -a market-signals-backend
   ```

5. **Deploy Frontend** (similar process)

**Live URLs**:
- Backend: `https://market-signals-backend.herokuapp.com`
- Frontend: `https://market-signals-frontend.herokuapp.com`

---

## 🔧 Post-Deployment Configuration

### Update Frontend Backend URL

Edit `frontend/pages/index.js`:
```javascript
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://your-backend.com'
```

### Update CORS in Backend

Edit `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.com",
        "https://your-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Update Zerodha Redirect URL

In `backend/config.py`:
```python
REDIRECT_URL = 'https://your-backend.com/auth/callback'
```

Also update in Zerodha Kite Console:
- Go to https://developers.kite.trade/apps
- Edit your app
- Add redirect URL: `https://your-backend.com/auth/callback`

---

## 📊 Recommended: Vercel (Frontend) + Railway (Backend)

**Why**: Best of both worlds - fast frontend, powerful backend

1. **Deploy Frontend to Vercel**:
   ```bash
   cd frontend
   vercel --prod
   ```
   Result: `https://market-signals.vercel.app`

2. **Deploy Backend to Railway**:
   ```bash
   cd backend
   railway up
   ```
   Result: `https://market-signals-backend.railway.app`

3. **Update Frontend**:
   ```javascript
   const BACKEND_URL = 'https://market-signals-backend.railway.app'
   ```

4. **Update Backend CORS**:
   ```python
   allow_origins=["https://market-signals.vercel.app"]
   ```

---

## 🔐 Environment Variables Checklist

For any deployment, ensure these are set:

**Backend**:
- `ZERODHA_API_KEY`
- `ZERODHA_API_SECRET`
- `REDIRECT_URL` (your deployed backend URL + `/auth/callback`)

**Frontend**:
- `NEXT_PUBLIC_BACKEND_URL` (your deployed backend URL)

---

## 🧪 Testing Your Deployment

1. **Backend Health Check**:
   ```bash
   curl https://your-backend.com/health
   ```

2. **Frontend Access**:
   - Open: `https://your-frontend.com`
   - Select a symbol
   - Check browser console for API calls

3. **Authentication**:
   - Visit: `https://your-backend.com/auth/login`
   - Complete Zerodha login flow
   - Check for live data

---

## 💡 Cost Comparison

| Platform | Backend | Frontend | Total/Month |
|----------|---------|----------|-------------|
| Vercel + Railway | $5 | Free | $5 |
| Render.com | Free* | Free | $0 |
| Heroku | $7 | $7 | $14 |
| DigitalOcean | $5 | $5 | $10 |
| AWS (t2.micro) | $8 | $8 | $16 |

*Render free tier sleeps after inactivity

---

## 🆘 Troubleshooting

**CORS Errors**:
- Update `allow_origins` in backend
- Check frontend URL matches

**Authentication Fails**:
- Verify `REDIRECT_URL` matches Zerodha console
- Check API credentials

**No Signals Showing**:
- Check backend logs
- Verify `/api/signal` returns data
- Test with: `curl https://your-backend.com/api/signal?symbol=NIFTY`

**Frontend Won't Connect**:
- Check `BACKEND_URL` in frontend
- Verify CORS settings
- Check browser console for errors

---

## 📱 Next Steps After Deployment

1. ✅ Test all symbols (NIFTY, BANKNIFTY, SENSEX)
2. ✅ Verify STRONG BUY signals appear correctly
3. ✅ Test authentication flow with Zerodha
4. ✅ Monitor logs for errors
5. ✅ Set up custom domain (optional)
6. ✅ Add monitoring/alerts (optional)

---

**Choose your deployment method above and follow the steps. Most teams prefer Vercel + Railway for the best balance of ease and power!** 🚀
