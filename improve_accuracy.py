"""
improve_accuracy.py
-------------------
Quick-win improvements for delay prediction accuracy.
Adds live traffic and holiday features to the model.

Run this to enhance your existing model with minimal changes.
"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np


# ── Indian Public Holidays 2024-2026 ─────────────────────────────────────────
INDIAN_HOLIDAYS = {
    # 2024
    "2024-01-26": "Republic Day",
    "2024-03-25": "Holi",
    "2024-03-29": "Good Friday",
    "2024-04-11": "Eid al-Fitr",
    "2024-04-17": "Ram Navami",
    "2024-04-21": "Mahavir Jayanti",
    "2024-06-17": "Eid al-Adha",
    "2024-08-15": "Independence Day",
    "2024-08-26": "Janmashtami",
    "2024-09-16": "Milad un-Nabi",
    "2024-10-02": "Gandhi Jayanti",
    "2024-10-12": "Dussehra",
    "2024-10-31": "Diwali",
    "2024-11-01": "Diwali (Day 2)",
    "2024-11-15": "Guru Nanak Jayanti",
    "2024-12-25": "Christmas",

    # 2025
    "2025-01-26": "Republic Day",
    "2025-03-14": "Holi",
    "2025-03-31": "Eid al-Fitr",
    "2025-04-06": "Ram Navami",
    "2025-04-10": "Mahavir Jayanti",
    "2025-04-18": "Good Friday",
    "2025-06-07": "Eid al-Adha",
    "2025-08-15": "Independence Day",
    "2025-08-16": "Janmashtami",
    "2025-09-05": "Milad un-Nabi",
    "2025-10-02": "Gandhi Jayanti",
    "2025-10-12": "Dussehra",
    "2025-10-20": "Diwali",
    "2025-11-05": "Guru Nanak Jayanti",
    "2025-12-25": "Christmas",

    # 2026
    "2026-01-26": "Republic Day",
    "2026-03-04": "Holi",
    "2026-03-21": "Eid al-Fitr",
    "2026-03-28": "Ram Navami",
    "2026-03-30": "Mahavir Jayanti",
    "2026-04-03": "Good Friday",
    "2026-05-28": "Eid al-Adha",
    "2026-08-05": "Janmashtami",
    "2026-08-15": "Independence Day",
    "2026-08-26": "Milad un-Nabi",
    "2026-10-02": "Gandhi Jayanti",
    "2026-10-22": "Dussehra",
    "2026-11-08": "Diwali",
    "2026-11-24": "Guru Nanak Jayanti",
    "2026-12-25": "Christmas",
}

# Festival seasons (multi-day impacts)
FESTIVAL_SEASONS = [
    ("2024-10-20", "2024-11-10", "Diwali Season"),  # Diwali + surrounding travel
    ("2025-10-10", "2025-10-30", "Diwali Season"),
    ("2026-10-28", "2026-11-18", "Diwali Season"),
    ("2024-12-20", "2025-01-05", "Christmas/New Year"),
    ("2025-12-20", "2026-01-05", "Christmas/New Year"),
]

# Fog season airports (Delhi, Lucknow, etc.)
FOG_SEASON_AIRPORTS = {"DEL", "VIDP", "LKO", "VILK", "JAI", "VIJP", "AGR", "VIAG", "ATQ", "VIAR"}


def is_public_holiday(date_str: str) -> bool:
    """Check if date is a public holiday."""
    return date_str in INDIAN_HOLIDAYS


def is_holiday_adjacent(date_str: str, days_buffer: int = 1) -> bool:
    """Check if date is within `days_buffer` days of a holiday."""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    for i in range(-days_buffer, days_buffer + 1):
        check_date = (date + timedelta(days=i)).strftime("%Y-%m-%d")
        if check_date in INDIAN_HOLIDAYS:
            return True
    return False


def is_festival_season(date_str: str) -> bool:
    """Check if date falls in a festival season."""
    date = datetime.strptime(date_str, "%Y-%m-%d")
    for start_str, end_str, _ in FESTIVAL_SEASONS:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")
        if start <= date <= end:
            return True
    return False


def get_live_airport_traffic(flights_df: pd.DataFrame, iata_code: str) -> dict:
    """
    Calculate live traffic metrics for an airport.

    Returns:
        dict with keys: arrivals_now, departures_now, inbound_30min, terminal_density
    """
    if flights_df.empty or not iata_code:
        return {
            "arrivals_now": 0,
            "departures_now": 0,
            "inbound_30min": 0,
            "terminal_density": 0,
        }

    arr_flights = flights_df[flights_df.get("arr_iata", pd.Series(dtype=str)) == iata_code]
    dep_flights = flights_df[flights_df.get("dep_iata", pd.Series(dtype=str)) == iata_code]

    # Inbound within 30 min: distance < 250km and altitude < 15000ft
    inbound = arr_flights[
        (pd.to_numeric(arr_flights.get("distance_km", pd.Series([999]*len(arr_flights))), errors="coerce") < 250) &
        (pd.to_numeric(arr_flights.get("altitude_ft", pd.Series([99999]*len(arr_flights))), errors="coerce") < 15000)
    ]

    # Terminal area density: flights within 50km
    terminal = arr_flights[
        pd.to_numeric(arr_flights.get("distance_km", pd.Series([999]*len(arr_flights))), errors="coerce") < 50
    ]

    return {
        "arrivals_now": len(arr_flights),
        "departures_now": len(dep_flights),
        "inbound_30min": len(inbound),
        "terminal_density": len(terminal),
    }


def add_enhanced_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add enhanced features to improve delay prediction accuracy.

    Features added:
    - is_public_holiday
    - is_holiday_adjacent
    - is_festival_season
    - is_fog_alert (for fog-prone airports in winter)
    - live_traffic_score

    Args:
        df: DataFrame with columns dep_month, dep_icao (or arr_icao), dep_date

    Returns:
        Enhanced DataFrame with new feature columns
    """
    df = df.copy()

    # ── Holiday features ──────────────────────────────────────────────────
    if "dep_date" in df.columns:
        df["is_public_holiday"] = df["dep_date"].apply(
            lambda x: int(is_public_holiday(str(x)[:10])) if pd.notna(x) else 0
        )
        df["is_holiday_adjacent"] = df["dep_date"].apply(
            lambda x: int(is_holiday_adjacent(str(x)[:10], days_buffer=1)) if pd.notna(x) else 0
        )
        df["is_festival_season"] = df["dep_date"].apply(
            lambda x: int(is_festival_season(str(x)[:10])) if pd.notna(x) else 0
        )
    else:
        # Fallback: use current date
        today = datetime.now().strftime("%Y-%m-%d")
        df["is_public_holiday"] = int(is_public_holiday(today))
        df["is_holiday_adjacent"] = int(is_holiday_adjacent(today))
        df["is_festival_season"] = int(is_festival_season(today))

    # ── Fog alert feature ─────────────────────────────────────────────────
    # 1 if departure is from fog-prone airport during Dec-Feb
    dep_month = df.get("dep_month", datetime.now().month)
    dep_icao = df.get("dep_icao", df.get("arr_icao", ""))

    if isinstance(dep_month, pd.Series):
        df["is_fog_alert"] = (
            dep_month.isin([12, 1, 2]) &
            dep_icao.isin(FOG_SEASON_AIRPORTS)
        ).astype(int)
    else:
        df["is_fog_alert"] = int(
            dep_month in [12, 1, 2] and
            str(dep_icao).upper() in FOG_SEASON_AIRPORTS
        )

    # ── Live traffic score (if flights_df available) ──────────────────────
    # This is a placeholder — in production, pass live flights_df
    # For now, use route_flight_count as proxy
    if "route_flight_count" in df.columns:
        # Normalize to 0-10 scale
        max_traffic = df["route_flight_count"].max()
        df["live_traffic_score"] = (
            df["route_flight_count"] / max_traffic * 10
        ).clip(0, 10).fillna(5.0)
    else:
        df["live_traffic_score"] = 5.0  # neutral default

    return df


