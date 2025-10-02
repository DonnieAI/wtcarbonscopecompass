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

st.title("EU GHG data country view")
st.markdown("""
            ### 📈 Last available data 2022 at EU level 
            
            """)
st.markdown(""" 
            source: EU
            """)

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
 #onlyt he last 

df_ghg_eu_country=pd.read_csv("data/EU_GHG_Emissions_by_country_sector_2022.csv")

df_ghg_eu_country.columns = (
    df_ghg_eu_country.columns
    .str.strip()                        # remove leading/trailing spaces
    .str.replace(r"\s+", " ", regex=True)  # normalize whitespace
    .str.replace(" ", "_")              # replace space with underscore
    .str.lower()                        # optional: lowercase everything
)


df_ghg_eu_country = df_ghg_eu_country.rename(
    columns={"industrial_processes_and_product_use": "industrial_processes",
             "manufacturing_and_construction" : "manufacturing"}
)
df_ghg_eu_country = df_ghg_eu_country[df_ghg_eu_country["country"] != "EU-27"]

# Columns to use for stacking
cols = [
    "energy_industries", 
    "manufacturing",
    "transport",
    "other",
    "industrial_processes",
    "agriculture",
    "waste"
]
color_map = {
    "energy_industries": palette_blue[0],
    "manufacturing": palette_blue[1],
    "transport": palette_blue[2],
    "other": palette_blue[3],
    "industrial_processes": palette_other[0],
    "agriculture": palette_other[1],
    "waste": palette_other[2],
}
# Fill NaNs with 0 for calculation
#for col in cols:

# Step 1: Copy and clean the relevant columns (country + selected sectors)
df_long = df_ghg_eu_country[["country"] + cols].copy()

# Step 2: Replace NaNs in sector columns with 0
for col in cols:
    df_long[col] = df_long[col].fillna(0)

# Step 3: Compute total emissions per country across selected sectors
df_long["emissions_total"] = df_long[cols].sum(axis=1)

# Step 4: Sort by total emissions (descending)
df_long = df_long.sort_values("emissions_total", ascending=False)

# Step 5: Melt to long format for stacked bar plot
df_melt = df_long.melt(
    id_vars=["country"],
    value_vars=cols,
    var_name="sector",
    value_name="emissions"
)

# Step 6: Preserve sorted order in categorical y-axis
df_melt["country"] = pd.Categorical(
    df_melt["country"],
    categories=df_long["country"],  # already sorted by emissions_total
    ordered=False
)

# Step 7: Plot horizontal stacked bar chart
fig = px.bar(
    df_melt,
    x="emissions",
    y="country",
    color="sector",
    orientation="h",
    title="GHG Emissions by Sector and Country (Descending Order)",
    color_discrete_map=color_map
)

# Step 8: Layout improvements
fig.update_layout(
    barmode="stack",
    yaxis_title="Country",
    xaxis_title="Emissions (kt CO₂e)",
    yaxis=dict(autorange="reversed"),  # 👈 add this line
    height=900,
    margin=dict(l=100, r=40, t=80, b=40)
)

# Step 9: Show in Streamlit
st.plotly_chart(fig, use_container_width=True)

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------


ETS1=["energy_industries","public_electricity_and_heat_production","petroleum_refining",
      "iron_and_steel","non-ferrous_metals","chemicals","pulp,_paper_and_print"]
ETS2=["transport","commercial/institutional","residential"]
df_ghg_eu_country = df_ghg_eu_country.loc[:, ~df_ghg_eu_country.columns.duplicated()]
df_scatter = df_ghg_eu_country.copy()

# Fill NaNs to avoid issues in summing
df_scatter[ETS1 + ETS2] = df_scatter[ETS1 + ETS2].fillna(0)

# Sum ETS1 and ETS2 sectors per country
df_scatter["ETS1_total"] = df_scatter[ETS1].sum(axis=1)
df_scatter["ETS2_total"] = df_scatter[ETS2].sum(axis=1)

# Total emissions (used for marker size)
df_scatter["total_emissions"] = df_scatter["total_emissions"].fillna(0)

fig2 = px.scatter(
            df_scatter,
            x="ETS1_total",
            y="ETS2_total",
            size="total_emissions",
            color_discrete_sequence=[palette_other[2]],
            hover_name="country",
            title="ETS1 vs ETS2 Emissions by Country",
            labels={
                "ETS1_total": "ETS1 Emissions (kt CO₂e)",
                "ETS2_total": "ETS2 Emissions (kt CO₂e)",
                "total_emissions": "Total Emissions"
            }
        )

fig2.update_traces(marker=dict(symbol="square", sizemode="area", line=dict(width=1, color="black")))

fig2.update_layout(
    xaxis=dict(title="ETS1 Emissions (kt CO₂e)"),
    yaxis=dict(title="ETS2 Emissions (kt CO₂e)"),
    height=700,
    margin=dict(t=60, l=80, r=40, b=60)
)

st.plotly_chart(fig2, use_container_width=True)