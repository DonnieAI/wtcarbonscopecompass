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

st.title("Company GHG Compass")
st.markdown("""
            ### 📈 Company GHG Compass
            
            """)
st.markdown(""" 
            source: EU
            """)

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

activity_code_mapping = {
    "Combustion installations with a rated thermal input exceeding 20 MW": 1,
    "Mineral oil refineries": 2,
    "Coke ovens": 3,
    "Metal ore (including sulphide ore) roasting or sintering installations": 4,
    "Installations for the production of pig iron or steel (primary or secondary fusion) including continuous casting": 5,
    "Installations for the production of cement clinker in rotary kilns or lime in rotary kilns or in other furnaces": 6,
    "Installations for the manufacture of glass including glass fibre": 7,
    "Installations for the manufacture of ceramic products by firing, in particular roofing tiles, bricks, refractory bricks, tiles, stoneware or porcelain": 8,
    "Industrial plants for the production of (a) pulp from timber or other fibrous materials (b) paper and board": 9,
    "Aircraft operator activities": 10,
    "Combustion of fuels": 20,
    "Refining of mineral oil": 21,
    "Production of coke": 22,
    "Metal ore roasting or sintering": 23,
    "Production of pig iron or steel": 24,
    "Production or processing of ferrous metals": 25,
    "Production of primary aluminium": 26,
    "Production of secondary aluminium": 27,
    "Production or processing of non-ferrous metals": 28,
    "Production of cement clinker": 29,
    "Production of lime, or calcination of dolomite/magnesite": 30,
    "Manufacture of glass": 31,
    "Manufacture of ceramics": 32,
    "Manufacture of mineral wool": 33,
    "Production or processing of gypsum or plasterboard": 34,
    "Production of pulp": 35,
    "Production of paper or cardboard": 36,
    "Production of carbon black": 37,
    "Production of nitric acid": 38,
    "Production of adipic acid": 39,
    "Production of glyoxal and glyoxylic acid": 40,
    "Production of ammonia": 41,
    "Production of bulk chemicals": 42,
    "Production of hydrogen and synthesis gas": 43,
    "Production of soda ash and sodium bicarbonate": 44,
    "Capture of greenhouse gases under Directive 2009/31/EC": 45,
    "Transport of greenhouse gases under Directive 2009/31/EC": 46,
    "Storage of greenhouse gases under Directive 2009/31/EC": 47,
    "Maritime Operator": 50,
    "Other activity opted-in pursuant to Article 24 of Directive 2003/87/EC": 99
}


#CO2_yearly_value=[50,50,50,50,50,50,50,50,50,50,50,70]
#year_price_map = dict(zip(years, CO2_yearly_value))  

years = list(range(2013, 2025))
CO2_yearly_value_df=pd.read_csv("yearly_average_price.csv")
year_price_map = dict(zip(CO2_yearly_value_df["year"], CO2_yearly_value_df["price"]))
# Create a mapping from year to price
     
    
df=pd.read_csv(r"C:\Users\donat\Documents\PYTHON_CO2EUETS\data\verified_emissions_2024_en_elaborated.csv")
df.columns = df.columns.str.strip()

#---- Year selection 
years = sorted(years, reverse=True)  # now starts from 2024
# Default index = 0 (which will be 2024 after sorting)
selected_year_int = st.selectbox("Select a year:", years, index=0)
# Convert to string if needed
selected_year = str(selected_year_int)

CO2_price = year_price_map[selected_year_int]

#------activity selection 
# Convert keys to list
activities = list(activity_code_mapping.keys())
# Set default activity
default_activity = 'Refining of mineral oil'
default_index = activities.index(default_activity) if default_activity in activities else 0
# Selectbox with default
selected_activity = st.selectbox(
    "Select an activity:",
    options=activities,
    index=default_index
)
# Get the corresponding numeric code
#activity_code = activity_code_mapping[selected_activity]


#------country selection 
# Get unique country codes
available_countries = df["REGISTRY_CODE"].unique().tolist()
# Set default country to "DE"
default_country = "ES"
default_index = available_countries.index(default_country) if default_country in available_countries else 0
# Selectbox with default set to DE
selected_country = st.selectbox(
    "Select a country:",
    available_countries,
    index=default_index
)


