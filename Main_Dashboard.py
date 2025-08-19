import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import requests
import datetime

# --- Page Config ------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Daily Stats on Squid router",
    page_icon="https://img.cryptorank.io/coins/squid1675241862798.png",
    layout="wide"
)

# --- Title with Logo -----------------------------------------------------------------------------------------------------
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 15px;">
        <img src="https://img.cryptorank.io/coins/squid1675241862798.png" alt="Squid Logo" style="width:60px; height:60px;">
        <h1 style="margin: 0;">Daily Stats on Squid router</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Builder Info ---------------------------------------------------------------------------------------------------------
st.markdown(
    """
    <div style="margin-top: 20px; margin-bottom: 20px; font-size: 16px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="https://pbs.twimg.com/profile_images/1841479747332608000/bindDGZQ_400x400.jpg" style="width:25px; height:25px; border-radius: 50%;">
            <span>Built by: <a href="https://x.com/0xeman_raz" target="_blank">Eman Raz</a></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info("📊Charts initially display data for a default time range. Select a custom range to view results for your desired period.")
st.info("⏳On-chain data retrieval may take a few moments. Please wait while the results load.")

# --- API List -----------------------------------------------------------------------------------------------------


# --- Fetch Data --------------------------------------------------------------------------------------------------


def fetch_data():
all_data = []
for url in APIS:
try:
r = requests.get(url)
r.raise_for_status()
data = r.json().get("data", [])
all_data.extend(data)
except Exception as e:
st.error(f"Error fetching {url}: {e}")
return pd.DataFrame(all_data)


raw_df = fetch_data()


if not raw_df.empty:
# Convert timestamp to date
raw_df["date"] = pd.to_datetime(raw_df["timestamp"], unit="ms").dt.date


# Aggregate daily totals
daily_df = raw_df.groupby("date").agg({"volume": "sum", "num_txs": "sum"}).reset_index()


# Get yesterday + day before
y_row = daily_df[daily_df["date"] == yesterday]
d_row = daily_df[daily_df["date"] == day_before]


vol_y, txs_y = (y_row["volume"].sum(), y_row["num_txs"].sum()) if not y_row.empty else (0, 0)
vol_d, txs_d = (d_row["volume"].sum(), d_row["num_txs"].sum()) if not d_row.empty else (0, 0)


# Percentage change
vol_change = ((vol_y - vol_d) / vol_d * 100) if vol_d != 0 else 0
txs_change = ((txs_y - txs_d) / txs_d * 100) if txs_d != 0 else 0


# --- KPI Layout ---------------------------------------------------------------------------------------------
col1, col2 = st.columns(2)


with col1:
st.metric(
label="Volume of Swaps",
value=f"{vol_y:,.2f}",
delta=f"{vol_change:.2f}%",
delta_color="normal"
)


with col2:
st.metric(
label="Number of Swaps",
value=f"{txs_y:,}",
delta=f"{txs_change:.2f}%",
delta_color="normal"
)
else:
st.warning("No data available.")
