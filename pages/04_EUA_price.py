import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px 
from pathlib import Path
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np

#https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart
#https://docs.mapbox.com/api/maps/styles/
#    cd C:\WT\WT_OFFICIAL_APPLICATIONS_REPOSITORY\WT_CARBON_SCOPE_COMPASS
#https://energy.instrat.pl/en/prices/eu-ets/

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
co2_price_df=pd.read_csv("data/prices_eu_ets_all.csv")
co2_price_df["date"] = pd.to_datetime(co2_price_df["date"], dayfirst=True)
# Extract the year from the date
co2_price_df["year"] = co2_price_df["date"].dt.year


#-----------------------------------------------------
#-AVERAGE YEARLY
# Calculate yearly average EUA prices from 2005 to 2024 (based on available data)
# Define current year
current_year = datetime.now().year

# Filter and calculate yearly average prices from 2005 to 2025
yearly_avg_prices = (
    co2_price_df
    .groupby("year")["price"]
    .mean()
    .round(2)
    .loc[lambda s: (s.index >= 2005) & (s.index <= 2025)]
)

# Calculate YTD average for the current year
ytd_avg_price = (
    co2_price_df[co2_price_df["year"] == current_year]
    .groupby("year")["price"]
    .mean()
    .round(2)
)

# Update or append the YTD value to the series
yearly_avg_prices.update(ytd_avg_price)

# Convert to DataFrame and calculate variation
yearly_avg_df = (
    yearly_avg_prices
    .sort_index()
    .reset_index()
    .rename(columns={"index": "year", "price": "price"})
    .assign(variation=lambda df: df["price"].pct_change().round(2)*100)
)

#-----------------------------------------------------)

print(yearly_avg_df)




#🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠-----------------
# Sort and set index BEFORE assign (required for resample)
co2_price_df = (
    co2_price_df
    .sort_values("date")
    .set_index("date")     # <-- IMPORTANT
)


co2_price_df = (
    co2_price_df
   # .sort_values("date")
   # .reset_index(drop=True)
    .assign(
        monthly_average=lambda df: df["price"].resample("ME").mean(),
        MA_1Y=lambda df: df["price"].rolling(window=365, min_periods=1).mean(),
        daily_variation=lambda df: df["price"].pct_change() * 100,
        log_return=lambda df: np.log(df["price"] / df["price"].shift(1)),
        daily_volatility=lambda df: np.abs(df["log_return"]) * 100,
        #volatility_1y=lambda df: df["log_return"].rolling(window=365, min_periods=10).std(),
        volatility_20d=lambda df: df["log_return"].rolling(window=20, min_periods=5).std(),
        volatility_1y=lambda df: df["log_return"].rolling(window=252, min_periods=5).std()
    )
)
#🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠🧠--------
co2_price_df["monthly_average"].isna().sum()
thresold_day=min(co2_price_df.index)
#🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹
#VOLATILITY SECTION
#🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹
# Daily log returns already computed in your df
daily_vol = co2_price_df["log_return"].std() * 100          # Daily volatility in %
annual_vol = daily_vol * np.sqrt(252)   
weekly_vol=daily_vol*np.sqrt(5)# Annualized volatility in %
monthly_vol=daily_vol*np.sqrt(21)# Annualized volatility in %
print(f"Daily Volatility: {daily_vol:.2f}% (std dev of daily returns)")
print(f"Annualized Volatility: {annual_vol:.2f}%")

co2_price_df["month"] = co2_price_df.index.month
co2_price_df["year"] = co2_price_df.index.year

monthly_vol_df = (
    co2_price_df
    .groupby(["year", "month"])
    .agg(monthly_volatility=("log_return", lambda x: np.std(x) * np.sqrt(21)))  # Monthly vol (annualized-style)
    .reset_index()
)
monthly_vol_df["month_name"] = pd.to_datetime(monthly_vol_df["month"], format="%m").dt.strftime("%b")
avg_vol_by_month = (
    monthly_vol_df
    .groupby("month_name", sort=False)
    .agg(avg_volatility=("monthly_volatility", "mean"))
    .reset_index()
)

