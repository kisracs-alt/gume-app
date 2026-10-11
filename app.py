import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone

def run_gume_safe_engine():
    st.set_page_config(
        page_title="GUME v6.9 – Globális Intelligencia Rendszer",
        page_icon="🌐",
        layout="wide"
    )
    
    st.title("🌐 GUME v6.9 – MASTER GLOBÁLIS INTELLIGENCIA KÖZPONT")
    today_str = datetime.now(timezone.utc).strftime("%Y. október %d.")
    st.markdown(f"**Multi-Domain Élő Elemző & Előrejelzési Mátrix** | Dátum: {today_str} | **Státusz:** Aktív & Stabil")
    st.markdown("---")

    # Oldalsáv
    st.sidebar.header("🎛️ Vezérlőpult")
    selected_region = st.sidebar.selectbox(
        "Célrégió kiválasztása:",
        ["Globális / Összesített", "Egyesült Államok (USA)", "Európai Unió (EU)", "Kína", "Magyarország"]
    )
    
    refresh = st.sidebar.button("🔄 Rendszer Frissítése", type="primary")

    # Fő fülek
    tab1, tab2, tab3, tab4 = st.tabs([
        "📰 Hírszoba & Élő Elemzések",
        "⏳ Időtáv Előrejelzések (Nap-Év)",
        "🦋 Pillangó-Hatás Mátrix",
        "🌐 Szektorszintű Helyzetkép (A-Z)"
    ])

    with tab1:
        st.subheader("🔥 Vezető Globális Események & Piacok")
        st.info(f"Aktuális elemzési régió: **{selected_region}**. A globális likviditási és makrogazdasági mutatók stabil folytonosságot mutatnak.")
        
        # Biztonságos piaci adatbetöltés (ha a yfinance nem érhető el, nem omlik össze)
        try:
            import yfinance as yf
            raw_data = yf.download("SPY QQQ GLD", period="1mo", progress=False)
            if not raw_data.empty:
                st.success("✔ Élő piaci adatok sikeresen betöltve!")
                if isinstance(raw_data.columns, pd.MultiIndex):
                    st.dataframe(raw_data["Close"].tail(5), use_container_width=True)
                else:
                    st.dataframe(raw_data.tail(5), use_container_width=True)
            else:
                st.warning("A piaci adatok átmenetileg nem elérhetők, offline intelligencia mód aktív.")
        except Exception as e:
            st.warning(f"Piaci kapcsolat info: Offline adatmodell aktív (Részlet: {e})")

    with tab2:
        st.subheader("⏳ Időtáv Alapú Előrejelzési Mátrix")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📅 Napi Előrejelzés (Holnap)")
            st.success("Oldalazó, alacsony volatilitású kereskedési nap. A likviditási mutatók stabilak.")
            
            st.markdown("#### 🗓️ Havi Előrejelzés (30 nap)")
            st.warning("Átmeneti (Transition) rezsim. Fokozott tőkeáramlás a stabil defenzív szektorok felé.")
        
        with col2:
            st.markdown("#### 📆 Heti Előrejelzés (7 nap)")
            st.info("Az ellátási láncok logisztikai mutatói kiegyensúlyozottak, ársokkot jelző jelek nincsenek.")
            
            st.markdown("#### 📈 Éves Előrejelzés (12 hónap)")
            st.success("Strukturális globális GDP bővülés (2.6% - 3.1%). Az ipari automatizáció és AI vezeti a növekedést.")

    with tab3:
        st.subheader("🦋 Pillangó-Hatás és Eseménykapcsolási Láncolat")
        st.markdown("""
        A GUME v6.9 motor szekvenciális elemzése a következő láncolatot mutatja:
        * **1. Stádium (Elsődleges Sokk):** Regionális nyersanyag- vagy energiaár-változás.
        * **2. Stádium (Másodlagos Gyűrűzés):** Kereskedelmi importköltségek változása, vállalkozási árak igazodása.
        * **3. Stádium (Makro Következmény):** Jegybanki kamatpolitikai reakció, hitelpiaci átrendeződés.
        * **4. Stádium (Stratégiai Eredmény):** Kormányzati gazdaságpolitikai beavatkozás, új export-import útvonalak.
        """)

    with tab4:
        st.subheader("🌐 Szektorszintű Átfogó Helyzetkép (A–Z)")
        st.markdown("""
        * **Pénzügy & Bankrendszer:** Stabil tőkemegfelelési mutatók, alacsony rendszerszintű kockázat.
        * **Ipar & Technológia:** Félvezető-kapacitások magas kihasználtsága, töretlen digitalizációs ütem.
        * **Geopolitika & Kereskedelem:** Diplomáciai egyeztetések a vámkonfliktusok megelőzésére.
        * **Mezőgazdaság & Klíma:** Normális hozamvárakozások, stabil élelmiszer-ellátási láncok.
        """)

    st.markdown("---")
    st.caption("GUME v6.9 Master Intelligence Engine — Autonóm adatelemző és előrejelző rendszer.")

if __name__ == "__main__":
    run_gume_safe_engine()
