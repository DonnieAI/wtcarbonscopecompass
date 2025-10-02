import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px 
from pathlib import Path
from plotly.subplots import make_subplots

#https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart
#https://docs.mapbox.com/api/maps/styles/
#    cd C:\WT\WT_OFFICIAL_APPLICATIONS_REPOSITORY\WT_CARBON_SCOPE_COMPASS


st.set_page_config(page_title="projects", layout="wide")
from utils import apply_style_and_logo
apply_style_and_logo()


palette_blue = [
    "#A7D5F2",  # light blue
    "#94CCE8",
    "#81C3DD",
    "#6FBBD3",
    "#5DB2C8",
    "#A9DEF9",  # baby blue
]

palette_green = [
    "#6DC0B8",  # pastel teal
    "#7DCFA8",
    "#8DDC99",
    "#9CE98A",
    "#ABF67B",
    "#C9F9D3",  # mint green
    "#C4E17F",  # lime green
]

palette_other = [
    "#FFD7BA",  # pastel orange
    "#FFE29A",  # pastel yellow
    "#FFB6C1",  # pastel pink
    "#D7BDE2",  # pastel purple
    "#F6C6EA",  # light rose
    "#F7D794",  # peach
    "#E4C1F9",  # lavender
]
#--------------------------------------------------------------------------------------------

st.title("Allowance Allocation & Revenues")
st.markdown("""
            ### 📈 Allowance Allocation & Revenues
            
            """)
st.markdown(""" 
            source: EU
            """)

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------


df=pd.read_csv("data\Data details by year.csv")

df['Year'] = pd.to_datetime(df['Year'], format='%Y')
#df_ghg_eu_sector['year'].dt.year

df["Net_Supply_Allowance"]=(-df["Verified Emission"]+df["Allocations"])/df["Verified Emission"]*100

# Create bar chart
fig = px.bar(
    df,
    x="Year",
    y="Net_Supply_Allowance",
    color="Net_Supply_Allowance",
    color_continuous_scale=[palette_blue[0], palette_other[-1]],  # red for negative, green for positive
    title="Net Supply Allowance (% of Verified Emissions)"
)

fig.add_vrect(
    x0=pd.Timestamp("2005-01-01"), 
    x1=pd.Timestamp("2007-12-31"),
    fillcolor=palette_other[0], opacity=0.3, line_width=0,
    annotation_text="Phase 1", annotation_position="top left"
)

fig.add_vrect(
    x0=pd.Timestamp("2008-01-01"), 
    x1=pd.Timestamp("2012-12-31"),
    fillcolor=palette_other[1], opacity=0.3, line_width=0,
    annotation_text="Phase 2", annotation_position="top left"
)

fig.add_vrect(
    x0=pd.Timestamp("2013-01-01"), 
    x1=pd.Timestamp("2020-12-31"),
    fillcolor=palette_other[2], opacity=0.3, line_width=0,
    annotation_text="Phase 3", annotation_position="top left"
)

fig.add_vrect(
    x0=pd.Timestamp("2021-01-01"), 
    x1=df["Year"].max(),  # also a Timestamp
    fillcolor=palette_other[3], opacity=0.3, line_width=0,
    annotation_text="Phase 4", annotation_position="top left"
)




# Show zero line
fig.update_layout(
    yaxis_title="Net Supply Allowance (%)",
    xaxis_title="Year",
    coloraxis_showscale=False  # hide gradient legend if not needed
)
fig.add_hline(y=0, line_dash="dash", line_color="black")

st.plotly_chart(fig, use_container_width=True)


import streamlit as st

