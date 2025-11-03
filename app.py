"""Streamlit dashboard for monitoring traffic and energy supply."""
from __future__ import annotations

import datetime as dt
import math
from dataclasses import dataclass
from typing import Iterable

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Urban Monitoring Dashboard",
    page_icon="🚦",
    layout="wide",
)

st.title("🚦 Urban Monitoring Dashboard")
st.caption(
    "Analyse in Echtzeit Trends zur Verkehrsauslastung und zur Energieversorgung in einer Stadt. "
    "Die Daten werden simuliert, orientieren sich aber an realistischen Schwankungen."
)


@dataclass
class Sensor:
    """Simple representation of a sensor or energy node."""

    id: str
    name: str
    region: str
    latitude: float
    longitude: float


REGIONS = ["Innenstadt", "Nord", "Süd", "Ost", "West"]
TRAFFIC_SENSORS: tuple[Sensor, ...] = (
    Sensor("T-101", "Innenstadt Süd", "Innenstadt", 52.515, 13.405),
    Sensor("T-102", "Innenstadt Nord", "Innenstadt", 52.525, 13.405),
    Sensor("T-201", "Nordallee", "Nord", 52.565, 13.321),
    Sensor("T-301", "Südring", "Süd", 52.455, 13.385),
    Sensor("T-401", "Ostring", "Ost", 52.515, 13.515),
    Sensor("T-501", "Westtangente", "West", 52.495, 13.295),
)
@st.cache_data(show_spinner=False)
def build_time_index(days: int = 30) -> pd.DatetimeIndex:
    """Return hourly timestamps for the last ``days`` days."""

    end = dt.datetime.now().replace(minute=0, second=0, microsecond=0)
    start = end - dt.timedelta(days=days)
    return pd.date_range(start=start, end=end, freq="1h")


@st.cache_data(show_spinner=False)
def build_traffic_data(_index: Iterable[pd.Timestamp]) -> pd.DataFrame:
    rng = np.random.default_rng(seed=42)
    records = []

    for timestamp in _index:
        hour = timestamp.hour
        daily_factor = 1.2 if timestamp.weekday() < 5 else 0.8
        rush_hour = 1.8 if hour in range(7, 10) or hour in range(16, 19) else 1.0
        night = 0.35 if 0 <= hour <= 5 else 1.0

        for sensor in TRAFFIC_SENSORS:
            base_volume = rng.normal(1200, 150)
            seasonal = 1 + 0.3 * math.sin((timestamp.timetuple().tm_yday / 365) * 2 * math.pi)
            volume = max(0, base_volume * daily_factor * rush_hour * night * seasonal)
            avg_speed = rng.normal(45, 5) * (1.5 - min(volume / 2200, 1.2))
            congestion = max(0, min(volume / 2000, 1))

            records.append(
                {
                    "timestamp": timestamp,
                    "sensor_id": sensor.id,
                    "sensor_name": sensor.name,
                    "region": sensor.region,
                    "vehicle_volume": round(volume),
                    "average_speed": max(5, avg_speed),
                    "congestion": congestion,
                }
            )

    return pd.DataFrame.from_records(records)


ENERGY_SOURCES = ("Solar", "Wind", "Wasserkraft", "Biomasse", "Import")


@st.cache_data(show_spinner=False)
def build_energy_data(_index: Iterable[pd.Timestamp]) -> pd.DataFrame:
    rng = np.random.default_rng(seed=123)
    records = []

    for timestamp in _index:
        hour = timestamp.hour
        demand_base = 300 + 40 * math.sin((hour - 6) / 24 * 2 * math.pi) + rng.normal(0, 10)
        demand_season = 50 * math.sin((timestamp.timetuple().tm_yday / 365) * 2 * math.pi)
        demand = max(250, demand_base + demand_season)

        solar = max(0, rng.normal(80, 15) * max(0, math.sin((hour - 6) / 12 * math.pi)))
        wind = max(0, rng.normal(110, 20))
        hydro = max(0, rng.normal(60, 5))
        biomass = max(0, rng.normal(40, 4))
        total_generation = solar + wind + hydro + biomass
        imports = max(0, demand - total_generation)

        for source_name, value in zip(
            ENERGY_SOURCES,
            (solar, wind, hydro, biomass, imports),
            strict=True,
        ):
            records.append(
                {
                    "timestamp": timestamp,
                    "source": source_name,
                    "output_mw": value,
                    "demand_mw": demand,
                }
            )

    return pd.DataFrame.from_records(records)


