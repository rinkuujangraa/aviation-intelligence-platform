# Railway Deployment Guide

## Prerequisites
- Railway account (sign up at https://railway.app)
- API Keys:
  - AirLabs API key (https://airlabs.co/)
  - Mapbox token (https://account.mapbox.com/)
  - CheckWX API key (https://www.checkwx.com/) - optional

## Step-by-Step Deployment

### 1. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: Aviation Intelligence Platform"
```

### 2. Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository (e.g., "aviation-intelligence")
3. Don't initialize with README (you already have one)
4. Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/aviation-intelligence.git
git branch -M main
git push -u origin main
```

### 3. Deploy on Railway

#### Option A: Deploy from GitHub (Recommended)
1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Authorize Railway to access your GitHub
4. Select your `aviation-intelligence` repository
5. Railway will auto-detect it's a Python app

#### Option B: Deploy using Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 4. Configure Environment Variables

In Railway dashboard → Variables tab, add:

```
AIRLABS_API_KEY=your_airlabs_key_here
MAPBOX_TOKEN=pk.your_mapbox_token_here
CHECKWX_API_KEY=your_checkwx_key_here
```

Optional variables:
```
CESIUM_TOKEN=your_cesium_token
OPENSKY_USERNAME=your_opensky_username
OPENSKY_PASSWORD=your_opensky_password
ALERT_EMAIL_FROM=your.email@gmail.com
ALERT_EMAIL_TO=your.email@gmail.com
ALERT_EMAIL_PASSWORD=your_app_password
```

### 5. Deployment Settings

Railway should auto-detect these from your `railway.toml`:
- **Start Command**: `python3 inject_meta.py && streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
- **Builder**: Nixpacks (auto-detected)

### 6. Generate Domain

1. In Railway dashboard → Settings tab
2. Click "Generate Domain" under Public Networking
3. Your app will be live at: `https://your-app-name.up.railway.app`

## Post-Deployment

### Monitor Logs
```bash
railway logs
```

### Check Status
- Railway dashboard shows deployment status
- Check logs for any errors
- Visit your generated domain to test

### Update Deployment
```bash
git add .
git commit -m "Your changes"
git push origin main
```
Railway auto-deploys on every push to main.

## Troubleshooting

### Build Fails
- Check Python version in `runtime.txt` matches Railway's Python
- Verify all dependencies in `requirements.txt` are valid
- Check build logs in Railway dashboard

### App Crashes
- Verify all required environment variables are set
- Check Railway logs for error messages
- Ensure API keys are valid and have quota

### API Issues
- AirLabs has rate limits - check your quota
- CheckWX may be rate-limited without a key
- Weather features gracefully degrade if CheckWX key is missing

## Cost Estimate
- **Free Tier**: $5 credit/month (sufficient for light usage)
- **Pro Plan**: $20/month for production use
- This app uses minimal resources (~512MB RAM, low CPU)

## Performance Tips
1. Railway automatically scales based on traffic
2. Built-in caching reduces API calls
3. Circuit breaker prevents API quota exhaustion
4. 30-second refresh rate balances freshness vs cost
