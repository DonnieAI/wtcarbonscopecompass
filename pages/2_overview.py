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
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
df_ghg_eu_sector=pd.read_csv("data/EU_GHG_Emissions_by_sector.csv")
# Your DataFrame
df_ghg_eu_sector['Year'] = pd.to_datetime(df_ghg_eu_sector['Year'], format='%Y')
df_ghg_eu_sector.columns = (
    df_ghg_eu_sector.columns
    .str.strip()                        # remove leading/trailing spaces
    .str.replace(r"\s+", " ", regex=True)  # normalize whitespace
    .str.replace(" ", "_")              # replace space with underscore
    .str.lower()                        # optional: lowercase everything
)

df_ghg_eu_sector = df_ghg_eu_sector.rename(
    columns={"industrial_processes_and_product_use": "industrial_processes",
             "manufacturing_and_construction" : "manufacturing"}
)

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

st.title("EU GHG macro sector trend")
st.markdown("""
            ### 📈 
            
            """)
st.markdown(""" 
            source: EU
            """)

# Define sector columns (excluding 'year' and 'total_emissions')
available_sectors = [
    col for col in df_ghg_eu_sector.columns
    if col not in ['year', 'total_emissions']
    and pd.api.types.is_numeric_dtype(df_ghg_eu_sector[col])
]

# Dropdown to select sector
selected_sector = st.selectbox("Select a sector to compare with EU GHG total emissions (1990=100):", available_sectors)


def plot_emission_index(df, sector_col):
    """
    Plot emission index (1990=100) for a given sector vs total emissions.
    """
    if 1990 not in df['year'].dt.year.values:
        raise ValueError("DataFrame must contain 1990 as baseline year.")

    baseline_sector = df.loc[df['year'].dt.year == 1990, sector_col].iloc[0]
    baseline_total = df.loc[df['year'].dt.year == 1990, "total_emissions"].iloc[0]

    df_plot = df.copy()
    df_plot["sector_index"] = df_plot[sector_col] / baseline_sector * 100
    df_plot["total_index"] = df_plot["total_emissions"] / baseline_total * 100

    df_long = df_plot.melt(
        id_vars="year",
        value_vars=["sector_index", "total_index"],
        var_name="Series",
        value_name="Index"
    )

    label_map = {
        "sector_index": f"{sector_col} (index, 1990=100)",
        "total_index": "Total Emissions (index, 1990=100)"
    }
    df_long["Series"] = df_long["Series"].map(label_map)

    fig = px.line(
            df_long,
            x="year",
            y="Index",
            color="Series",
            color_discrete_sequence=[palette_blue[0], palette_other[0]], # first color = sector, second = total
            title=f"Emission Index (1990=100): {sector_col.replace('_', ' ').title()} vs Total"
    )
    fig.update_layout(height=500)
    fig.update_traces(line=dict(width=6))
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
        x1=df["year"].max(),  # also a Timestamp
        fillcolor=palette_other[3], opacity=0.3, line_width=0,
        annotation_text="Phase 4", annotation_position="top left"
)
    
        


    return fig

# Show chart
fig = plot_emission_index(df_ghg_eu_sector, selected_sector)

st.plotly_chart(fig, use_container_width=True)

#NARRATIVE BOX
# Narrative text with f-string + HTML styling
narrative_trend = f"""
<div style="
    border: 2px solid {palette_green[3]};
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
">
<b>📊 Key Insights</b>

- Figures for 2025 and 2026 are based on projections 
- D.M 2018 boosted the production from **** to **** bsmc from 2018 to 2024
- Current biomethane thoerica capacity : **** bn Smc/y</span>  


<b>💡 Interpretation:</b>  
- The sector is progressing, but still **below target**.  
- Additional investments or incentives are required to accelerate deployment.  
</div>
"""

st.markdown(narrative_trend, unsafe_allow_html=True)
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

st.title("EU GHG data overview")
st.markdown("""
            ### 📈 
            
            """)
st.markdown(""" 
            source: EU
            """)



# Year selectors
years = sorted(df_ghg_eu_sector['year'].dt.year.unique(), reverse=True)
col1, col2 = st.columns(2)

year1 = col1.selectbox("Select first year", years, index=0)
year2 = col2.selectbox("Select second year", years, index=1)

# Columns to extract
cols = [
    "energy_industries", 
    "manufacturing",
    "transport",
    "other",
    "industrial_processes",
    "agriculture",
    "waste"
]

# Color mapping
color_map = {
    "energy_industries": palette_blue[0],
    "manufacturing": palette_blue[1],
    "transport": palette_blue[2],
    "other": palette_blue[3],
    "industrial_processes": palette_other[0],
    "agriculture": palette_other[1],
    "waste": palette_other[2],
}

# Function to generate pie chart for a selected year
def make_pie(year):
    df_selected = df_ghg_eu_sector[df_ghg_eu_sector['year'].dt.year == year]
    emissions = df_selected[cols].iloc[0]
    df_pie = emissions.reset_index()
    df_pie.columns = ['sector', 'emissions']

    fig = go.Figure(
        data=[
            go.Pie(
                labels=df_pie['sector'],
                values=df_pie['emissions'],
                hole=0.4,
                marker_colors=[color_map[s] for s in df_pie['sector']],
                textposition='inside',
                textinfo='percent+label'
            )
        ]
    )
    fig.update_layout(
        title_text=f"GHG Emissions by Sector – {year}",
        width=450,
        height=500,
        margin=dict(t=60, b=40, l=20, r=20),
        showlegend=False
    )
    return fig

with col1:
    st.plotly_chart(make_pie(year1), use_container_width=False)
    total1 = df_ghg_eu_sector[df_ghg_eu_sector['year'].dt.year == year1][cols].iloc[0].sum()
    st.markdown(f"**Total GHG Emissions {year1}:** {total1:,.0f} kt")

with col2:
    st.plotly_chart(make_pie(year2), use_container_width=False)
    total2 = df_ghg_eu_sector[df_ghg_eu_sector['year'].dt.year == year2][cols].iloc[0].sum()
    st.markdown(f"**Total GHG Emissions {year2}:** {total2:,.0f} kt")


#NARRATIVE BOX
# Narrative text with f-string + HTML styling
narrative_pie = f"""
<div style="
    border: 2px solid {palette_green[3]};
    padding: 15px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
">
<b>📊 Key Insights</b>

- Figures for 2025 and 2026 are based on projections 
- D.M 2018 boosted the production from **{total1}** to **{total1}** bsmc from 2018 to 2024
- Current biomethane thoerica capacity : **{total1}** bn Smc/y</span>  


<b>💡 Interpretation:</b>  
- The sector is progressing, but still **below target**.  
- Additional investments or incentives are required to accelerate deployment.  
</div>
"""

st.markdown(narrative_pie, unsafe_allow_html=True)














