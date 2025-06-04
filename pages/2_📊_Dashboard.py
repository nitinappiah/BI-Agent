import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

# Title
st.title("Plant Capacity Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/plants.csv")
    # Drop any unnamed index columns
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
plants = df["plant"].sort_values().unique().tolist()
materials = df["chemical_material"].sort_values().unique().tolist()

selected_plants = st.sidebar.multiselect("Select Plant(s):", plants, default=plants)
selected_materials = st.sidebar.multiselect("Select Material(s):", materials, default=materials)

# Filter data
df_filtered = df[
    (df["plant"].isin(selected_plants)) &
    (df["chemical_material"].isin(selected_materials))
]

# KPIs
total_capacity = df_filtered["capacity_kg"].sum()
num_plants = df_filtered["plant"].nunique()
num_materials = df_filtered["chemical_material"].nunique()

st.subheader("Key Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Capacity (kg)", f"{total_capacity:,.0f}")
kpi2.metric("Number of Plants", num_plants)
kpi3.metric("Number of Materials", num_materials)

st.markdown("---")

# Aggregate capacity by plant
df_by_plant = (
    df_filtered
    .groupby(["plant", "latitude", "longitude"], as_index=False)
    .agg({"capacity_kg": "sum"})
    .sort_values("capacity_kg", ascending=False)
)

# Bar chart: Plant vs Capacity
st.subheader("Capacity by Plant")
bar_chart = (
    alt.Chart(df_by_plant)
    .mark_bar()
    .encode(
        x=alt.X("plant:N", sort="-y", title="Plant"),
        y=alt.Y("capacity_kg:Q", title="Total Capacity (kg)"),
        tooltip=["plant", alt.Tooltip("capacity_kg:Q", title="Capacity (kg)")]
    )
    .properties(width=700, height=400)
)
st.altair_chart(bar_chart, use_container_width=True)

# Stacked bar: Material capacity by Plant
st.subheader("Material Capacity by Plant")
df_mat = (
    df_filtered
    .groupby(["plant", "chemical_material"], as_index=False)
    .agg({"capacity_kg": "sum"})
)
stacked = (
    alt.Chart(df_mat)
    .mark_bar()
    .encode(
        x=alt.X("plant:N", sort=alt.EncodingSortField(field="capacity_kg", order="descending"), title="Plant"),
        y=alt.Y("capacity_kg:Q", title="Capacity (kg)"),
        color=alt.Color("chemical_material:N", title="Material"),
        tooltip=["plant", "chemical_material", alt.Tooltip("capacity_kg:Q", title="Capacity (kg)")]
    )
    .properties(width=700, height=400)
)
st.altair_chart(stacked, use_container_width=True)

st.markdown("---")

# Map: Plot plants with total capacity
st.subheader("Plant Locations Map")
# Prepare data for map
df_map = df_by_plant.copy()
df_map["capacity_scaled"] = df_map["capacity_kg"] / df_map["capacity_kg"].max() * 200000  # scale for radius

# Define PyDeck layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_map,
    get_position=["longitude", "latitude"],
    get_radius="capacity_scaled",
    get_fill_color=[255, 140, 0, 160],
    pickable=True,
)

# Set the viewport location
view_state = pdk.ViewState(
    latitude=df_map["latitude"].mean(),
    longitude=df_map["longitude"].mean(),
    zoom=4,
    pitch=0
)

# Render the deck.gl map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>Plant:</b> {plant} <br/>"
                "<b>Capacity (kg):</b> {capacity_kg}",
        "style": {"color": "white"}
    }
)

st.pydeck_chart(r)

# Show raw data if needed
with st.expander("View Filtered Data"):
    st.dataframe(df_filtered.reset_index(drop=True))