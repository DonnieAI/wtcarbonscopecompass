import streamlit as st

st.set_page_config(page_title="projects", layout="wide")
from utils import apply_style_and_logo
apply_style_and_logo()


st.title("EU Emission Trading System [EU-ETS] ")
st.markdown("""
            ### 📖 IU Emission Trading System [EU-ETS]
            
            """)
st.markdown(""" 
            source: EU, ICAP""") 

# Create a download button


st.markdown(
    """
    # 🌍 General Introduction  

    - 🏛️ **Operational since 2005** → EU ETS is the oldest and largest cap-and-trade system in the world.  
    - 📉 **Covers ~40% of EU emissions** → includes power, industry, aviation, and (from 2024) maritime transport.  
    - ✈️ **Aviation & Maritime Updates (2024)** → now includes most EU flights and shipping.  
    - 🔄 **Trading Phases** → currently in *Phase IV (2021–2030)*.  
    - 💶 **Allowance Distribution** → mainly auctioning, with some free allocation to prevent carbon leakage.  
    - 🌱 **Revised in 2023 under the European Green Deal** with:  
        - 📦 Expanded scope → maritime + new ETS2 (buildings, road transport, others from 2027/28).  
        - ⚖️ Stronger Market Stability Reserve (MSR).  
        - 🛫 Updated aviation rules.  
        - 🚢 Stricter monitoring/reporting for maritime transport.  
        - 🏦 Social Climate Fund (from 2026, linked to ETS2).  
        - 🌐 Carbon Border Adjustment Mechanism (CBAM) → gradually replaces free allocation.  
    """
)

st.markdown(
    """
    # 📏 Size & 📆 Phases of the EU ETS

    ## 🔢 Basic Stats (2022)
    - 📊 **Covered Emissions**: **40.00%** of total EU emissions  
    - 🧾 **Verified ETS Emissions**: **1362 MtCO₂e**  
    - 🌫️ **GHGs Covered**: CO₂, N₂O, HFCs, PFCs  

    ## ⏳ Phases Overview
    - 🔹 **Phase 1**: 2005–2007 (3 years)  
    - 🔹 **Phase 2**: 2008–2012 (5 years)  
    - 🔹 **Phase 3**: 2013–2020 (8 years)  
    - 🔹 **Phase 4**: 2021–2030 (10 years)  

    ## 🎯 Emissions Cap
    - 🎯 The cap limits total emissions to reduce by **62% (vs 2005)** by **2030**  
    - 🧮 **Phase 1 & 2**: Cap set via Member States’ national allocation plans  
        - 2005: 2,096 MtCO₂e  
        - 2008: 2,049 MtCO₂e  
    - 📉 **Phase 3**:  
        - Single EU-wide cap: 2,084 MtCO₂e (2013), decreasing annually by **1.74%**  
        - 2020 cap: **1,816 MtCO₂e**  
        - ✈️ Aviation added in 2012 (separate cap: 221 MtCO₂e)  
        - "Stop-the-clock" reduced aviation scope to intra-EEA until 2026  

    - 🔽 **Phase 4**:  
        - Linear reduction factor:  
            - 2.2% (2021–2023)  
            - 4.3% (2024–2027)  
            - 4.4% (from 2028)  
        - 🧾 Cap reduced by **90M allowances (2024)** and **27M (2026)**  
        - 2024 cap: **1,386 MtCO₂e**  
        - 🚢 Maritime added: +78.4M allowances (based on 2018–2019 emissions)  
        - ✈️ Aviation cap (2024): **27.6 MtCO₂e**  

    ## 🏭 Sectors & Thresholds

    - **Phase 1**:  
        - Power stations >20 MW  
        - Refineries, coke ovens, steel, cement, glass, lime, paper, etc.  

    - **Phase 2**:  
        - Some N₂O emissions added  
        - ETS expanded to **Iceland, Liechtenstein, Norway**  

    - ✈️ **Aviation (from 2012)**:  
        - Commercial: >10,000 tCO₂/year  
        - Non-commercial: >1,000 tCO₂/year  

    - **Phase 3**:  
        - Carbon capture, ammonia, aluminum, acids added  
        - Swiss flights included (from 2020 via agreement)  

    - **Phase 4**:  
        - Updated scope post-Brexit  
        - Benchmarks adjusted for tech like green hydrogen  
        - ✈️ EU–UK flights covered under respective systems  
        - 🌍 Flights from outermost EU regions to CH/UK added (from 2024)  

    ## 🚢 Maritime (from 2024)
    - Applies to ships >5,000 GT  
    - 📦 Coverage:  
        - 100% of emissions between EU ports  
        - 50% of emissions for voyages to/from non-EU ports  
    - 🧪 GHGs covered: initially **CO₂**, from 2026 also **CH₄** and **N₂O**  
    - 🔄 Gradual surrender obligation:  
        - 2025: 40% of 2024 emissions  
        - 2026: 70% of 2025 emissions  
        - 2027: 100% of 2026 emissions onward  
    - 🛑 Allowances cancelled for uncovered emissions in 2024 & 2025  

    ## 🧩 Regulation Details
    - 🔍 **Point of Regulation**: Point source  
    - 🏢 **Entities Regulated** (2024):  
        - 8,554 installations  
        - 379 aircraft operators  
        - 2,251 shipping companies  
    """
)

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

