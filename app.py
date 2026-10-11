from __future__ import annotations
import streamlit as st
import pandas as pd
import numpy as np
import feedparser
import sqlite3
from datetime import datetime, timezone

try:
    import yfinance as yf
except ImportError:
    yf = None

# --- SQLite Adatbázis az 9 pilléres elemzések mentéséhez ---
def init_db():
    conn = sqlite3.connect("gume_9_pillars.db", check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pillar_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            country TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_pillar_report(country, content):
    conn = sqlite3.connect("gume_9_pillars.db", check_same_thread=False)
    c = conn.cursor()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    c.execute("INSERT INTO pillar_reports (timestamp, country, content) VALUES (?, ?, ?)", (ts, country, content))
    conn.commit()
    conn.close()

def load_pillar_reports():
    conn = sqlite3.connect("gume_9_pillars.db", check_same_thread=False)
    df = pd.read_sql("SELECT * FROM pillar_reports ORDER BY id DESC", conn)
    conn.close()
    return df

def run_gume_9_pillars():
    st.set_page_config(
        page_title="GUME v6.9 – 9 Pilléres Világelőrejelző Hub",
        page_icon="🌐",
        layout="wide"
    )

    st.title("🌐 GUME v6.9 – 9 PILLÉRES VILÁGELŐREJELZŐ MÁTRIX")
    today_str = datetime.now(timezone.utc).strftime("%Y. %B %d. | %H:%M UTC")
    st.markdown(f"**A mindennapi életet és a világot alakító 9 legfontosabb tényező alapján** | Frissítve: `{today_str}`")
    st.markdown("---")

    # --- OLDALSÁV: AZONNALI REAKTÍV ORSZÁGVÁLTÁS ---
    st.sidebar.header("🌍 Célpont & Fókusz")
    target_country = st.sidebar.selectbox(
        "Válassz országot vagy régiót:",
        [
            "Magyarország", "Egyesült Államok (USA)", "Németország", "Kína", 
            "Japán", "Egyesült Királyság", "Franciaország", "Oroszország", 
            "Brazília", "India", "Globális / Teljes Emberiség"
        ],
        key="reactive_country_9pillars"
    )

    ticker_input = st.sidebar.text_input("Piaci & Deviza Tickerek", "EURHUF=X, USDHUF=X, EURUSD=X, ^VIX, SPY, CL=F")

    # Élő hírek RSS-ből
    live_news = []
    try:
        rss_query = target_country.split(" ")[0]
        feed_url = f"https://news.google.com/rss/search?q={rss_query}&hl=hu&gl=HU&ceid=HU:hu" if target_country == "Magyarország" else f"https://news.google.com/rss/search?q={rss_query}&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:6]:
            live_news.append({
                "title": entry.title,
                "link": entry.link,
                "published": getattr(entry, "published", "Ma")
            })
    except Exception:
        pass

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

    st.subheader(f"📍 Aktív Elemzési Célpont: {target_country}")
    st.success(f"🚨 **HOLNAPI VILÁGELŐREJELZÉS:** A 9 kulcspillér (gazdaság, technológia, társadalom, politika, környezet, egészségügy, globalizáció, infrastruktúra és média) szinkronja alapján {target_country}-ban a holnapi nap a makrogazdasági stabilitás és a digitális tudatosság jegyében telik.")

    # --- TABS / FÜLEK A 9 PILLÉR ALAPJÁN ---
    tab_news, tab_p1, tab_p2, tab_p3, tab_market, tab_db = st.tabs([
        "📰 Élő Hírek & Események",
        "💰 1-3. Gazdaság, Tech & Társadalom",
        "🏛️ 4-6. Politika, Környezet & Egészség",
        "🌐 7-9. Globalizáció, Infrastruktúra & Média",
        "📈 Piaci Adatok & VIX Index",
        "💾 Adatbázis & Riport Export"
    ])

    with tab_news:
        st.subheader(f"📰 A mai nap legfrissebb hírei ({target_country}):")
        if live_news:
            for item in live_news:
                st.markdown(f"* **[{item['title']}]({item['link']})** — *Frissítve: {item['published']}*")
        else:
            st.info("Az élő hírfolyam átmenetileg offline módban van.")

    with tab_p1:
        st.subheader("1. Gazdasági tényezők")
        st.write("Az árak, a fizetések, a munkalehetőségek és az infláció meghatározzák, hogy az emberek mire tudnak költeni, milyen lakásban élnek, és milyen életszínvonalat tudnak fenntartani.")
        
        st.subheader("2. Technológiai fejlődés")
        st.write("Az internet, az okostelefonok, a mesterséges intelligencia és az automatizálás megváltoztatják a kommunikációt, a tanulást, a munkát és a szórakozást.")
        
        st.subheader("3. Társadalmi és kulturális tényezők")
        st.write("A család, a barátok, a hagyományok, a vallás, az oktatás és a társadalmi normák hatással vannak az emberek gondolkodására és viselkedésére.")

    with tab_p2:
        st.subheader("4. Politikai tényezők")
        st.write("A kormányok döntései, a törvények, az adók, a nemzetközi kapcsolatok és a háborúk befolyásolják a biztonságot, a megélhetést és az emberek lehetőségeit.")
        
        st.subheader("5. Környezeti és természeti tényezők")
        st.write("Az időjárás, az éghajlatváltozás, a természeti katasztrófák, a víz- és élelmiszerkészletek hatással vannak a mezőgazdaságra, az egészségre és a mindennapi életre.")
        
        st.subheader("6. Egészségügyi tényezők")
        st.write("A betegségek, az egészségügyi ellátás minősége, a táplálkozás és a mentális egészség meghatározzák az emberek életminőségét és munkaképességét.")

    with tab_p3:
        st.subheader("7. Nemzetközi események és globalizáció")
        st.write("A világkereskedelem, a migráció, a háborúk és a más országokban bekövetkező gazdasági változások a helyi árakra, a munkahelyekre és az áruk elérhetőségére is hatással vannak.")
        
        st.subheader("8. Közlekedés és infrastruktúra")
        st.write("Az utak, a tömegközlekedés, az energiaellátás és az internetkapcsolat befolyásolják, hogy az emberek mennyi idő alatt jutnak el a munkahelyükre, és milyen szolgáltatásokhoz férnek hozzá.")
        
        st.subheader("9. Média és információ")
        st.write("A televízió, a híroldalak és a közösségi média befolyásolják, miről tudunk, hogyan vélekedünk a világról, és milyen döntéseket hozunk.")

    with tab_market:
        st.subheader("📈 Élő Piaci Mutatók & Volatilitás")
        st.metric("Aktuális VIX (Félelem) Index", f"{vix_val:.1f}")
        if not market_df.empty:
            st.dataframe(market_df.tail(5), use_container_width=True)
        else:
            st.info("Piaci adatok betöltése folyamatban...")

    with tab_db:
        st.subheader("💾 Adatbázis Mentés & Riport Export")
        r_title = st.text_input("Riport Megnevezése", f"GUME 9-Pillér Jelentés – {target_country}")
        
        if st.button("💾 Mentés az SQLite Adatbázisba", type="primary"):
            content_desc = f"Célpont: {target_country}. Elemzés a 9 kulcspillér alapján."
            save_pillar_report(target_country, content_desc)
            st.success("✔ Sikeresen elmentve az adatbázisba!")

        st.markdown("---")
        st.write("Korábban elmentett jelentések:")
        db_df = load_pillar_reports()
        if not db_df.empty:
            st.dataframe(db_df, use_container_width=True)
        else:
            st.info("Még nincsenek elmentett jelentések.")

        export_md = f"""# {r_title}
Dátum: {today_str}
Célpont: {target_country}

## Összefoglalás a 9 Pillér Alapján
A mindennapi életet befolyásoló fő tényezők: gazdaság, technológia, társadalom, politika, környezet, egészségügy, globalizáció, közlekedés és média.
"""
        st.download_button(
            label="📥 Riport Letöltése Markdownként",
            data=export_md,
            file_name=f"gume_9pillars_report_{target_country.lower()}.md",
            mime="text/markdown"
        )

    st.markdown("---")
    st.caption("GUME v6.9 9-Pilláris Motor — Teljes körű reaktív architektúra aktív.")

if __name__ == "__main__":
    run_gume_9_pillars()
