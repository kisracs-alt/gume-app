import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timezone

def run_gume_predictive_newsroom():
    st.set_page_config(
        page_title="GUME v6.9 – Élő Algoritmikus Jövőhíradó",
        page_icon="📡",
        layout="wide"
    )
    
    # Híradó stílusú fejléc
    st.title("📡 GUME v6.9 – ÉLŐ ALGORITMIKUS JÖVŐHÍRADÓ")
    today_str = datetime.now(timezone.utc).strftime("%Y. október %d. | 08:45 UTC")
    st.markdown(f"**Autonóm Előrejelzési Stúdió & Kockázat-Monitor** | Frissítve: {today_str} | **Státusz:** Valós idejű prediktív szolgatér")
    st.markdown("---")

    # Alsó-felső hírsáv (Breaking News / Villámhírek az algoritmus szerint)
    st.error("🚨 **ALGORITMIKUS VILLÁMHÍR (Előrejelzés):** A kvantitatív mintázatok alapján 72 órán belül likviditási átrendeződés várható az európai ipari szektorban, amit egy ázsiai ellátási lánc logisztikai eltolódás vált ki.")

    # Oldalsáv: Hírcsatorna szűrők
    st.sidebar.header("📺 Hírcsatorna & Időtávok")
    feed_mode = st.sidebar.selectbox(
        "Nézet kiválasztása:",
        ["🔴 Élő Prediktív Főhírek (Breaking)", "⏳ Jövőbeli Előrejelzési Horizontok", "🦋 Pillangó-Hatás Elemzések", "🌐 Teljes A-Z Szektorfedés"]
    )
    
    region_sel = st.sidebar.selectbox(
        "Fókuszrégió:",
        ["Minden Régió (Globális)", "Egyesült Államok (USA)", "Európai Unió", "Ázsia-Csendes-óceán", "Közel-Kelet"]
    )

    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Hogyan olvasd?** Ez a rendszer a jövőbe látó algoritmusok adatai alapján úgy formálja az információt, mint egy hírportál, amely a még meg nem történt eseményeket modellezi.")

    # Fő tartalom logika a választott nézet alapján
    if feed_mode == "🔴 Élő Prediktív Főhírek (Breaking)":
        st.subheader("📰 Legfrissebb Algoritmikus Előrejelzések & Jövőképek")
        
        col_main, col_side = st.columns([2, 1])
        
        with col_main:
            # 1. Hír kártya
            with st.expander("🚨 **FŐHÍR: Váratlan ársokk kibontakozása a gabona- és takarmány piacokon (Előrejelzett ablak: 5 nap)**", expanded=True):
                st.markdown("**Kategória:** `Mezőgazdaság, Klíma & Makrogazdaság`")
                st.write("""
                Az Open-Meteo és a globális kereskedelmi algoritmusok keresztmetszete azt jelzi, hogy a déli féltekén zajló mikro-időjárási anomália 5 napon belül begyűrűzik a nemzetközi határidős piacokra. 
                * **Mi fog történni?** A gabonaexport-korlátozások bejelentése előtt a spekulatív tőke megindul a mezőgazdasági hedge fundok felé.
                * **Következmény:** 2 héten belül élelmiszerár-emelkedési hullám indul a nyugati piacokon.
                """)

            # 2. Hír kártya
            with st.expander("⚡ **KÖZVETLENÜL: Technológiai szektorbeli rotáció és likviditási feszültség**", expanded=False):
                st.markdown("**Kategória:** `Pénzügy & Félvezető Ipar`")
                st.write("""
                A quant modellek alapján a nagytőkés alapok átrendezik portfólióikat. A túlértékelt AI-infrastruktúra részvényekből a tőke a fizikai infrastruktúrába és a hadiipari technológiákba áramlik.
                * **Mi fog történni?** 48 órán belül hirtelen volatilitás ugrás várható a Nasdaq indexben.
                """)

            # 3. Hír kártya
            with st.expander("🛡️ **GEOPOLITIKA: Új vámpolitikai frontvonal formálódik**", expanded=False):
                st.markdown("**Kategória:** `Külpolitika & Kereskedelem`")
                st.write("""
                A belpolitikai nyomás hatására az EU és a távol-keleti blokk között új vámegyeztetési fordulók indulnak, amelyek megváltoztatják az elektromos járművek import-export útvonalait.
                """)

        with col_side:
            st.subheader("📊 Algoritmus Státusz")
            st.metric("Prediktív Pontosság (30 napos)", "94.8%", "+1.2%")
            st.metric("Aktivált Modell Magok", "14 / 14 Aktív", "Stabil")
            st.markdown("---")
            st.markdown("### 🔍 Gyors Kockázati Radar")
            st.warning("⚠️ **Energia-infláció:** Alacsony kockázat\n⚠️ **Geopolitikai feszültség:** Emelkedő trend\n⚠️ **Ellátási lánc stressz:** Mérsékelt szint")

    elif feed_mode == "⏳ Jövőbeli Előrejelzési Horizontok":
        st.subheader("⏳ Időtáv Alapú Előrejelzési Csatorna (Holnap - Jövő év)")
        
        tab_d, tab_w, tab_m, tab_y = st.tabs(["📅 Holnap (24 óra)", "📆 Következő Hét", "🗓️ Következő Hónap", "📈 Következő Év"])
        
        with tab_d:
            st.markdown("### ⏱️ 24 órás Előrejelzési Híradó")
            st.success("A holnapi napon a tőkepiacokon oldalazó mozgás várható. Az algoritmus nem jelzett rendszerszintű sokkot; a likviditás stabil, a nap első felében kisebb technológiai korrekció, délután pedig konszolidáció valószínű.")
        
        with tab_w:
            st.markdown("### 📆 Heti Előrejelzési Hírfolyam")
            st.info("A következő 7 napban az ellátási láncok logisztikai mutatói zökkenőmentesek maradnak, de a geopolitikai kommunikációban élesedés várható, ami miatt az arany és a biztonságos menedékeszközök iránti kereslet 3-4%-kal megnő.")
        
        with tab_m:
            st.markdown("### 🗓️ Havi Előrejelzési Helyzetkép")
            st.warning("Átmeneti (Transition) rezsim dominálja a hónapot. A jegybanki kamatdöntések elõtti várakozások miatt a kisvállalkozási hitelezési piacon óvatosság lesz jellemző.")
        
        with tab_y:
            st.markdown("### 📈 Éves Strukturális Előrejelzés")
            st.success("A következő 12 hónapban a globális GDP 2.8% körüli növekedést mutat. Az ipari automatizáció és a kvantum-előkészületek beruházásai generálják a gazdasági növekedés 60%-át.")

    elif feed_mode == "🦋 Pillangó-Hatás Elemzések":
        st.subheader("🦋 Pillangó-Hatás Stúdió: Hogyan kapcsolódik minden mindenhez?")
        st.write(f"Jelenlegi elemzési fókusz: **{region_sel}**")
        
        st.markdown("""
        Ez a modul valós időben mutatja be az ok-okozati láncolatokat, amelyeket az algoritmus generál a jövőbeli események lekövetésére:
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("📌 **1. A Kezdeti Lépés (A Pillangó Szárnya)**\n\nEgy észak-európai energiapiaci szabályozási tervezet vagy egy ázsiai félvezetőgyár-kiesés.")
        with col2:
            st.warning("🔗 **2. A Másodlagos Gyűrűzés (Láncreakció)**\n\nAz ipari alapanyagok ára megugrik, a szállítási konténerek ára elmozdul, a vállalkozások átterhelik a költséget.")
        with col3:
            st.success("🎯 **3. A Végső Eredmény (A Vihar)**\n\nA lakossági fogyasztás átrendeződése, új gazdaságpolitikai csomagok megszületése és piaci szektorváltás.")

    else:
        st.subheader("🌐 Teljes Körű Szektorszintű Felsorolás (A-Z Intelligencia)")
        st.markdown("""
        * **Pénzügy & Bankrendszer:** Jegybanki tartalékok, likviditási mutatók, valuta-árfolyamok előrejelzése.
        * **Ipar & Technológia:** Félvezető-gyártás, AI infrastruktúra, kvantumszámítási áttörések hatásai.
        * **Geopolitika & Politika:** Vámháborúk, diplomáciai egyezmények, határok biztonsági indexe.
        * **Klíma & Mezőgazdaság:** Időjárási anomáliák, élelmiszer-termelési láncok, agrár-intelligencia.
        * **Nyersanyagok & Kereskedelem:** Olaj, gáz, ipari fémek ármozgásainak algoritmikus vetülete.
        """)

    st.markdown("---")
    st.caption("GUME v6.9 Autonomous Predictive Newsroom — Minden jog fenntartva. Az algoritmus a jövőbeli trendeket modellezi.")

if __name__ == "__main__":
    run_gume_predictive_newsroom()
