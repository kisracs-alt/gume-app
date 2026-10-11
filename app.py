import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

def run_gume_engine():
    st.set_page_config(page_title="GUME v6.9 – Globális Intelligencia Motor", page_icon="🌐", layout="wide")
    st.title("🌐 GUME v6.9 – Globális Intelligencia & Piaci Előrejelző Rendszer")
    st.caption("Adatvezérelt globális rezsim elemzés és piaci kilátások a holnapi napra.")

    st.sidebar.header("1. Elemzési Paraméterek")
    ticker_input = st.sidebar.text_input("Vizsgált eszközök (tickerek)", "SPY, QQQ, GLD, BTC-USD, EURUSD=X")
    period = st.sidebar.selectbox("Időtáv", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)
    
    run_btn = st.sidebar.button("🚀 Globális Elemzés Futtatása", type="primary")

    if run_btn:
        tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
        
        with st.spinner("Adatok letöltése és globális elemzés futtatása..."):
            try:
                data = yf.download(tickers, period=period, auto_adjust=True, progress=False)
                if data.empty:
                    st.error("Nem sikerült adatokat letölteni a megadott tickerekhez.")
                    return
                
                if isinstance(data.columns, pd.MultiIndex):
                    prices = data["Close"]
                else:
                    prices = data[["Close"]]
                    prices.columns = tickers

                prices = prices.dropna(how="all")
                
                # Hozamok és mutatók számítása
                returns = np.log(prices / prices.shift(1)).dropna()
                
                st.subheader("📊 Piaci Rezsim és Globális Állapot")
                
                col1, col2, col3 = st.columns(3)
                
                recent_return = returns.tail(21).mean().mean() * 252
                volatility = returns.tail(21).std().mean() * np.sqrt(252)
                
                if recent_return > 0.05 and volatility < 0.25:
                    regime = "EXPANSIVE (Expanzív / Risk-On)"
                elif recent_return < -0.05 or volatility > 0.30:
                    regime = "DEFENSIVE (Védekező / Risk-Off)"
                else:
                    regime = "TRANSITION (Átmeneti / Semleges)"

                col1.metric("Aktuális Piaci Rezsim", regime)
                col2.metric("Évesített Volatilitás", f"{volatility*100:.1f}%")
                col3.metric("Rövid távú Momentum", f"{recent_return*100:.1f}%")

                st.divider()

                st.subheader("📈 Eszközök Legfrissebb Árakai")
                st.dataframe(prices.tail(5), use_container_width=True)

                st.subheader("🔮 Holnapi Kilátások & Intelligencia Összegzés")
                if "EXPANSIVE" in regime:
                    st.success("A globális adatok alapján a kockázatvállalási kedv dominál. A piacok stabil növekedést mutathatnak a holnapi napon, de a volatilitást éber szemmel kell kísérni.")
                elif "DEFENSIVE" in regime:
                    st.warning("Magasabb piaci stressz vagy negatív momentum detektálva. A védekező stratégiák és a menedékeszközök (pl. arany) előnyben részesítése javasolt.")
                else:
                    st.info("Oldalazó, bizonytalan globális környezet. A rendszer semleges (Transition) állapotot mutat, óvatos pozíciókezelés indokolt.")

            except Exception as e:
                st.error(f"Hiba történt az elemzés során: {e}")
    else:
        st.info("Kattints a bal oldalsávban a **'Globális Elemzés Futtatása'** gombra a legfrissebb adatok lekéréséhez és a holnapi kilátások elemzéséhez.")

if __name__ == "__main__":
    run_gume_engine()
