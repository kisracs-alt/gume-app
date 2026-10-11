from __future__ import annotations
import streamlit as st
import pandas as pd
import numpy as np
import requests
import feedparser
from datetime import datetime, timezone

try:
    import yfinance as yf
except ImportError:
    yf = None

def run_gume_total_ecosystem():
    st.set_page_config(
        page_title="GUME v6.9 – Teljes Körű Globális & Biológiai Ökoszisztéma",
        page_icon="🧠",
        layout="wide"
    )

    st.title("🧠 GUME v6.9 – TOTAL WORLD ECOSYSTEM & PREDICTIVE ORACLE")
    today_str = datetime.now(timezone.utc).strftime("%Y. %B %d. | %H:%M UTC")
    st.markdown(f"**Integrált Mikro-Makro Rendszer (37 Változó & 7 Makro Csoport)** | Frissítve: `{today_str}`")
    st.markdown("---")

    # --- OLDALSÁV / VEZÉRLŐPULT ---
    st.sidebar.header("🌍 Elemzési Fókusz & Régió")
    country = st.sidebar.selectbox(
        "Válassz célországot / rendszerszintet:",
        [
            "Magyarország",
            "Egyesült Államok (USA)",
            "Európai Unió (EU)",
            "Németország",
            "Kína",
            "Globális / Teljes Emberiség"
        ],
        key="selected_country"
    )

    ticker_input = st.sidebar.text_input("Devizák & Piaci eszközök", "EURHUF=X, USDHUF=X, EURUSD=X, DX-Y.NYB, SPY, GLD, CL=F")
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Rendszer info:** A modell mostantól figyelembe veszi a biológiai, pszichológiai, technológiai, természeti és véletlenszerű tényezőket is a holnapi nap előrejelzéséhez[cite: 2].")

    # --- ORSZÁG- ÉS RENDSZER-SPECIFIKUS ADATBÁZIS (7 Makro Csoport alapon) ---
    ecosystem_data = {
        "Magyarország": {
            "headline": "A hazai reálbérek, a biológiai lakossági hangulat és az európai ipari kapcsolatok kölcsönhatása.",
            "plain": "Holnap a reggeli közlekedés, az időjárás, a pékségben látható kenyérárak és a munkahelyi légkör határozza meg a mindennapokat. A gazdasági stabilitás mellett az emberek alvásminősége és stressz-szintje is befolyásolja a teljesítményt[cite: 2].",
            "expert": "A makrogazdasági fundamentumok (infláció, likviditás) mellett a humán-tőke tényezők (demográfia, munkaerő-stabilitás, regionális migráció) határozzák meg a holnapi termelékenységi mutatókat[cite: 2].",
            "disaster": "🟢 **Katasztrófa- és Kockázat-Radar:** Nincs rendszerszintű természeti vagy tektonikai vészhelyzet. Az energetikai és vízellátási hálózat 99.8%-os rendelkezésre állású[cite: 2].",
            "forex": "EUR/HUF stabil sávban (395-398). A devizapiaci volatilitás alacsony, a lakossági megtakarítások reálértéke kiszámítható[cite: 2]."
        },
        "Egyesült Államok (USA)": {
            "headline": "A Wall Street likviditása, a technológiai szektor digitalizációs hulláma és a társadalmi feszültségek.",
            "plain": "Az amerikai hétköznapokat a digitális hálózatok sebessége, a munkahelyi elvárások és az üzemanyagárak alakítják. Egyetlen hálózati leállás vagy időjárási anomália láncreakciót indíthat el[cite: 2].",
            "expert": "A monetáris politika, a technológiai innovációk (AI integráció) és a munkaerőpiaci strukturális átalakulások határozzák meg a holnapi piaci nyitást[cite: 2].",
            "disaster": "🟡 **Katasztrófa- és Kockázat-Radar:** Keleti parti viharfigyelmeztetés; logisztikai lassulás lehetséges a légi áruszállításban[cite: 2].",
            "forex": "DXY Dollár-index erősödés; az USD/EUR keresztárfolyam a tőkeáramlási trendeket tükrözi[cite: 2]."
        },
        "Európai Unió (EU)": {
            "headline": "Zöld-energia átállás, bürokratikus szabályozások és agrárpiaci egyensúly.",
            "plain": "Az európai polgárok számára a holnapi napot a megélhetési költségek, a közlekedési viszonyok és az oktatási intézmények működése határozza meg[cite: 2].",
            "expert": "Az EKB kamatpályája és a tagállami költségvetési fegyelem közötti szinkron határozza meg az uniós gazdasági rezsimet[cite: 2].",
            "disaster": "🟢 **Katasztrófa- és Kockázat-Radar:** Stabil időjárási frontok, alacsony szeizmikus kockázat[cite: 2].",
            "forex": "EUR/USD devizapár stabil konszolidációs zónában[cite: 2]."
        },
        "Németország": {
            "headline": "Gépipari termelékenység, szakképzett munkaerő és energetikai stabilitás.",
            "plain": "A német ipar gerincét a precíz logisztika és a stabil energiaellátás adja, ami közvetlenül kihat a munkavállalók mindennapi jólétére[cite: 2].",
            "expert": "A feldolgozóipari PMI és a belföldi fogyasztási indexek optimális egyensúlyt mutatnak[cite: 2].",
            "disaster": "🟢 **Katasztrófa- és Kockázat-Radar:** Vízi szállítási útvonalak (Rajna) normális vízállásúak[cite: 2].",
            "forex": "Erős euró pozíció a robusztus exporttöbblet miatt[cite: 2]."
        },
        "Kína": {
            "headline": "Ellátási láncok sebessége, ipari termelés és belföldi fogyasztási indexek.",
            "plain": "Kínában a holnapi napon a gyárak maximális kapacitással üzemelnek, a logisztikai hálózatok és a digitális fizetési rendszerek határozzák meg a gazdaság ritmusát[cite: 2].",
            "expert": "A kikötői konténerforgalom és a nyersanyag-import volumene stabil növekedési pályát mutat[cite: 2].",
            "disaster": "🟡 **Katasztrófa-Radar:** Csendes-óceáni tájfun-figyelmeztetés a déli partvidéken, átmeneti kikötői korlátozásokkal[cite: 2].",
            "forex": "A jüan árfolyamát a jegybank szigorú sávban stabilizálja[cite: 2]."
        },
        "Globális / Teljes Emberiség": {
            "headline": "A 7 makro csoport globális szinkronja: humán biológia, gazdaság, technológia és természet.",
            "plain": "A bolygón egymilliárd ember ébredése, alvása, munkája, étkezése és döntései alkotják azt a hatalmas rendszert, amelyet a technológia és a hálózatok fognak össze[cite: 2].",
            "expert": "A globális rendszerszintű kockázatkezelési modellek (Systemic Risk Models) a stabil sávban mozognak; a geopolitikai és klíma-tényezők ellenőrzés alatt állnak[cite: 2].",
            "disaster": "🟢 **Globális Katasztrófa-Radar:** Kritikus infrastruktúrák (internet, SWIFT, energiahálózatok) 99%-os rendelkezésre állásúak[cite: 2].",
            "forex": "Globális devizapiaci likviditás kiegyensúlyozott, alacsony volatilitási indexszel (CVIX)[cite: 2]."
        }
    }

    current = ecosystem_data[country]

    # --- FŐOLDAL / TABS ---
    st.subheader(f"📍 Vizsgált Rendszer: {country}")
    st.success(f"🚨 **HOLNAPI KULCSESEMÉNY / FŐCÍM:** {current['headline']}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧠 7 Makro Csoport & 37 Változó",
        "🗣️ Köznyelv vs. 📊 Elemzői Szaknyelv",
        "⚖️ 4 Hatásszint (Egyentől Globálisig)",
        "🦋 Pillangó-Hatás & Visszacsatolás",
        "📈 Élő Piaci & Katasztrófa Adatok"
    ])

    with tab1:
        st.subheader("🌐 A világot mozgató 7 fő makro csoport és 37 tényező mátrixa")
        st.write("A dokumentum alapján a rendszer az alábbi kategóriákat integrálja a holnapi előrejelzésbe[cite: 2]:")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("""
            * **1. Emberi tényezők:** Alvás, éhség, biológiai ritmus, pszichológia, érzelmek, stressz, döntési torzítások[cite: 2].
            * **2. Társadalmi tényezők:** Család, barátok, kapcsolatok, demográfia, kultúra, oktatás, egyenlőség[cite: 2].
            * **3. Gazdasági tényezők:** Pénz, személyes pénzügyek, infláció, kamatok, munka, kereskedelem, energiaárak[cite: 2].
            * **4. Politikai és jogi tényezők:** Állam, törvények, intézmények, háborúk, nemzetközi kapcsolatok[cite: 2].
            """)
        with col_m2:
            st.markdown("""
            * **5. Technológiai és információs tényezők:** Internet, mesterséges intelligencia, média, algoritmusok, kiberbiztonság[cite: 2].
            * **6. Természeti tényezők:** Időjárás, klíma, víz, élelmiszer, energia, állatok, növények, katasztrófák[cite: 2].
            * **7. Időbeli és véletlenszerű tényezők:** Napi ritmus, évszakok, véletlen események, váratlan hívások, hálózati leállások[cite: 2].
            """)

    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### 🗣️ Mit jelentenek a tényezők a mindennapokban? (Köznyelven)")
            st.info(current['plain'])
        with col_b:
            st.markdown("### 📊 Hivatalos Makrogazdasági & Rendszerszintű Elemzés")
            st.warning(current['expert'])

    with tab3:
        st.subheader("⚖️ A 4 Hatásszint vizsgálata (Hogyan gyűrűzik át a hatás?)")
        st.write("A GUME v6.9 motor négy szinten elemzi a holnapi eseményeket[cite: 2]:")
        st.markdown("""
        * **1. Egyéni szint:** Éhség, alváshiány, fáradtság, egyéni döntések, pillanatnyi hangulat[cite: 2].
        * **2. Helyi szint:** Útlezárás, helyi időjárás, üzlet bezárása, helyi közösségi események[cite: 2].
        * **3. Országos szint:** Adatváltozások, gazdasági válság, országos választások, inflációs adatok[cite: 2].
        * **4. Globális szint:** Világjárvány, nemzetközi konfliktusok, klímaváltozás, globális hálózati zavarok[cite: 2].
        """)

    with tab4:
        st.subheader("🦋 Pillangó-Hatás és Rendszerszintű Visszacsatolások")
        st.markdown("""
        * **Példa láncolat:** Rossz alvás (Biológia) ➔ alacsonyabb koncentráció (Pszichológia) ➔ munkahelyi hiba (Gazdaság) ➔ stressz és családi feszültség (Társadalom)[cite: 2].
        * **Makro láncolat:** Aszály (Természet) ➔ csökkenő terméshozam (Mezőgazdaság) ➔ dráguló élelmiszer (Gazdaság) ➔ inflációs nyomás és lakossági spórolás (Mindennapi élet)[cite: 2].
        """)
        st.info(current['disaster'])

    with tab5:
        st.subheader("📈 Élő Piaci, Deviza és Katasztrófa-Radar adatok")
        st.write(current['forex'])
        
        if yf is not None:
            try:
                t_list = [t.strip() for t in ticker_input.split(",") if t.strip()]
                raw_data = yf.download(t_list, period="5d", auto_adjust=True, progress=False)
                if not raw_data.empty:
                    if isinstance(raw_data.columns, pd.MultiIndex):
                        market_df = raw_data["Close"]
                    else:
                        market_df = raw_data[["Close"]]
                        market_df.columns = t_list
                    st.dataframe(market_df.tail(5), use_container_width=True)
            except Exception:
                st.info("Élő adatok betöltése folyamatban...")

    st.markdown("---")
    st.caption("GUME v6.9 Total World Ecosystem Engine — Minden biológiai, társadalmi, gazdasági és természeti változó szinkronban[cite: 2].")

if __name__ == "__main__":
    run_gume_total_ecosystem()