#Method 1 — Volatility on Up vs. Down Days
co2_price_df["direction"] = np.where(co2_price_df["log_return"] > 0, "Up", "Down")

# Compare average volatility
vol_by_direction = (
    co2_price_df
    .groupby("direction")
    .agg(avg_volatility=("daily_volatility", "mean"),
         count=("daily_volatility", "count"))
    .reset_index()
)
print(vol_by_direction)


#🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹
#CORRELATION WITH TTF
#🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹🧹
ttf_raw_df=pd.read_csv("data/2025-10-31_TTF_monthly.csv")
ttf_raw_df["Date"] = pd.to_datetime(ttf_raw_df["Date"], dayfirst=False)

thresold_day=max(min(co2_price_df.index),min(ttf_raw_df["Date"]))

ttf_df=(
            ttf_raw_df
            .query("Date>=@thresold_day")
            .sort_values("Date")
            .set_index("Date")     # <-- IMPORTANT
               
)


eua_monthly = co2_price_df["monthly_average"][~co2_price_df["monthly_average"].index.duplicated(keep="first")]
gas_weekly = ttf_df["price_eur/mwh"][~ttf_df["price_eur/mwh"].index.duplicated(keep="first")]

# Combine into one DataFrame
combined_df = pd.concat([eua_monthly, gas_weekly], axis=1)
combined_df.columns = ["eua_price", "gas_price"]
combined_df.dropna(inplace=True)
combined_df["rolling_corr_12w"] = combined_df["eua_price"].rolling(12).corr(combined_df["gas_price"])

#--------------------------------------------------------------------------------------------
st.title("EU Allowance (EUA)")
st.markdown("""
            ### 📈 EU Allowance (EUA) price trend [EUR/tCO₂]
            
            """)
st.markdown(""" 
            source: energy.instrat.pl
            """)

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.12,
    row_heights=[0.7, 0.3],
    subplot_titles=(
        f"EUA CO2 Price [EUR/tCO₂]",
        "Daily variation  [%]"
    )
)

fig.add_trace(
    go.Scatter(
        x=co2_price_df.index,
        y=co2_price_df["price"],
        mode="lines",
        name="CO2 price | daily",
        line=dict(
            color=palette_blue[4],
            width=2,
            dash="solid"
        )
    ),
    row=1,
    col=1
)
   
fig.add_trace(
    go.Scatter(
        x=co2_price_df.index,
        y=co2_price_df["MA_1Y"],
        mode="lines",
        name="CO2 price| Yearly Moving Average 1y",
        line=dict(
            color=palette_green[2],
            width=3,
            dash="dash"
        )
    ),
    row=1,
    col=1
)

fig.add_trace(
    go.Bar(
         x=co2_price_df.index,
        y=co2_price_df["daily_variation"],
        name="Variation (%)",
        marker_color=[
            "#F5B7B1" if v < 0 else "#A9DFBF"
            for v in co2_price_df["daily_variation"]
        ]
    ),
    row=2,
    col=1
)
       
# Step 3: Optional layout tweaks
fig.update_layout(
                    legend_title_text='Legend',
                    xaxis_title='Date',
                    yaxis_title='EUR/tCO₂',
                    hovermode='x unified'
        )


fig.add_vrect(
                x0=pd.Timestamp("2021-01-01"), 
                x1=co2_price_df.index.max(),  # also a Timestamp
                fillcolor="blue", opacity=0.1, line_width=0,
                annotation_text="Phase 4", annotation_position="top left"
)

fig.add_vrect(
                x0=pd.Timestamp("2013-01-01"), 
                x1=pd.Timestamp("2020-12-31"),
                fillcolor="red", opacity=0.1, line_width=0,
                annotation_text="Phase 3", annotation_position="top left"
)


