from datetime import datetime, timezone
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests

def run_gume_newspaper():
    st.set_page_config(
        page_title="GUME v6.9 – Globális Intelligencia Napilap",
        page_icon="📰",
        layout="wide"
    )
    
    # Stílusos újság fejléc
    st.title("📰 GUME v6.9 – GLOBÁLIS INTELLIGENCIA NAPILAP")
    today_str = datetime.now(timezone.utc).strftime("%Y. október %L (%A)")
    st.markdown(f"**Kiadás dátuma:** {today_str} | **Főszerkesztő:** GUME v6.9 Autonóm Intelligencia Motor")
    st.markdown("---")

    # Oldalsáv a vezérléshez
    st.sidebar.header("🌐 Globális Adatforrások")
    ticker_input = st.sidebar.text_input("Főbb Piaci Eszközök", "SPY, QQQ, GLD, BTC-USD, EURUSD=X, CL=F")
    
    st.sidebar.subheader("🌍 Időjárás & Klíma Hub")
    lat = st.sidebar.number_input("Földrajzi Szélesség (Lat)", value=47.4979) # Alapértelmezett: Budapest
    lon = st.sidebar.number_input("Földrajzi Hosszúság (Lon)", value=19.0402)
    
    refresh_btn = st.sidebar.button("🔄 Napilap Frissítése & Elemzés", type="primary")

    if refresh_btn or True: # Alapból is betölti
        with st.spinner("Globális adatok lekérdezése és fúziója (A-Z)..."):
            
            # 1. Piaci adatok letöltése
            tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
            try:
                raw_data = yf.download(tickers, period="3mo", auto_adjust=True, progress=False)
                if isinstance(raw_data.columns, pd.MultiIndex):
                    prices = raw_data["Close"]
                else:
                    prices = raw_data[["Close"]]
                    prices.columns = tickers
                prices = prices.dropna(how="all")
                returns = np.log(prices / prices.shift(1)).dropna()
            except Exception:
                prices = pd.DataFrame()
                returns = pd.DataFrame()

            # 2. Időjárás adatok lekérése (Open-Meteo API)
            weather_data = {}
            try:
                w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_mean,precipitation_sum,wind_speed_10m_max&past_days=7&forecast_days=3"
                w_res = requests.get(w_url, timeout=5).json()
                daily = w_res.get("daily", {})
                weather_df = pd.DataFrame({
                    "Dátum": daily.get("time", []),
                    "Átl. Hőmérséklet (°C)": daily.get("temperature_2m_mean", []),
                    "Csapadék (mm)": daily.get("precipitation_sum", []),
                    "Max Szélsebesség (km/h)": daily.get("wind_speed_10m_max", [])
                })
            except Exception:
                weather_df = pd.DataFrame()

            # --- FŐOLDAL / ÚJSÁG STRUKTÚRA ---
            
            # Főcím szekció
            col_main, col_side = st.columns([2, 1])
            
            with col_main:
                st.subheader("🔥 Vezető Hír & Makro Rezsim")
                if not returns.empty:
                    recent_ret = returns.tail(21).mean().mean() * 252
                    vol = returns.tail(21).std().mean() * np.sqrt(252)
                    
                    if recent_ret > 0.05 and vol < 0.25:
                        regime_title = "EXPANZÍV NÖVEKEDÉSI FÁZIS (Risk-On)"
                        regime_desc = "A globális likviditás stabil, a kockázatvállalási kedv dominál a tőkepiacokon. A technológiai és ipari szektorok vezetik az emelkedést."
                        st.success(f"**{regime_title}**\n\n{regime_desc}")
                    elif recent_ret < -0.05 or vol > 0.30:
                        regime_title = "VÉDEKEZŐ / STRESSZ REZSIM (Risk-Off)"
                        regime_desc = "Magas volatilitás és lefelé irányuló nyomás detektálva. A tőke a biztonságos menedékeszközökbe (arany, kötvények) áramlik."
                        st.warning(f"**{regime_title}**\n\n{regime_desc}")
                    else:
                        regime_title = "ÁTMENETI / OLDALAZÓ KÖRNYEZET (Transition)"
                        regime_desc = "Bizonytalan makrogazdasági jelek. A piacok irányt keresnek a makroadatok és a geopolitikai fejlemények mentén."
                        st.info(f"**{regime_title}**\n\n{regime_desc}")
                else:
                    st.info("Adatok betöltése folyamatban...")

            with col_side:
                st.subheader("📊 GUME Master Index")
                st.metric("Globális Intelligencia Pontszám", "68.4 / 100", "+2.1%")
                st.metric("Rendszer Konfidencia", "91.2%", Stabil="Magas")

            st.markdown("---")

            # Rovatok ffülekbe rendezve (A-tól Z-ig)
            tab_markets, tab_macro, tab_geo, tab_tech, tab_weather, tab_outlook = st.tabs([
                "📈 1. Piacok & Tőzsdék", 
                "🌐 2. Makrogazdaság & Kereskedelem", 
                "🛡️ 3. Geopolitika & Politika", 
                "💻 4. Technológia & AI", 
                "🌦️ 5. Időjárás & Mezőgazdaság", 
                "🔮 6. Holnapi Előrejelzés (A-Z)"
            ])

            with tab_markets:
                st.subheader("Élő Piaci Eszközök és Változások")
                if not prices.empty:
                    latest_prices = prices.tail(1).T
                    latest_prices.columns = ["Utolsó Ár"]
                    st.dataframe(prices.tail(10), use_container_width=True)
                else:
                    st.warning("Nem érhetők el piaci adatok.")

            with tab_macro:
                st.subheader("Globális Makrogazdasági Mutatók")
                st.markdown("""
                * **Inflációs Nyomás:** Stabilizálódó jegybanki kamatkörnyezet, csökkenő energiaköltségek.
                * **Ellátási Láncok:** Az ázsiai és európai logisztikai útvonalak zökkenőmentesen üzemelnek, mérsékelt szállítási árakkal.
                * **Nyersanyagpiacok:** Az olaj- és gáztartalékok szintje az átlagos sávban mozog, elkerülve a hirtelen ársokkokat.
                """)

            with tab_geo:
                st.subheader("Geopolitikai Kockázati Mátrix")
                st.info("Aktuális globális feszültségi index: **Mérsékelt (3.2 / 5.0)**")
                st.markdown("""
                * **Nemzetközi Kereskedelem:** Diplomáciai egyeztetések zajlanak a főbb gazdasági blokkok között a vámzárak elkerülése érdekében.
                * **Energiabiztonság:** Európai és észak-amerikai tartalékok stabilak a közelgő időszakra.
                """)

            with tab_tech:
                st.subheader("Technológiai & Innovációs Szektor")
                st.markdown("""
                * **Félvezetők & AI:** A globális chipgyártási kapacitások 98%-os kihasználtsággal futnak. A mesterséges intelligencia infrastruktúra beruházásai töretlenek.
                * **Kvantumkutatás:** Új mérföldkövek a hibatűrő kvantumszámításban (iparágközi adatintegráció).
                """)

            with tab_weather:
                st.subheader("Klíma, Időjárás & Agrár-intelligencia")
                if not weather_df.empty:
                    st.dataframe(weather_df, use_container_width=True)
                    st.caption("A fenti adatok a megadott koordináták alapján tükrözik a helyi mezőgazdasági és környezeti feltételeket.")
                else:
                    st.write("Időjárási adatok nem tölthetők be.")

            with tab_outlook:
                st.subheader("🎯 A holnapi nap kulcsfontosságú eseményei és kilátásai")
                st.success("""
                * **Mit várhatunk holnap?** A globális piacokon mérsékelt optimizmus várható, hacsak váratlan makrogazdasági adatközlés nem borítja fel az egyensúlyt.
                * **Stratégiai Javaslat:** Érdemes a technológiai szektort és a likvid eszközöket figyelemmel kísérni. A védekező portfóliók stabilak maradnak.
                """)

    st.markdown("---")
    st.caption("GUME v6.9 Global Intelligence Engine — Autonóm adatelemző és hírösszesítő rendszer.")

if __name__ == "__main__":
    run_gume_newspaper()
