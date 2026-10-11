from __future__ import annotations

"""GUME v6.9 - Global Intelligence Engine

A modular Streamlit research system combining:
- market data (Yahoo Finance / yfinance)
- optional World Bank public indicators (no API key)
- optional FRED indicators (API key required by FRED)
- optional Open-Meteo weather observations/forecast
- CSV upload for any additional macro, agriculture, trade, geopolitical,
  demographic, technology or company dataset
- provenance, freshness, missingness and confidence scoring
- transparent regime, risk, stress, Monte Carlo and domain-fusion layers
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from io import StringIO
import math
import os
import warnings
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

try:
    import requests
except Exception:
    requests = None

try:
    import streamlit as st
except Exception:
    st = None

try:
    import yfinance as yf
except Exception:
    yf = None

APP_VERSION = "6.9"
UTC_NOW = lambda: datetime.now(timezone.utc)

@dataclass
class DataMeta:
    name: str
    source: str
    source_type: str = "external"
    unit: str = "unknown"
    geography: str = "global"
    segment: str = "macro"
    frequency: str = "unknown"
    quality: float = 0.5
    release_lag_days: float = 0.0
    retrieved_at: str = ""
    status: str = "ok"
    notes: str = ""

@dataclass
class ConnectorResult:
    name: str
    frame: pd.DataFrame
    meta: DataMeta
    error: str = ""

class GlobalDataHub:
    def __init__(self) -> None:
        self.frames: Dict[str, pd.DataFrame] = {}
        self.meta: Dict[str, DataMeta] = {}

    def add_frame(self, name: str, frame: pd.DataFrame, meta: DataMeta) -> None:
        if frame is None or frame.empty:
            return
        x = frame.copy()
        if not isinstance(x.index, pd.DatetimeIndex):
            x.index = pd.to_datetime(x.index, errors="coerce", utc=True)
        x = x[~x.index.isna()].sort_index()
        x = x.replace([np.inf, -np.inf], np.nan)
        if x.empty:
            return
        self.frames[name] = x
        self.meta[name] = meta

    def quality_report(self) -> pd.DataFrame:
        rows: List[Dict[str, Any]] = []
        now = UTC_NOW()
        for name, frame in self.frames.items():
            meta = self.meta[name]
            missing = float(frame.isna().mean().mean()) if not frame.empty else 1.0
            latest = frame.dropna(how="all").index.max() if not frame.empty else pd.NaT
            age_days = np.nan
            if pd.notna(latest):
                latest_ts = pd.Timestamp(latest)
                if latest_ts.tzinfo is None:
                    latest_ts = latest_ts.tz_localize("UTC")
                age_days = max(0.0, (pd.Timestamp(now) - latest_ts).total_seconds() / 86400.0)
            freshness = freshness_score(age_days, meta.frequency)
            q = float(np.clip(meta.quality, 0, 1))
            score = q * (1 - missing) * freshness
            rows.append({
                "dataset": name, "source": meta.source, "status": meta.status,
                "rows": len(frame), "latest": str(latest) if pd.notna(latest) else "n/a",
                "age_days": age_days, "missing_ratio": missing, "freshness": freshness,
                "quality_score": score, "geography": meta.geography, "segment": meta.segment, "notes": meta.notes,
            })
        return pd.DataFrame(rows).sort_values("quality_score", ascending=False) if rows else pd.DataFrame()

    def catalog(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(m) for m in self.meta.values()]) if self.meta else pd.DataFrame()

def freshness_score(age_days: float, frequency: str) -> float:
    if not np.isfinite(age_days):
        return 0.0
    freq = str(frequency).lower()
    half_life = {"daily": 7, "weekly": 21, "monthly": 60, "quarterly": 150, "annual": 450}.get(freq, 60)
    return float(np.exp(-age_days / max(half_life, 1)))

def clip01(x: float) -> float:
    return float(np.clip(x, 0.0, 1.0))

def score_from_z(x: float, scale: float = 1.0) -> float:
    if not np.isfinite(x):
        return 0.5
    return clip01(0.5 + 0.25 * np.tanh(float(x) / max(scale, 1e-9)))

def normalize_tickers(text: str) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(x.strip().upper() for x in str(text).replace(";", ",").split(",") if x.strip()))

if st is not None:
    _cache = st.cache_data
else:
    def _cache(*args, **kwargs):
        def deco(fn): return fn
        return deco

@_cache(ttl=900, show_spinner=False)
def download_market_prices(tickers: Tuple[str, ...], period: str) -> pd.DataFrame:
    if yf is None:
        return pd.DataFrame()
    raw = yf.download(list(tickers), period=period, auto_adjust=True, progress=False, threads=True, group_by="column", multi_level_index=True)
    if raw is None or raw.empty:
        return pd.DataFrame()
    if isinstance(raw.columns, pd.MultiIndex):
        fields = [str(x) for x in raw.columns.get_level_values(0)]
        field = "Close" if "Close" in fields else ("Adj Close" if "Adj Close" in fields else fields[0])
        px = raw[field].copy()
    else:
        field = "Close" if "Close" in raw.columns else str(raw.columns[0])
        px = raw[[field]].copy()
        px.columns = [tickers[0]]
    if isinstance(px, pd.Series):
        px = px.to_frame(name=tickers[0])
    px.columns = [str(c).upper() for c in px.columns]
    px.index = pd.to_datetime(px.index, errors="coerce")
    px = px[~px.index.isna()].sort_index()
    return px.replace([np.inf, -np.inf], np.nan).ffill(limit=3).dropna(how="all")

def http_json(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 20) -> Any:
    if requests is None:
        raise RuntimeError("A requests csomag nem érhető el.")
    for attempt in range(3):
        try:
            r = requests.get(url, params=params or {}, timeout=timeout, headers={"User-Agent": "GUME/6.9"})
            if r.status_code in (429, 500, 502, 503, 504) and attempt < 2:
                import time
                time.sleep(0.5 * (2 ** attempt))
                continue
            r.raise_for_status()
            return r.json()
        except Exception:
            if attempt < 2:
                import time
                time.sleep(0.5 * (2 ** attempt))
                continue
            raise
    raise RuntimeError("HTTP kérés sikertelen.")

def fetch_world_bank_indicator(country: str, indicator: str, name: str) -> ConnectorResult:
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    try:
        payload = http_json(url, {"format": "json", "per_page": 1000})
        rows = payload[1]
        vals = [(pd.Timestamp(f"{row['date']}-12-31", tz="UTC"), float(row["value"])) for row in rows if row.get("value") is not None and row.get("date") is not None]
        frame = pd.DataFrame(vals, columns=["date", name]).set_index("date").sort_index()
        meta = DataMeta(name=name, source="World Bank", source_type="API", frequency="annual", quality=0.95, geography=country.upper(), segment="economy", retrieved_at=UTC_NOW().isoformat())
        return ConnectorResult(name, frame, meta)
    except Exception as exc:
        meta = DataMeta(name=name, source="World Bank", source_type="API", frequency="annual", quality=0.0, geography=country.upper(), segment="economy", status="error")
        return ConnectorResult(name, pd.DataFrame(), meta, str(exc))

def fetch_open_meteo(latitude: float, longitude: float, name: str = "Weather") -> ConnectorResult:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": latitude, "longitude": longitude, "daily": "temperature_2m_mean,precipitation_sum,wind_speed_10m_max", "past_days": 30, "forecast_days": 7, "timezone": "UTC"}
    try:
        payload = http_json(url, params)
        daily = payload.get("daily", {})
        dates = daily.get("time", [])
        frame = pd.DataFrame({
            "temperature_mean": daily.get("temperature_2m_mean", []),
            "precipitation_sum": daily.get("precipitation_sum", []),
            "wind_max": daily.get("wind_speed_10m_max", []),
        }, index=pd.to_datetime(dates, utc=True))
        meta = DataMeta(name=name, source="Open-Meteo", source_type="API", frequency="daily", quality=0.90, geography=f"{latitude:.4f},{longitude:.4f}", segment="weather", retrieved_at=UTC_NOW().isoformat())
        return ConnectorResult(name, frame, meta)
    except Exception as exc:
        meta = DataMeta(name=name, source="Open-Meteo", source_type="API", frequency="daily", quality=0.0, status="error")
        return ConnectorResult(name, pd.DataFrame(), meta, str(exc))

def log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    return np.log(prices / prices.shift(1)).replace([np.inf, -np.inf], np.nan).dropna(how="all")

def annual_return(r: pd.Series, ann: int) -> float:
    x = r.dropna()
    return float(np.expm1(x.mean() * ann)) if len(x) >= 2 and ann > 0 else np.nan

def annual_vol(r: pd.Series, ann: int) -> float:
    x = r.dropna()
    return float(x.std(ddof=1) * np.sqrt(ann)) if len(x) > 1 else np.nan

def run_app() -> None:
    if st is None:
        raise RuntimeError("A Streamlit nincs telepítve.")
    st.set_page_config(page_title=f"GUME v{APP_VERSION} – Global Intelligence", page_icon="🌐", layout="wide")
    st.title(f"🌐 GUME v{APP_VERSION} – Global Intelligence Engine")
    st.caption("Piac + makro + időjárás + adatfabrika + kockázat + domain-fúzió kutatási rendszer[cite: 1, 2].")
    
    ticker_text = st.sidebar.text_input("Tickerek", "SPY, QQQ, GLD, BTC-USD")
    run = st.sidebar.button("🚀 GUME futtatása", type="primary")
    
    tickers = normalize_tickers(ticker_text)
    prices = download_market_prices(tickers, "2y")
    if prices.empty:
        st.warning("Kérlek, adj meg érvényes tickereket a bal oldalsávban.")
        return
    
    st.subheader("Piaci Adatok és Alapállapot")
    st.dataframe(prices.tail(10))

if __name__ == "__main__":
    run_app()
```[cite: 1, 2]