def metric_delta(current: float, previous: float) -> tuple[str, str]:
    """Return formatted value and delta string for st.metric."""

    delta = current - previous
    percentage = (delta / previous * 100) if previous else 0
    delta_str = f"{delta:+.1f} ({percentage:+.1f}%)"
    return f"{current:,.0f}", delta_str


# Sidebar configuration ----------------------------------------------------
with st.sidebar:
    st.header("Filter")
    days = st.slider("Zeitraum (Tage)", min_value=3, max_value=60, value=14)
    region = st.selectbox("Region", options=["Alle"] + REGIONS)
    compare_weekend = st.checkbox("Wochenende vergleichen", value=True)

index = build_time_index(days=days)
traffic_df = build_traffic_data(index)
energy_df = build_energy_data(index)

if region != "Alle":
    traffic_df = traffic_df[traffic_df["region"] == region]

latest_time = traffic_df["timestamp"].max()
previous_time = latest_time - dt.timedelta(hours=1)

# Key metrics --------------------------------------------------------------
latest_traffic = traffic_df[traffic_df["timestamp"] == latest_time]
previous_traffic = traffic_df[traffic_df["timestamp"] == previous_time]

current_volume = latest_traffic["vehicle_volume"].mean()
previous_volume = previous_traffic["vehicle_volume"].mean()

current_speed = latest_traffic["average_speed"].mean()
previous_speed = previous_traffic["average_speed"].mean()

current_congestion = latest_traffic["congestion"].mean()
previous_congestion = previous_traffic["congestion"].mean()

col1, col2, col3 = st.columns(3)
with col1:
    value, delta = metric_delta(current_volume, previous_volume)
    st.metric("Fahrzeuge / Stunde", value, delta)
with col2:
    value, delta = metric_delta(current_speed, previous_speed)
    st.metric("Durchschnittsgeschwindigkeit (km/h)", value, delta)
with col3:
    st.metric(
        "Stauindex",
        f"{current_congestion:.2f}",
        f"{(current_congestion - previous_congestion):+.2f}",
    )

st.divider()

# Traffic section ----------------------------------------------------------
st.subheader("Verkehrsauslastung")

volume_chart = (
    alt.Chart(traffic_df)
    .mark_line()
    .encode(
        x="timestamp:T",
        y=alt.Y("mean(vehicle_volume)", title="Fahrzeuge / Stunde"),
        color="region:N",
        tooltip=["timestamp:T", "region:N", "mean(vehicle_volume):Q"],
    )
    .properties(height=320)
)

speed_chart = (
    alt.Chart(traffic_df)
    .mark_line(color="#FF7F0E")
    .encode(
        x="timestamp:T",
        y=alt.Y("mean(average_speed)", title="km/h"),
        tooltip=["timestamp:T", "mean(average_speed):Q"],
    )
    .properties(height=320)
)

st.altair_chart(volume_chart, use_container_width=True)

col_a, col_b = st.columns((2, 1), gap="large")
with col_a:
    st.altair_chart(speed_chart, use_container_width=True)