def load_pdf(path):
    with open(path, "rb") as f:
        return f.read()

# --- Title ---
st.markdown("""
    <h2 style="color:#2E86AB;">📘 EU ETS – Legal & Reference Materials</h2>
    <hr style="margin-top: 0; margin-bottom: 20px;">
""", unsafe_allow_html=True)


# ===============================
# 📚 DOCUMENT DOWNLOAD SECTION
# ===============================

st.markdown("""
    <h4 style="color:#4CAF50;">📂 Downloadable Documents</h4>
    <p style="font-size:16px;">📄 Official directives and reports available as PDF:</p>
""", unsafe_allow_html=True)

# --- Directive 2003/87/EC ---
pdf_bytes_1 = load_pdf("docs/CELEX_02003L0087-20180408_EN_TXT.pdf")
st.download_button(
    label="⬇️ Directive 2003/87/EC – Establishing EU ETS",
    data=pdf_bytes_1,
    file_name="Directive_2003_87_EC.pdf",
    mime="application/pdf"
)

# --- Directive 2023/959 ---
pdf_bytes_2 = load_pdf("docs/CELEX_32023L0959_EN_TXT.pdf")
st.download_button(
    label="⬇️ Directive 2023/959 – Amending EU ETS & Market Stability Reserve",
    data=pdf_bytes_2,
    file_name="Directive_2023_959_EC.pdf",
    mime="application/pdf"
)

# --- 2024 Carbon Market Report ---
pdf_bytes_3 = load_pdf("docs/2024_carbon_market_report_en.pdf")
st.download_button(
    label="⬇️ 2024 Carbon Market Report – European Commission",
    data=pdf_bytes_3,
    file_name="2024_Carbon_Market_Report.pdf",
    mime="application/pdf"
)


# ===============================
# 🌍 WEB LINKS SECTION
# ===============================
st.markdown("""<br><br>""", unsafe_allow_html=True)
st.divider()

st.markdown("""
    <h4 style="color:#4CAF50;">🌍 Key Web Resources</h4>
    <p style="font-size:16px;">🔗 Explore official EU and global carbon market data portals:</p>

    <ul style="font-size:15px; line-height:1.8;">
        <li>🔗 <a href="https://climate.ec.europa.eu/eu-action/carbon-markets/eu-emissions-trading-system-eu-ets_en" target="_blank">EU ETS Overview – European Commission</a></li>
        <li>🔗 <a href="https://climate.ec.europa.eu/eu-action/carbon-markets/ets2-buildings-road-transport-and-additional-sectors_en" target="_blank">EU ETS II – Buildings & Transport</a></li>
        <li>🔗 <a href="https://www.eea.europa.eu/en/datahub/datahubitem-view/98f04097-26de-4fca-86c4-63834818c0c0" target="_blank">EEA Datahub – EU Carbon Market</a></li>
        <li>🔗 <a href="https://carbonpricingdashboard.worldbank.org/" target="_blank">World Bank – Carbon Pricing Dashboard</a></li>
    </ul>
""", unsafe_allow_html=True)