fig.update_xaxes(
                dtick="M12",         # one tick every 12 months
                tickformat="%Y",     # show only the year
                ticklabelmode="period"  # align ticks at year start
)
 
fig.update_layout(height=800) 
st.plotly_chart(fig, use_container_width=True)


#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
st.divider()  # <--- Streamlit's built-in separator
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------
st.markdown("""
            ### 📈 EU Allowance (EUA) price yearly average (EUR/tCO₂)
            
            """)
st.markdown(""" 
            source: energy.instrat.pl
            """)

fig2 = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.12,
    row_heights=[0.7, 0.3],
    subplot_titles=(
        f" EUA CO2 Price [EUR/tCO₂] | yearly average ",
        "Yearly variation  [%]"
    )
)

fig2.add_trace(
    go.Scatter(
        x=yearly_avg_df["year"],
        y=yearly_avg_df["price"],
        mode="lines+markers",
        name="CO₂ price | yearly average",
        line=dict(color=palette_blue[1], width=2),
        marker=dict(symbol="diamond", size=14, color=palette_blue[4])
    ),
    row=1,
    col=1
)
    
fig2.add_trace(
    go.Bar(
        x=yearly_avg_df["year"],
        y=yearly_avg_df["variation"],
        name="Variation (%)",
        marker_color=[
            "#F5B7B1" if v < 0 else "#A9DFBF"
            for v in yearly_avg_df["variation"]
        ]
    ),
    row=2,
    col=1
)

fig2.update_layout(
                title="📊 Average CO₂ Price per Year",
                xaxis_title="Year",
                yaxis_title="Average Price [EUR/tCO₂]",
                uniformtext_minsize=8,
                uniformtext_mode='hide',
                bargap=0.2               # spacing between bars
)

fig2.update_xaxes(
            dtick="M12",         # one tick every 12 months
            tickformat="%Y",     # show only the year
            ticklabelmode="period"  # align ticks at year start
)
fig2.update_layout(height=1000) 
st.plotly_chart(fig2, use_container_width=True)


#---------------------------------
#---------------------------------

fig3 = go.Figure()

# 20-Day Historical Volatility
fig3.add_trace(
        go.Scatter(
                x=co2_price_df.index,
                y=co2_price_df["volatility_20d"] * 100,  # convert to percent
                mode="lines",
                name="20D Historical Volatility",
                line=dict(
                    color=palette_blue[4], 
                        width=2)
))

# 1-Year Historical Volatility
fig3.add_trace(go.Scatter(
   x=co2_price_df.index,
    y=co2_price_df["volatility_1y"] * 100,  # convert to percent
    mode="lines",
    name="1Y Historical Volatility",
    line=dict(color=palette_green[4], width=2)
))

# Layout
fig3.update_layout(
    title="EU ETS Volatility (Daily, 20D, 1Y)",
    xaxis_title="Date",
    yaxis_title="Volatility (%)",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0)', borderwidth=0)
)

fig3.update_layout(height=1000) 
st.plotly_chart(fig3, use_container_width=True)

st.dataframe(yearly_avg_df, use_container_width=True)



fig4 = px.bar(
    vol_by_direction,
    x="direction",
    y="avg_volatility",
    title="Average Volatility on Up vs. Down Days",
    labels={"avg_volatility": "Average Volatility (%)", "direction": "Price Movement"},
    template="plotly_white"
)
st.plotly_chart(fig4, use_container_width=True)



# 📈 Plot rolling correlation
fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=combined_df.index, y=combined_df["rolling_corr_12w"], name="12W Corr"))
fig5.update_layout(title="🔗 Rolling Correlation (EUA vs Gas)", template="plotly_white")
st.plotly_chart(fig5, use_container_width=True)




# Convert dataframe to CSV
csv = yearly_avg_df.to_csv(index=False).encode("utf-8")
yearly_avg_df.to_csv("yearly_average_price.csv")
# Add download button
st.download_button(
    label="💾 Download CSV",
    data=csv,
    file_name="yearly_avg_co2_price.csv",
    mime="text/csv"
)