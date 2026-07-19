# ✈️ Aviation Intelligence Platform

<div align="center">

**Live India flight tracking · ML delay prediction · Airport analytics**

[![Python](https://img.shields.io/badge/Python-3.12-3572A5?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-ff4b4b?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Railway](https://img.shields.io/badge/Deployed_on-Railway-0B0D0E?style=flat&logo=railway&logoColor=white)](https://railway.app)
[![Tests](https://img.shields.io/badge/Tests-64%20passing-brightgreen?style=flat)](#)
[![License](https://img.shields.io/badge/License-MIT-bcff5c?style=flat)](LICENSE)

</div>

---

A self-learning project built from scratch — real-time flight tracking, ML-powered delay prediction, and airport analytics for Indian airspace.

## ✨ Features

| Module | Description |
|--------|-------------|
| ✈️ **Live Flight Ops** | Real-time positions for all Indian flights on a Mapbox satellite map. Auto-refreshes every 30 s via a shared server-side cache |
| 🤖 **Delay Prediction** | Hybrid XGBoost + rule engine scores every flight. Factors: congestion, METAR severity, route OTP, aircraft type, schedule pressure |
| 🏢 **Airport Analytics** | Congestion score (AFRI), inbound density, low-altitude pressure, and 1-hour schedule demand per airport |
| 🚨 **Anomaly Alerts** | Auto-detects holding patterns, go-arounds, diversions, and stale contacts |
| 👤 **Passenger Tracker** | Search any flight by call sign — live position, ETA, distance to destination, predicted delay reason |
| 🌦️ **Weather Integration** | CheckWX METAR ingestion with deduplication and severity scoring, feeds directly into the ML model |
| 📊 **Flight Board** | Departure/arrival board for 10 major Indian airports |

## 🛠️ Tech Stack

- **Backend** — Python 3.12, Streamlit, Pandas, SQLite, `concurrent.futures`
- **Map** — Mapbox GL JS (satellite + flight layers, trail arcs, aircraft SVG icons)
- **ML** — XGBoost, scikit-learn (feature engineering on live + METAR data)
- **APIs** — AirLabs (live flights), CheckWX (METAR weather), OpenSky (fallback)
- **Infra** — Railway, `python-dotenv`, thread-safe write locks, exponential back-off

## 🚀 Quick Start

```bash
git clone https://github.com/rinkuujangraa/indian-avitation-intelligence.git
cd indian-avitation-intelligence

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # fill in your API keys

streamlit run app.py
```

## 🔑 Environment Variables

| Variable | Required | Source |
|----------|----------|--------|
| `AIRLABS_API_KEY` | ✅ | [airlabs.co](https://airlabs.co/) |
| `MAPBOX_TOKEN` | ✅ | [account.mapbox.com](https://account.mapbox.com/) |
| `CHECKWX_API_KEY` | Recommended | [checkwx.com](https://www.checkwx.com/) |
| `CESIUM_TOKEN` | Optional | [ion.cesium.com](https://ion.cesium.com/) |
| `OPENSKY_USERNAME` / `OPENSKY_PASSWORD` | Training only | [opensky-network.org](https://opensky-network.org/) |

The app runs without `CHECKWX_API_KEY` — weather panels will show "Unavailable".

## 📁 Project Structure

```
├── app.py                  # Streamlit entry point + all UI modules
├── analytics.py            # Delay prediction, congestion, anomaly detection
├── data_fetcher.py         # AirLabs API client + OpenSky fallback + cache
├── mapbox_base.py          # Mapbox GL JS map HTML generator
├── tracker.py              # In-memory + on-disk flight trail tracker
├── snapshot_store.py       # SQLite snapshot store (time-slider playback)
├── weather_fetcher.py      # CheckWX METAR client with circuit breaker
├── delay_model.py          # XGBoost training pipeline
├── aircraft_icons.py       # SVG aircraft icon registry
│
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
├── Procfile                # Railway deployment config
├── railway.toml            # Railway project settings
│
├── tests/                  # Pytest test suite (64+ passing)
├── models/                 # Trained model artifacts (gitignored)
├── brand/                  # Logo assets
├── static/                 # Static assets (og:image, etc.)
└── .github/workflows/      # CI pipeline
```

## 🧪 Tests

```bash
pytest tests/ -v
```

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built by <a href="https://github.com/rinkuujangraa">@rinkuujangraa</a> — learning by building real things</sub>
</p>