with col_b:
    st.markdown("""
    **Interpretationstipps**

    * Hohe Werte im Stauindex (>0,7) deuten auf kritische Engpässe hin.
    * Eine sinkende Durchschnittsgeschwindigkeit bei gleichzeitig hohem Verkehrsaufkommen
      weist auf eine mögliche Überlastung hin.
    * Nutzen Sie die Region-Auswahl in der Sidebar, um lokale Hotspots zu identifizieren.
    """)

# Map visualization --------------------------------------------------------
map_df = pd.DataFrame(
    [
        {
            "lat": sensor.latitude,
            "lon": sensor.longitude,
            "name": sensor.name,
            "Auslastung": traffic_df[traffic_df["sensor_id"] == sensor.id][
                "vehicle_volume"
            ].iloc[-1],
        }
        for sensor in TRAFFIC_SENSORS
        if (region == "Alle") or (sensor.region == region)
    ]
)

st.map(map_df, latitude="lat", longitude="lon", size="Auslastung", zoom=10)

st.divider()

# Energy section -----------------------------------------------------------
st.subheader("Energieversorgung")

latest_energy = energy_df[energy_df["timestamp"] == latest_time]

energy_mix = (
    latest_energy.groupby("source", as_index=False)["output_mw"].sum()
    .sort_values("output_mw", ascending=False)
)

total_generation = energy_mix["output_mw"].sum()
current_demand = latest_energy["demand_mw"].max()

generation_metric, generation_delta = metric_delta(
    total_generation, energy_df[energy_df["timestamp"] == previous_time]["output_mw"].sum()
)

demand_metric, demand_delta = metric_delta(
    current_demand,
    energy_df[energy_df["timestamp"] == previous_time]["demand_mw"].max(),
)

col4, col5 = st.columns(2)
with col4:
    st.metric("Stromerzeugung (MW)", generation_metric, generation_delta)
with col5:
    st.metric("Nachfrage (MW)", demand_metric, demand_delta)

energy_chart = (
    alt.Chart(energy_df)
    .mark_area()
    .encode(
        x="timestamp:T",
        y=alt.Y("sum(output_mw)", stack="normalize", title="Anteil"),
        color=alt.Color("source:N", legend=alt.Legend(title="Quelle")),
        tooltip=["timestamp:T", "source:N", "sum(output_mw):Q"],
    )
    .properties(height=320)
)

st.altair_chart(energy_chart, use_container_width=True)

comparison_chart = (
    alt.Chart(energy_df)
    .mark_line()
    .transform_aggregate(
        generation="sum(output_mw)",
        demand="max(demand_mw)",
        groupby=["timestamp"],
    )
    .transform_fold(["generation", "demand"], as_=["Kategorie", "Leistung"])
    .encode(
        x="timestamp:T",
        y=alt.Y("Leistung:Q", title="MW"),
        color="Kategorie:N",
        tooltip=["timestamp:T", "Kategorie:N", "Leistung:Q"],
    )
    .properties(height=320)
)

st.altair_chart(comparison_chart, use_container_width=True)

if compare_weekend:
    st.subheader("Vergleich Werktag vs. Wochenende")
    traffic_df = traffic_df.assign(is_weekend=traffic_df["timestamp"].dt.dayofweek >= 5)
    weekend_chart = (
        alt.Chart(traffic_df)
        .mark_bar()
        .encode(
            x=alt.X("is_weekend:N", title=""),
            y=alt.Y("mean(vehicle_volume)", title="Ø Fahrzeuge / Stunde"),
            color=alt.Color("is_weekend:N", legend=alt.Legend(title="")),
            tooltip=["is_weekend:N", "mean(vehicle_volume):Q"],
        )
        .properties(height=200)
    )
    st.altair_chart(weekend_chart, use_container_width=True)

st.info(
    "Die dargestellten Werte basieren auf einem simulierten Datensatz, der stündliche Messwerte "
    "mehrerer Sensoren und Energiequellen abbildet. Die Logik lässt sich leicht an reale "
    "Schnittstellen (z. B. REST- oder SQL-Backends) anpassen."
)