def calculate_delay_multiplier(
    is_public_holiday: int,
    is_holiday_adjacent: int,
    is_festival_season: int,
    is_fog_alert: int,
    live_traffic_score: float,
) -> float:
    """
    Calculate delay probability multiplier based on enhanced features.

    Returns:
        Multiplier (0.8 - 2.5) to apply to base delay probability
    """
    multiplier = 1.0

    # Public holiday: +60% delay probability
    if is_public_holiday:
        multiplier *= 1.6
    # Day before/after holiday: +30%
    elif is_holiday_adjacent:
        multiplier *= 1.3

    # Festival season: +25%
    if is_festival_season:
        multiplier *= 1.25

    # Fog alert: +40% (fog is severe)
    if is_fog_alert:
        multiplier *= 1.4

    # Live traffic congestion (0-10 scale)
    # 0-3: reduce by 10%, 4-6: neutral, 7-8: +15%, 9-10: +30%
    if live_traffic_score <= 3:
        multiplier *= 0.9
    elif live_traffic_score >= 9:
        multiplier *= 1.3
    elif live_traffic_score >= 7:
        multiplier *= 1.15

    return min(max(multiplier, 0.8), 2.5)  # cap at 0.8x - 2.5x


# ── Example Usage ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("DELAY PREDICTION ACCURACY IMPROVEMENT SCRIPT")
    print("=" * 70)
    print()

    # Example: Check today's delay factors
    today = datetime.now().strftime("%Y-%m-%d")
    is_holiday = is_public_holiday(today)
    is_adj = is_holiday_adjacent(today)
    is_festival = is_festival_season(today)

    print(f"📅 Today: {today}")
    print(f"   Public Holiday: {'✅ YES' if is_holiday else '❌ No'}")
    if is_holiday:
        print(f"   Holiday: {INDIAN_HOLIDAYS[today]}")
    print(f"   Holiday Adjacent: {'✅ YES' if is_adj else '❌ No'}")
    print(f"   Festival Season: {'✅ YES' if is_festival else '❌ No'}")
    print()

    # Example: Enhanced delay prediction
    sample_flight = {
        "dep_date": today,
        "dep_month": datetime.now().month,
        "dep_icao": "VIDP",  # Delhi
        "route_flight_count": 150,
    }

    df = pd.DataFrame([sample_flight])
    df_enhanced = add_enhanced_features(df)

    print("Enhanced Features:")
    for col in ["is_public_holiday", "is_holiday_adjacent", "is_festival_season",
                "is_fog_alert", "live_traffic_score"]:
        print(f"  {col}: {df_enhanced[col].iloc[0]}")

    multiplier = calculate_delay_multiplier(
        int(df_enhanced["is_public_holiday"].iloc[0]),
        int(df_enhanced["is_holiday_adjacent"].iloc[0]),
        int(df_enhanced["is_festival_season"].iloc[0]),
        int(df_enhanced["is_fog_alert"].iloc[0]),
        float(df_enhanced["live_traffic_score"].iloc[0]),
    )

    print()
    print(f"🎯 Delay Probability Multiplier: {multiplier:.2f}x")
    print()

    # Simulate delay probability adjustment
    base_prob = 0.35  # 35% base delay probability from ML model
    adjusted_prob = min(base_prob * multiplier, 0.95)

    print(f"Example Flight Delay Prediction:")
    print(f"  Base ML Probability: {base_prob:.1%}")
    print(f"  Adjusted Probability: {adjusted_prob:.1%}")
    print(f"  Change: {(adjusted_prob - base_prob) * 100:+.1f} percentage points")
    print()

    print("=" * 70)
    print("✅ Script ready. Import functions into analytics.py or delay_model.py")
    print("=" * 70)