def filter_by_year_and_activity_query(df: pd.DataFrame,selected_country: str, selected_year: str, selected_activity: str,
    yearly_average_co2_price:float,
    activity_code_mapping: dict
    ) -> pd.DataFrame:
    """
    Filters the DataFrame by selected year, country, and main activity type.
    """

    # 1. Clean column names
    df.columns = df.columns.str.strip()

    # 2. Get activity code
    activity_code = activity_code_mapping.get(selected_activity)
    if activity_code is None:
        raise ValueError(f"Activity '{selected_activity}' is not in activity_code_mapping.")

    # 3. Dynamically build column names
    allocation_col = f"ALLOCATION_{selected_year}"
    reserve_col = f"ALLOCATION_RESERVE_{selected_year}"
    trans_col   = f"ALLOCATION_TRANSITIONAL_{selected_year}"
    #ch_alloc_col = f"CH_ALLOCATION_{selected_year}"
    verified_col = f"VERIFIED_EMISSIONS_{selected_year}"
    #ch_verified_col = f"CH_VERIFIED_EMISSIONS_{selected_year}"

    base_cols = [
        "INSTALLATION_NAME",
        "INSTALLATION_IDENTIFIER",
        "PERMIT_IDENTIFIER",
        "REGISTRY_CODE"
    ]
    year_cols = [allocation_col, reserve_col, trans_col, verified_col ]
    all_required_cols = base_cols + year_cols

    # 4. Check if all required columns exist
    missing_cols = [col for col in all_required_cols + ["MAIN_ACTIVITY_TYPE_CODE"] if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing required columns: {missing_cols}")

    # 5. Apply filtering using boolean mask (safer than .query)
    mask = (
        (df["REGISTRY_CODE"] == selected_country) &
        (df[allocation_col] != -1) &
        (df[verified_col] != -1) &
        (df[verified_col] != -99) &
        (df["MAIN_ACTIVITY_TYPE_CODE"] == activity_code)
    )

    # 6. Filter and return relevant columns
    filtered_df=df.loc[mask, all_required_cols]
    filtered_df ["ETS_COST_MEUR"]=(filtered_df[verified_col]-filtered_df[allocation_col])*yearly_average_co2_price/1000000 #MEUR
    
    return filtered_df

df_filtered = filter_by_year_and_activity_query(df, selected_country, selected_year, selected_activity, CO2_price,activity_code_mapping)

def plot_allocation_vs_emissions(df_filtered, selected_year: str, selected_country: str, selected_activity: str):
    x_col = f"ALLOCATION_{selected_year}"
    y_col = f"VERIFIED_EMISSIONS_{selected_year}"

    # Create scatter with ETS_COST_kEUR as color
    fig = px.scatter(
        df_filtered,
        x=x_col,
        y=y_col,
        color="ETS_COST_MEUR",          # map color to ETS cost
        color_continuous_scale="Reds",  # red style
        title=f"Allocation vs Verified Emissions ({selected_activity} | {selected_country} | {selected_year})",
        hover_data=["INSTALLATION_NAME", "REGISTRY_CODE", "ETS_COST_MEUR"],
    )

    # Update marker style to triangle
    fig.update_traces(
        marker=dict(symbol="triangle-up", size=20),
    )

    # Add 45° line (y=x)
    min_val = min(df_filtered[x_col].min(), df_filtered[y_col].min())
    max_val = max(df_filtered[x_col].max(), df_filtered[y_col].max())

    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode="lines",
        line=dict(dash="dash", color="gray"),
        #name="45° Line"
    ))

    # Layout improvements
    fig.update_layout(
        xaxis_title="Allocation",
        yaxis_title="Verified Emissions",
        width=900,
        height=700,
        coloraxis_colorbar=dict(
            title="ETS Cost<br>(MEUR)",
            #titleside="right"
        )
    )

    return fig

fig = plot_allocation_vs_emissions(df_filtered, selected_year,selected_country,selected_activity)

st.plotly_chart(fig, use_container_width=True)

# Define suffix to remove
suffix = f"_{selected_year}"

# Rename columns that end with _{year} → remove year part
df_display = df_filtered.rename(
    columns=lambda col: col.replace(suffix, "") if col.endswith(suffix) else col
)

# Select relevant columns to display in table (optional order)
columns_to_show = [
    "INSTALLATION_NAME",
    "INSTALLATION_IDENTIFIER",
    "PERMIT_IDENTIFIER",
    "REGISTRY_CODE",
    "ALLOCATION",
    "ALLOCATION_RESERVE",
    "ALLOCATION_TRANSITIONAL",
    "VERIFIED_EMISSIONS",
    "ETS_COST_MEUR"
]

# Show nicely formatted table
st.markdown("### 📋 Filtered Results Table")
st.dataframe(df_display[columns_to_show], use_container_width=True)

# Convert dataframe to CSV
csv = df_display.to_csv(index=False).encode("utf-8")
#yearly_avg_df.to_csv("yearly_average_price.csv")
# Add download button
st.download_button(
    label="💾 Download CSV",
    data=csv,
    file_name="df_display.csv",
    mime="text/csv"
)