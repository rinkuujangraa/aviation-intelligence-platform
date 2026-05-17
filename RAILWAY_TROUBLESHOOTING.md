# Railway Deployment Troubleshooting

## ✅ Your Environment Variables (Add to Railway)

**Required (Critical):**
```
AIRLABS_API_KEY=your_airlabs_key_from_env_file
MAPBOX_TOKEN=pk.your_mapbox_token_from_env_file
```

**Recommended:**
```
CHECKWX_API_KEY=your_checkwx_key_from_env_file
```

**Optional:**
```
CESIUM_TOKEN=your_cesium_token_from_env_file
```

**Get your actual keys from your `.env` file!**

⚠️ **DO NOT ADD:**
- `OPENSKY_USERNAME` (only for ML training)
- `OPENSKY_PASSWORD` (only for ML training)
- `ALERT_EMAIL_*` (optional, causes errors if SMTP blocked)

---

## 🔍 Step-by-Step Debugging

### **Step 1: Check Railway Logs**

1. Go to Railway dashboard
2. Click your deployment
3. Click **"Deployments"** tab
4. Click the latest deployment
5. Scroll to **"Deploy Logs"**

**Look for these errors:**

#### ❌ **Error: "ModuleNotFoundError"**
**Fix:** Missing dependency in requirements.txt
```bash
# Add missing package to requirements.txt, commit, push
```

#### ❌ **Error: "AIRLABS_API_KEY not found"**
**Fix:** Environment variable not set
1. Go to Railway dashboard → Variables
2. Add `AIRLABS_API_KEY` and `MAPBOX_TOKEN`
3. Redeploy

#### ❌ **Error: "Address already in use"**
**Fix:** Port binding issue (rare)
1. Check railway.toml has `--server.port $PORT`
2. Should already be correct

#### ❌ **Error: "No module named 'streamlit'"**
**Fix:** Build failed
1. Check requirements.txt exists
2. Redeploy

---

### **Step 2: Verify Environment Variables**

In Railway Dashboard:
1. Click your project
2. Click **"Variables"** tab
3. Verify you have:
   - ✅ `AIRLABS_API_KEY`
   - ✅ `MAPBOX_TOKEN`
   - ✅ `CHECKWX_API_KEY` (optional)

---

### **Step 3: Check Domain/URL**

Railway generates a URL like:
```
https://your-app-name.up.railway.app
```

1. Go to Railway dashboard → Settings
2. Under **"Domains"**, click **"Generate Domain"**
3. Copy the URL
4. Wait 30 seconds, then visit

---

### **Step 4: Force Redeploy**

If logs look fine but site still won't load:
1. Railway dashboard → Deployments
2. Click **"⋯"** (three dots) on latest deployment
3. Click **"Redeploy"**

---

## 🚀 **Quick Fix Commands**

If Railway shows errors, fix and redeploy:

```bash
# 1. Fix the issue locally
# 2. Commit changes
git add .
git commit -m "fix: Railway deployment issue"

# 3. Push to trigger redeploy
git push origin main
```

Railway auto-deploys on every push!

---

## 🧪 **Test Local Before Deploying**

Make sure it works locally first:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

If it works locally, it should work on Railway.

---

## 📋 **Railway Configuration Checklist**

✅ **Build Settings:**
- [x] Builder: Nixpacks (auto-detected)
- [x] Start Command: Defined in `railway.toml`
- [x] Python Version: 3.12 (from `runtime.txt`)

✅ **Environment Variables:**
- [ ] `AIRLABS_API_KEY` set?
- [ ] `MAPBOX_TOKEN` set?
- [ ] `CHECKWX_API_KEY` set?

✅ **Files:**
- [x] `railway.toml` exists
- [x] `requirements.txt` exists
- [x] `runtime.txt` exists
- [x] `Procfile` exists (backup)

---

## 🐛 **Common Error Messages & Fixes**

### **"This site can't be reached"**
- Domain not generated yet
- Go to Settings → Domains → Generate Domain

### **"Application error"**
- Check Deploy Logs for Python errors
- Usually missing environment variables

### **"502 Bad Gateway"**
- App crashed after starting
- Check logs for import errors or API key issues

### **"Build succeeded but deploy failed"**
- Start command issue
- Verify `railway.toml` is correct

---

## 📞 **Need More Help?**

**Share these with me:**
1. Railway Deploy Logs (last 50 lines)
2. Error message from browser (if any)
3. Railway deployment URL

I'll help you fix it!

---

## ✅ **Expected Working State**

When working correctly:
- Build logs show: "Build completed successfully"
- Deploy logs show: "You can now view your Streamlit app in your browser"
- Browser shows: Aviation Intelligence Platform with live flights

---

**Most Common Fix:** Just add the 2 required environment variables! 🎯
