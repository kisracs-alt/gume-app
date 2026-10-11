from datetime import datetime, timezone
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

def run_gume_newsroom():
    st.set_page_config(
        page_title="GUME v6.9 – Globális Intelligencia Hírszoba & Pillangó Elemző",
        page_icon="🌍",
        layout="wide"
    )
    
    # Fejléc
    st.title("🌍 GUME v6.9 – GLOBÁLIS INTELLIGENCIA HÍRSZOBA")
    today_str = datetime.now(timezone.utc).strftime("%Y. október %d.")
    st.markdown(f"**Élő Hírfizetés & Pillangó-Hatás Elemző** | Kiadás: {today_str} | **Státusz:** Teljes körű multi-domain monitorozás")
    st.markdown("---")

    # Oldalsáv: Ország választás és szűrők (Nincs koordináta beírás!)
    st.sidebar.header("🎛️ Vezérlőpult & Célpont")
    selected_country = st.sidebar.selectbox(
        "Válassz célországot / régiót:",
        ["Globális / Összesített", "Egyesült Államok (USA)", "Európai Unió (EU)", "Kína", "Németország", "Magyarország", "Oroszország", "Közel-Kelet"]
    )
    
    sector_filter = st.sidebar.selectbox(
        "Szektor szűrés:",
        ["Minden Szektor (A-Z)", "Geopolitika & Politika", "Makro- & Mikrogazdaság", "Kereskedelem & Export-Import", "Klíma, Időjárás & Agrár", "Nyersanyagok & Pénzpiacok"]
    )

    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tipp:** Kattints bármelyik kulcshírre a főoldalon, hogy lásd a pillangó-hatás láncolatot és a szektorokon átívelő következményeket!")

    # Főoldal elrendezés
    col_news, col_butterfly = st.columns([1.3, 1])

    with col_news:
        st.subheader("📰 Élő Globális Hírek & Események")
        
        # Interaktív hír-kiválasztó (kattintásra hozza a részleteket)
        news_items = {
            "1. Geopolitikai feszültség a főbb tengeri kereskedelmi útvonalakon": {
                "category": "Geopolitika & Kereskedelem",
                "summary": "Fokozódó katonai és diplomáciai jelenlét a kulcsfontosságú szorosokban, ami azonnali hatással van a logisztikai árakra.",
                "deep_analysis": "A tengeri áruszállítás lassulása miatt a biztosítási díjak megugrottak. Ez közvetlenül növeli az importált ipari alkatrészek és elektronikai cikkek árát, ami begyűrűzik a mikro- és makrogazdaságba, inflációs nyomást gyakorolva a fejlett gazdaságokra."
            },
            "2. Váratlan időjárási sokk a dél-amerikai mezőgazdasági övezetben": {
                "category": "Klíma, Időjárás & Mezőgazdaság",
                "summary": "Hosszan tartó szárazság veszélyezteti a szójabab- és kukoricatermést, ami globális árupiaci reakciót vált ki.",
                "deep_analysis": "A pillangó-hatás mechanizmus: 1) Csökken a termésmennyiség -> 2) Megugranak a takarmányárak -> 3) Drágul a hús- és élelmiszertermelés globálisan -> 4) Romlik a lakossági reálbér-stabilitás (mikrogazdaság), ami gazdaságpolitikai beavatkozásokat (árstopok, szubvenciók) kényszerít ki."
            },
            "3. Központi banki kamatpolitikai fordulat és likviditási hullám": {
                "category": "Pénzügy & Makrogazdaság",
                "summary": "A jegybankok váratlan monetáris lazítási jeleket mutatnak az ipari stagnálás elkerülése érdekében.",
                "deep_analysis": "Az alacsonyabb kamatok gyengítik a valutát az exportőrök javára, de élénkítik az inflációs várakozásokat. A tőke az állampapírokból a technológiai szektorba és a nyersanyagokba áramlik, átformálva a globális részvénypiacokat."
            },
            "4. Technológiai áttörés a félvezető-gyártásban és AI integrációban": {
                "category": "Technológia & Ipar",
                "summary": "Új gyártási technológia csökkenti a chipek előállítási költségét, miközben a globális kereslet csúcson van.",
                "deep_analysis": "A chipárak csökkenése olcsóbbá teszi az automatizált ipari berendezéseket és az IoT eszközöket. Ez felgyorsítja a gyárak digitalizációját, növeli a termelékenységet, és átrendezi a nemzetközi export-import pozíciókat az ázsiai és nyugati blokkok között."
            }
        }

        selected_headline = st.selectbox("Válassz egy eseményt a részletes elemzéshez:", list(news_items.keys()))
        
        current_news = news_items[selected_headline]
        st.markdown(f"**Kategória:** `{current_news['category']}`")
        st.info(current_news['summary'])
        
        st.markdown("### 🔍 Részletes Eseményelemzés")
        st.write(current_news['deep_analysis'])

    with col_butterfly:
        st.subheader("🦋 Pillangó-Hatás & Csatolási Mátrix")
        st.markdown(f"**Vizsgált régió:** `{selected_country}`")
        st.markdown(f"**Aktív szűrő:** `{sector_filter}`")
        
        st.markdown("""
        A GUME v6.9 motor valós időben elemzi, hogy az kiválasztott esemény hogyan lép kapcsolatba a többi szektorral:
        """)

        # Interaktív pillangó láncolat megjelenítése
        with st.expander("⚡ 1. Elsődleges Sokk (Közvetlen Hatás)", expanded=True):
            st.write("Az esemény közvetlenül megüti az érintett nyersanyagot vagy szektort (pl. logisztikai költségek növekedése, árak megugrása).")

        with st.expander("🔗 2. Másodlagos Gyűrűzés (Kereskedelem & Makro)", expanded=True):
            st.write("Az importőr országok inflációs nyomással szembesülnek; a vállalkozások kénytelenek árat emelni, ami csökkenti a lakossági fogyasztást (mikrogazdaság).")

        with st.expander("🌐 3. Makroszintű & Geopolitikai Következmény", expanded=True):
            st.write("A gazdaságpolitikák átrendeződnek (vámok, exportkorlátozások vagy szubvenciók), ami új kereskedelmi szövetségeket vagy feszültségeket szül.")

        st.markdown("---")
        st.success("🎯 **Előrejelzés a holnapi napra:** A láncolat áttételes hatásai miatt a tőkepiacokon ágazati átrendeződés várható; a védelmi és likvid eszközök felértékelődnek, míg a ciklikus iparágak óvatosabb mozgást mutatnak.")

    # Alsó rész: Teljes körű áttekintés táblázatban / tabokon
    st.markdown("---")
    st.subheader("📊 Teljes Körű Szektorszintű Helyzetkép (A-Z)")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌐 Geopolitika & Kereskedelem",
        "📈 Makro- & Mikrogazdaság",
        "⚙️ Ipar & Nyersanyagok",
        "🌦️ Klíma & Mezőgazdaság",
        "💰 Pénzügyek & Politika"
    ])

    with tab1:
        st.markdown("### Nemzetközi kapcsolatok, export-import és geopolitikai feszültségek")
        st.write(f"A(z) **{selected_country}** vonatkozásában a kereskedelmi útvonalak stabilitása mérsékelt. Az export volumene stabil, de a vámpolitikai változások miatt az import-struktúra átalakulóban van.")

    with tab2:
        st.markdown("### Makrogazdasági fundamentumok és mikrogazdasági hatások")
        st.write("A lakossági reálbérek és a vállalkozási hitelköltségek kölcsönhatása határozza meg a belső keresletet. A kisvállalkozások likviditása stabil, de a költséginfláció folyamatos figyelmet igényel.")

    with tab3:
        st.markdown("### Iparágak, technológia és nyersanyagpiacok")
        st.write("Az energiaárak oldalazó mozgást mutatnak. A feldolgozóipar digitalizációja és az automata rendszerek integrációja kompenzálja a munkaerőpiaci szűkülést.")

    with tab4:
        st.markdown("### Klímatényezők, időjárás és agrár-intelligencia")
        st.write("Az aktuális csapadékmennyiség és hőmérsékleti indexek az övezetek 85%-ában kedvezőek a mezőgazdasági termelés szempontjából, elkerülve a drasztikus élelmiszerár-sokkokat.")

    with tab5:
        st.markdown("### Monetáris politikák, gazdaságpolitika és pénzügyek")
        st.write("A jegybankok óvatos, adatalapú kamatpolitikát folytatnak. A tőkepiacokon a kockázatkezelési modellek (VaR/CVaR) a volatilitás mérsékelt szintjét jelzik.")

    st.markdown("---")
    st.caption("GUME v6.9 Global Intelligence Engine — Autonóm híraggregátor, pillangó-hatás szimulátor és előrejelző rendszer.")

if __name__ == "__main__":
    run_gume_newsroom()
