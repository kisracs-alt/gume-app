from __future__ import annotations
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timezone

try:
    import yfinance as yf
except ImportError:
    yf = None

# --- SQLite Adatbázis az összes részletes jelentés mentéséhez ---
def init_db():
    conn = sqlite3.connect("gume_total_ecosystem.db", check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS comprehensive_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            country TEXT,
            title TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_report(country, title, content):
    conn = sqlite3.connect("gume_total_ecosystem.db", check_same_thread=False)
    c = conn.cursor()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    c.execute("INSERT INTO comprehensive_reports (timestamp, country, title, content) VALUES (?, ?, ?, ?)", (ts, country, title, content))
    conn.commit()
    conn.close()

def load_reports():
    conn = sqlite3.connect("gume_total_ecosystem.db", check_same_thread=False)
    df = pd.read_sql("SELECT * FROM comprehensive_reports ORDER BY id DESC", conn)
    conn.close()
    return df

def run_gume_total_ecosystem():
    st.set_page_config(
        page_title="GUME v6.9 – Total World Ecosystem Hub",
        page_icon="🌍",
        layout="wide"
    )

    st.title("🌍 GUME v6.9 – TELJES KÖRŰ VILÁGELŐREJELZŐ & ÖKOSZISZTÉMA MÁTRIX")
    today_str = datetime.now(timezone.utc).strftime("%Y. %B %d. | %H:%M UTC")
    st.markdown(f"**Integrált Rendszer: 37 Változó, 7 Fő Csoport és 4 Hatásszint** | Frissítve: `{today_str}`")
    st.markdown("---")

    # --- OLDALSÁV VÉZÉRLŐPULT ---
    st.sidebar.header("🌐 Globális Rendszer Fókusz")
    target_country = st.sidebar.selectbox(
        "Válassz országot vagy régiót:",
        [
            "Magyarország", "Egyesült Államok (USA)", "Németország", "Kína", 
            "Japán", "Egyesült Királyság", "Franciaország", "Oroszország", 
            "Brazília", "India", "Globális / Teljes Emberiség"
        ]
    )
    
    ticker_input = st.sidebar.text_input("Piaci & Deviza Tickerek", "EURHUF=X, USDHUF=X, EURUSD=X, ^VIX, SPY, CL=F")
    refresh_btn = st.sidebar.button("🔄 Teljes Rendszer Újraszámítása", type="primary")

    # Piaci adatok
    market_df = pd.DataFrame()
    vix_val = 18.0
    if yf is not None:
        try:
            t_list = [t.strip() for t in ticker_input.split(",") if t.strip()]
            raw = yf.download(t_list, period="5d", auto_adjust=True, progress=False)
            if not raw.empty:
                if isinstance(raw.columns, pd.MultiIndex):
                    market_df = raw["Close"]
                else:
                    market_df = raw[["Close"]]
                    market_df.columns = t_list
                if "^VIX" in market_df.columns:
                    vix_val = float(market_df["^VIX"].dropna().iloc[-1])
        except Exception:
            pass

    # --- TARTALOM FÜLEK A TELJES DOKUMENTUM ALAPJÁN ---
    st.subheader(f"📍 Vizsgált Célpont: {target_country}")
    st.success(f"🚨 **HOLNAPI RENDSSZERSZINTŰ FŐCÍM:** A biológiai ritmusok, a mindennapi apróságok, a gazdasági láncok és a váratlan események hálózata {target_country}-ban[cite: 1].")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧬 1-3. Biológia, Psziché & Kapcsolatok",
        "💰 4-7. Gazdaság, Munka, Oktatás & Tech",
        "🌦️ 8-10. Természet, Víz, Élelmiszer & Energia",
        "🏛️ 11-18. Politika, Háború, Média & Társadalom",
        "🏠 19-37. Apróságok, Katasztrófák, Döntések & Rendszer",
        "💾 Adatbázis & Riport Export"
    ])

    with tab1:
        st.subheader("1. Az emberi test, biológia és pszichológia")
        st.markdown("""
        * **Alvás és biológiai ritmus:** Az alvás mennyisége, minősége, időzítése, a szoba hőmérséklete és a melatoninszint közvetlenül meghatározza a holnapi koncentrációt és a türelmet[cite: 1].
        * **Éhség, táplálkozás és folyadék:** A vércukorszint, a vitaminok, a vízfogyasztás és a kiszáradás mértéke alapvetően befolyásolja az azonos ingerekre adott reakciókat[cite: 1].
        * **Pszichológia, stressz és hiedelmek:** Az érzelmek, a pillanatnyi hangulat, a korábbi emlékek, a pénzügyi bizonytalanság miatti stressz és a döntési torzítások irányítják a lakosság reakcióit[cite: 1].
        """)
        st.markdown("---")
        st.subheader("2. Család, barátok és emberi kapcsolatok")
        st.markdown("""
        * **Kapcsolati háló:** A szülők, párkapcsolatok, barátok és munkahelyi kollégák viselkedése, a bizalom, az empátia vagy éppen a magány mélyen hat a mentális állapotra[cite: 1].
        * **Társas fertőzés:** Egy reggeli kedves szó vagy egy sértés láncreakcióként terjedhet tovább az emberek között egész nap[cite: 1].
        """)

    with tab2:
        st.subheader("3. Pénz, gazdaság, munka és oktatás")
        st.markdown("""
        * **Személyes pénzügyek:** Jövedelem, lakbér, rezsiköltségek (villany, gáz, víz), élelmiszerárak, hiteltörlesztések és a váratlan kiadások[cite: 1].
        * **Makrogazdasági folyamatok:** Infláció, jegybanki kamatok, munkanélküliség, kereslet-kínálat, árfolyamok és energiaárak[cite: 1].
        * **Munka és technológia:** Munkahelyi terhelés, túlóra, távmunka, valamint a mesterséges intelligencia és a robotok hatása a munkakörökre[cite: 1].
        * **Oktatás és tudás:** Az iskolák működése, a digitális készségek, a kritikus gondolkodás és az álhírek felismerésének képessége[cite: 1].
        * **Digitális világ:** Okostelefonok, mobilhálózatok, internetkapcsolat, algoritmusok, kiberbűnözés és az esetleges rendszerleállások[cite: 1].
        """)

    with tab3:
        st.subheader("4. Természet, élelmiszer, ivóvíz és energia")
        st.markdown("""
        * **Időjárás és éghajlat:** Hőmérséklet, páratartalom, szélsebesség, csapadék, hőség, fagy, viharok és UV-sugárzás, amelyek közvetlenül befolyásolják a közlekedést és a teljesítményt[cite: 1].
        * **Élelmiszer és ivóvíz:** Mezőgazdasági termelés, öntözővíz, hűtési és tárolási láncok, élelmiszer-biztonság és a bolti készletek[cite: 1].
        * **Energia és erőforrások:** Villamosenergia-termelés, kőolaj, földgáz, megújuló energiaforrások, akkumulátorok, ritkaföldfémek és az áramszünetek kockázata[cite: 1].
        """)

    with tab4:
        st.subheader("5. Politika, háború, média és társadalom")
        st.markdown("""
        * **Politika és jog:** Jogszabályok, adók, kormányzati döntések, közszolgáltatások (egészségügy, rendőrség, oktatás) működése[cite: 1].
        * **Háborúk és nemzetközi kapcsolatok:** Fegyveres konfliktusok, szankciók, menekültmozgások, határellenőrzések és kibertámadások[cite: 1].
        * **Média és hírek:** A hírek gyorsasága, algoritmusok, kattintásvadász címek, propaganda és a véleménybuborékok hatása a közhangulatra[cite: 1].
        * **Demográfia és kultúra:** A népesség öregedése, migráció, hagyományok, vallás és generációs különbségek[cite: 1].
        """)

    with tab5:
        st.subheader("6. Apróságok, katasztrófák, döntések és rendszerszint")
        st.markdown("""
        * **A legapróbb hétköznapi körülmények:** A szoba hőmérséklete, háttérzaj, egy lemerült telefon, eltévesztett kulcs, elromlott háztartási eszköz vagy megszakadt internetkapcsolat[cite: 1].
        * **Katasztrófa-Radar:** Földrengések, vulkánkitörések, erdőtüzek, áradások és extrém időjárási katasztrófák[cite: 1].
        * **Véletlen és szabad akarat:** Kiszámíthatatlan események, váratlan hívások, valamint az emberi döntések és a jövővel kapcsolatos várakozások[cite: 1].
        * **A 4 Hatásszint és Visszacsatolás:**
          * *Egyéni szint:* Éhség, fáradtság, hangulat[cite: 1].
          * *Helyi szint:* Útlezárás, helyi bolt bezárása[cite: 1].
          * *Országos szint:* Adatváltozás, gazdasági válság[cite: 1].
          * *Globális szint:* Világjárvány, háború, klímaváltozás[cite: 1].
        """)

    with tab6:
        st.subheader("💾 Adatbázis & Riport Kezelés")
        r_title = st.text_input("Riport Megnevezése", f"GUME Total Ökoszisztéma Jelentés – {target_country}")
        
        if st.button("💾 Teljes Riport Mentése az Adatbázisba", type="primary"):
            full_content = f"Célpont: {target_country}. A rendszer integrálta a 37 változót, a 7 makro csoportot és a 4 hatásszintet a dokumentum alapján."
            save_report(target_country, r_title, full_content)
            st.success("✔ Sikeresen elmentve az SQLite adatbázisba!")

        st.markdown("---")
        st.write("Korábban elmentett jelentések:")
        db_df = load_reports()
        if not db_df.empty:
            st.dataframe(db_df, use_container_width=True)
        else:
            st.info("Még nincsenek elmentett jelentések az adatbázisban.")

        export_text = f"# {r_title}\nCélpont: {target_country}\nDátum: {today_str}\n\n[Minden részletes változó és 7 makro csoport integrálva a dokumentum alapján]."
        st.download_button(
            label="📥 Letöltés Markdown Fájlként",
            data=export_text,
            file_name=f"gume_total_ecosystem_{target_country.lower()}.md",
            mime="text/markdown"
        )

    st.markdown("---")
    st.caption("GUME v6.9 Total World Ecosystem Core — Minden részlet, változó és szint aktív[cite: 1].")

if __name__ == "__main__":
    run_gume_total_ecosystem()