st.markdown(
    r"""
# 💰 Allowance Allocation & Revenue

## 🧾 Allocation by Phase

### 🔹 Phase 1
- Based on Member States’ national allocation plans
- Mostly **grandparenting** (allocation based on historical emissions)
- Some auctioning and benchmark-based allocation

### 🔹 Phase 2
- 🛒 **Auctioning** (~3% of allowances): 8 countries (e.g., DE, UK, NL)
- 🎁 **Free Allocation**: ~90% of allowances

### 🔹 Phase 3
- 🛒 **Auctioning**: Main method, up to 57% of cap  
    - 88% allocated to Member States (based on 2005 emissions)  
    - 10% solidarity provision for lower-income countries  
    - 2% reward for early emission reductions
- 🎁 **Free Allocation**:
    - Based on sector-specific **performance benchmarks**
    - Adjusted via a **cross-sectoral correction factor**
- ⚡ **Power Sector**:  
    - Full auctioning  
    - Optional transitional free allocation for 10 lower-income states  
- 🏭 **Industry**:
    - Based on benchmarks for the top 10% most efficient installations  
    - Reduction of free allocation for non-leakage sectors from 80% → 30% (by 2020)

- 🔐 **Carbon Leakage Risk** criteria:
    - Direct & indirect cost increase >30%; **or**
    - Non-EU trade intensity >30%; **or**
    - Direct & indirect cost >5% and trade intensity >10%
    - **Cost Intensity Formula**:
    $$
    \frac{\text{Carbon Price} \times (\text{Direct Emissions} \times \text{Auctioning Factor} + \text{Electricity Consumption} \times \text{Electricity Emission Factor})}{\text{Gross Value Added}}
    $$
    - **Trade Intensity Formula**:
    $$
    \frac{\text{Imports} + \text{Exports}}{\text{Imports} + \text{Production}}
    $$

- 🆕 **New Entrants’ Reserve (NER)**:  
    - 5% of Phase 3 cap set aside  
    - 300M allowances for **NER300** (funding low-carbon projects)

- ✈️ **Aviation**:
    - 15% auctioned, 82% free, 3% special reserve  
    - Scope reduced to intra-EEA → fewer allowances in circulation

---

### 🔹 Phase 4

- 🛒 **Auctioning**:  
    - Still ~57% of total cap  
    - 90% to Member States  
    - 10% solidarity redistribution  

- 🎁 **Free Allocation**:
    - Based on updated sector-specific **benchmarks**
    - Benchmarks updated **twice** (2021–2025 & 2026–2030)
    - Annual reductions vary per sector (e.g. **fixed rate for steel**)
    - **Cross-sectoral correction factor** = 1 (for 2021–2025)
    - 450M allowance buffer available to avoid correction factor

- 🏭 **Industry**:
    - Benchmarks revised using 2016–2017 data  
    - Reductions compared to 2007–08 → 2022–23  
        - 31/54 benchmarks reduced by the max 24%

    - **Production change adjustment**:
        - Triggered by ±15% production change  
        - Annual reports required  
        - Changes applied from **NER**  

- 🔐 **Carbon Leakage – Phase 4**
    - Criteria (composite indicator):
    $$
    \text{Trade Intensity} \times \text{Emissions Intensity} > 0.2
    $$
    - If:
    $$
    0.15 < \text{TI} \times \text{EI} \leq 0.2
    $$
    → Qualitative assessment (abatement potential, market, profits)

    - **Emissions Intensity**:
    $$
    \frac{\text{Direct Emissions} + (\text{Electricity Consumption} \times \text{Electricity Emission Factor})}{\text{Gross Value Added}}
    $$
    - **Trade Exposure**:
    $$
    \frac{\text{Imports} + \text{Exports}}{\text{Imports} + \text{Production}}
    $$

- 🌍 **Carbon Border Adjustment Mechanism (CBAM)**:
    - Gradual phase-out of free allocation (2026–2034)
    - Applies to: **steel, cement, aluminium, fertilizers, hydrogen**
    - Exempts: EFTA countries + CH (via ETS link)
    - ⚙️ **CBAM Factor**:
        - 2026: 97.5%  
        - 2030: 51.5%  
        - 2033: 14%  
    - Applies to electricity imports as well

- 🆕 **NER in Phase 4**:
    - 331.3M allowances total  
    - Includes leftover Phase 3 + 200M from MSR  

- ✈️ **Aviation (Phase 4)**:
    - Free allocation phased out:  
        - 2024: 75%  
        - 2025: 50%  
        - 2026: 0%

---

## 💶 Auctioning & Revenue

- 💵 **Auction Share**: 57% of total allowances  
- 💰 **Total Revenue**:  
    - €184B (USD 206B) since inception  
    - €38.8B (USD 42B) in 2024  
    - Includes: Iceland, Liechtenstein, Norway, Northern Ireland, and Funds  

---

## 📈 Use of Revenues (2024)

- 🏛️ Primarily goes to **national budgets**
- 🟩 Must be used for **climate and energy transition** (since June 2023)
- 🧾 **Exceptions**: Aid to electricity-intensive sectors allowed
- 💼 **State Aid Limit**: Max 25% of revenue

- 📊 **Reported Spending (2023)**:
    - 🔋 Energy, grids, storage: 43%  
    - 🚍 Transport & mobility: 23%  
    - 🧑‍🤝‍🧑 Social & just transition: 12%  
    - 🏘️ Buildings: heating/cooling/efficiency: 10%  
    - 🏭 Industry decarbonization: 3%  
    - Other: 9%

---

## 🧪 Innovation & Modernisation Funds

- 💡 **Innovation Fund**:  
    - One of the **world’s largest** low-carbon tech funds  
    - Funded by EU ETS revenues  
    - Budget: ~€40B (USD 43.3B) by 2030  
    - Grants for commercializing low/zero-carbon technologies  

- ⚡ **Modernisation Fund**:  
    - Solidarity-based support for lower-income Member States  
    - Targets: energy systems, efficiency, and just transition projects  

"""
)