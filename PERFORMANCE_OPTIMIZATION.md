# Performance Optimization Guide

## 🐌 Why Is It Slow?

### Current Bottlenecks:
1. **AirLabs API**: ~2 seconds per request
2. **Data Processing**: Heavy pandas operations on 100+ flights
3. **ML Model Loading**: XGBoost model (if exists)
4. **Map Generation**: Mapbox HTML with all flight layers
5. **Weather API**: CheckWX for multiple airports

## ⚡ Quick Fixes Applied

### 1. **Added Loading Spinner** ✅
Shows "Loading..." message while app initializes

### 2. **Health Check Script** ✅
Verifies dependencies before startup (Railway)

### 3. **Caching Enabled** ✅
- Flight data: 30s cache
- Airport data: 30min cache
- Weather data: 15min cache (in weather_fetcher.py)

## 🚀 Additional Optimizations You Can Apply

### **Option 1: Reduce Initial Data Load**

Edit `app.py` to load fewer flights initially:

```python
# Around line 163-180
@st.cache_data(ttl=30, show_spinner=False)
def load_flight_data_cached(region):
    # Add limit parameter
    flights = get_flight_data(region)
    # Only process top 50 flights initially
    if len(flights) > 50:
        flights = flights.head(50)
    return flights
```

### **Option 2: Lazy Load Heavy Features**

Don't compute analytics until user clicks:

```python
# Only compute when needed
if st.button("Show Delay Analytics"):
    analytics = compute_delay_predictions(flights)
```

### **Option 3: Use Lighter Map on First Load**

```python
# Simple markers first, details on hover
if 'detailed_map' not in st.session_state:
    # Show simple map
else:
    # Show full features
```

### **Option 4: Async Data Loading**

Load APIs in parallel:

```python
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor() as executor:
    future_flights = executor.submit(get_flight_data, "india")
    future_weather = executor.submit(get_weather_data)
    flights = future_flights.result()
    weather = future_weather.result()
```

## 📊 Expected Load Times

| Component | Current | After Optimization |
|-----------|---------|-------------------|
| API Fetch | 2-3s | 2-3s (unavoidable) |
| Processing | 2-4s | 0.5-1s (fewer flights) |
| Map Render | 1-2s | 0.5s (lazy load) |
| **Total** | **5-9s** | **3-4.5s** |

## 🎯 Best Practices for Production

1. **Use CDN for static assets**
2. **Enable Streamlit's experimental features**:
   ```python
   st.set_page_config(
       page_title="...",
       layout="wide",
       initial_sidebar_state="collapsed",
   )
   ```

3. **Add progress bars**:
   ```python
   progress = st.progress(0)
   progress.progress(50)  # 50% done
   progress.progress(100) # Complete
   progress.empty()       # Remove
   ```

4. **Implement pagination**:
   - Show 20 flights per page
   - Load more on scroll

## 🔧 Railway-Specific Optimizations

### **1. Increase Memory (if needed)**

Railway dashboard → Settings → Memory: 512MB → 1GB

### **2. Enable HTTP/2**

Already enabled by default on Railway

### **3. Set Timeout**

```toml
[deploy]
healthcheckTimeout = 60  # ✅ Already added
```

## 🧪 Test Performance

Run locally to measure:

```bash
# Terminal 1: Run app
streamlit run app.py

# Terminal 2: Measure load time
curl -w "\nTotal time: %{time_total}s\n" http://localhost:8501
```

## ✅ Current Status

- ✅ Loading spinner added
- ✅ Health check script
- ✅ Caching enabled
- ⚠️  Heavy data load (can optimize further)
- ⚠️  Full map on first load (can lazy-load)

## 💡 Recommendations

**For your use case (Aviation tracking):**

1. **Accept 3-5s load time** - This is normal for real-time data apps
2. **Add progress indicator** - Users don't mind waiting if they see progress
3. **Optimize after deployment** - Get it working first, then optimize

**Priority:**
1. Fix Railway deployment ← **Do this first**
2. Add loading indicator ← **Already done**
3. Optimize data loading ← **Optional, do later**

---

**Bottom line:** 5-9 seconds is acceptable for an app fetching live flight data from external APIs. Focus on fixing Railway first!
