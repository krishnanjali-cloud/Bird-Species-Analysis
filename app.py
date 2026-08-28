# import pandas as pd
import streamlit as st
import plotly.express as px
# import sqlite3
import plotly.graph_objects as go

from data_processing import(
    load_excel_data,clean_data,add_features
)

df = load_excel_data()
df = clean_data(df)
df = add_features(df)

# from database import create_database
# create_database(df)

st.set_page_config(
    page_title="Bird Biodiversity Analytics",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

.main {
    background-color: #f5f7f4;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

.stButton>button {
    border-radius: 10px;
}

h1 {
    font-weight: 700;
}

h2 {
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

st.title("🐦 Bird Species Observation Analytics")

st.markdown(
    """
    ### Biodiversity Monitoring & Conservation Intelligence

    Explore bird species distribution, habitat preference,
    seasonal patterns, environmental conditions and conservation
    priorities across forest and grassland ecosystems.
    """
)

st.sidebar.header("🔎 Dashboard Filters")

habitat_filter = st.sidebar.multiselect(
    "Habitat",
    options=sorted(df["Habitat"].dropna().unique()),
    default=sorted(df["Habitat"].dropna().unique())
)

admin_filter = st.sidebar.multiselect(
    "Administrative Unit",
    options=sorted(df["Admin_Unit_Code"].dropna().unique()),
    default=sorted(df["Admin_Unit_Code"].dropna().unique())
)

species_filter = st.sidebar.multiselect(
    "Bird Species",
    options=sorted(df["Common_Name"].dropna().unique())
)

month_filter = st.sidebar.multiselect(
    "Month",
    options=sorted(df["Month"].dropna().unique())
)
filtered_df = df[
    df["Habitat"].isin(habitat_filter)
    &
    df["Admin_Unit_Code"].isin(admin_filter)
]
if species_filter:

    filtered_df = filtered_df[
        filtered_df["Common_Name"].isin(
            species_filter
        )
    ]

if month_filter:

    filtered_df = filtered_df[
        filtered_df["Month"].isin(
            month_filter
        )
    ]
if st.sidebar.button("🔄 Reset Filters"):

    st.rerun()
csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="filtered_bird_observations.csv",
    mime="text/csv"
)

with st.expander("📊 About the Dataset", expanded=False):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Records",
            f"{len(df):,}"
        )

    with col2:
        st.metric(
            "Unique Species",
            f"{df['Scientific_Name'].nunique():,}"
        )

    with col3:
        forest_count = df[
            df["Habitat"] == "Forest"
        ]["Scientific_Name"].nunique()

        st.metric(
            "Forest Species",
            f"{forest_count:,}"
        )

    with col4:
        grassland_count = df[
            df["Habitat"] == "Grassland"
        ]["Scientific_Name"].nunique()

        st.metric(
            "Grassland Species",
            f"{grassland_count:,}"
        )

    st.markdown("---")

    st.markdown("""
    **Dataset Coverage**

    This dashboard compares bird observations across
    Forest and Grassland habitats using species,
    observation, environmental, and conservation-related
    information.
    """)

st.subheader("📊 Data Quality")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Records",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Duplicate Records",
        f"{df.duplicated().sum():,}"
    )

with col3:
    st.metric(
        "Missing Values",
        f"{df.isna().sum().sum():,}"
    )

# ============================================================
# KPI CALCULATIONS
# ============================================================

# KPI 1 — Total Observations
total_observations = len(df)


# KPI 2 — Unique Species
unique_species = (
    df["Scientific_Name"]
    .dropna()
    .nunique()
)


# KPI 3 — Habitats Covered
habitats_covered = (
    df["Habitat"]
    .dropna()
    .nunique()
)


# KPI 4 — Watchlist Species
watchlist_species = (
    df[
        df["PIF_Watchlist_Status"]
        .astype(str)
        .str.strip()
        .str.upper()
        .isin(["YES", "Y", "TRUE", "1"])
    ]["Scientific_Name"]
    .dropna()
    .nunique()
)


# KPI 5 — Administrative Units
administrative_units = (
    df["Admin_Unit_Code"]
    .dropna()
    .nunique()
)


# KPI 6 — Sampling Plots
sampling_plots = (
    df["Plot_Name"]
    .dropna()
    .nunique()
)

# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📊 Key Biodiversity Indicators")

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        label="🐦 Total Observations",
        value=f"{total_observations:,}"
    )


with col2:
    st.metric(
        label="🦜 Unique Species",
        value=f"{unique_species:,}"
    )


with col3:
    st.metric(
        label="🌿 Habitats Covered",
        value=f"{habitats_covered:,}"
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        label="⚠️ Watchlist Species",
        value=f"{watchlist_species:,}"
    )


with col5:
    st.metric(
        label="📍 Admin Units",
        value=f"{administrative_units:,}"
    )


with col6:
    st.metric(
        label="🔬 Sampling Plots",
        value=f"{sampling_plots:,}"
    )

#======================================================
# NAVIGATION TABS #
#======================================================  
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Overview",
    "🐦 Species",
    "📅 Temporal",
    "🌦️ Environment",
    "🛡️ Conservation"
])

with tab1:
    # ============================================================
    # GRAPH 1 — OBSERVATIONS BY HABITAT
    # ============================================================

    st.subheader("🌿 Observations by Habitat")

    habitat_data = (
        df.groupby("Habitat")
        .size()
        .reset_index(name="Observation_Count")
    )

    fig1 = px.bar(
        habitat_data,
        x="Habitat",
        y="Observation_Count",
        text="Observation_Count",
        title="Bird Observations by Habitat",
        labels={
            "Habitat": "Habitat",
            "Observation_Count": "Number of Observations"
        },
        template="plotly_white"
    )

    fig1.update_traces(
        textposition="outside",
        hovertemplate=(
            "<b>Habitat:</b> %{x}<br>"
            "<b>Observations:</b> %{y:,}<extra></extra>"
        )
    )

    fig1.update_layout(
        height=450,
        xaxis_title="Habitat",
        yaxis_title="Number of Observations"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.info(
        "💡 Business Insight: "
        "The chart compares bird observation activity across "
        "Forest and Grassland habitats. Differences in observation "
        "counts can help identify which habitats require greater "
        "monitoring attention and support habitat-management planning."
    )

    # ============================================================
    # GRAPH 2 — SPECIES BY HABITAT
    # ============================================================

    st.subheader("🌿 Species by Habitat")

    species_habitat = (
        df.groupby("Habitat")["Scientific_Name"]
        .nunique()
        .reset_index(name="Unique_Species")
    )

    fig2 = px.bar(
        species_habitat,
        x="Habitat",
        y="Unique_Species",
        text="Unique_Species",
        title="Unique Bird Species by Habitat",
        labels={
            "Habitat": "Habitat",
            "Unique_Species": "Unique Species"
        },
        template="plotly_white"
    )

    fig2.update_traces(
        textposition="outside",
        hovertemplate=(
            "<b>Habitat:</b> %{x}<br>"
            "<b>Unique Species:</b> %{y}<extra></extra>"
        )
    )

    fig2.update_layout(
        height=450
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.info(
        "💡 Business Insight: "
        "The chart compares species diversity across habitats, "
        "helping identify which habitat supports a greater variety "
        "of bird species and where biodiversity monitoring may be "
        "prioritized."
    )

    pass


with tab2:
    # ============================================================
        # GRAPH 3 — TOP 10 SPECIES
        # ============================================================
    
        st.subheader("🏆 Top 10 Species")
    
        top_species = (
            df["Scientific_Name"]
            .value_counts()
            .head(10)
            .reset_index()
        )
    
        top_species.columns = [
            "Scientific_Name",
            "Observation_Count"
        ]
    
        top_species = top_species.sort_values(
            "Observation_Count",
            ascending=True
        )
    
        fig3 = px.bar(
            top_species,
            x="Observation_Count",
            y="Scientific_Name",
            orientation="h",
            text="Observation_Count",
            title="Top 10 Most Frequently Observed Bird Species",
            labels={
                "Scientific_Name": "Species",
                "Observation_Count": "Observations"
            },
            template="plotly_white"
        )
    
        fig3.update_traces(
            textposition="outside"
        )
    
        fig3.update_layout(
            height=550
        )
    
        st.plotly_chart(
            fig3,
            use_container_width=True
        )
    
        st.info(
            "💡 Business Insight: "
            "The chart identifies the most frequently observed bird "
            "species, helping conservation teams prioritize species "
            "monitoring and better understand patterns of bird activity."
        )
    
        # ============================================================
        # GRAPH 4 — YEARLY OBSERVATION TREND
        # ============================================================
    
        st.subheader("📈 Yearly Observation Trend")
    
        yearly_data = (
            df.dropna(subset=["Year"])
            .groupby("Year")
            .size()
            .reset_index(name="Observation_Count")
        )
    
        yearly_data["Year"] = yearly_data["Year"].astype(int)
    
        yearly_data = yearly_data.sort_values("Year")
    
        fig4 = px.line(
            yearly_data,
            x="Year",
            y="Observation_Count",
            markers=True,
            title="Yearly Bird Observation Trend",
            labels={
                "Year": "Year",
                "Observation_Count": "Number of Observations"
            },
            template="plotly_white"
        )
    
        fig4.update_traces(
            hovertemplate=(
                "<b>Year:</b> %{x}<br>"
                "<b>Observations:</b> %{y:,}<extra></extra>"
            )
        )
    
        fig4.update_layout(
            height=450
        )
    
        st.plotly_chart(
            fig4,
            use_container_width=True
        )
    
        st.info(
            "💡 Business Insight: "
            "The yearly trend helps identify changes in bird observation "
            "activity over time, supporting long-term monitoring and "
            "data-driven conservation planning."
        )
    # ============================================================
    # GRAPH 5 — MONTHLY OBSERVATION TREND
    # ============================================================

        st.subheader("📅 Monthly Observation Trend")

        monthly_data = (
            df.dropna(subset=["Month_Number"])
            .groupby("Month_Number")
            .size()
            .reset_index(name="Observation_Count")
        )

        monthly_data["Month_Number"] = (
            monthly_data["Month_Number"].astype(int)
        )

        month_names = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }

        monthly_data["Month"] = (
            monthly_data["Month_Number"]
            .map(month_names)
        )

        monthly_data = monthly_data.sort_values("Month_Number")

        fig5 = px.line(
            monthly_data,
            x="Month",
            y="Observation_Count",
            markers=True,
            title="Monthly Bird Observation Trend",
            labels={
                "Month": "Month",
                "Observation_Count": "Number of Observations"
            },
            template="plotly_white"
        )

        fig5.update_traces(
            hovertemplate=(
                "<b>Month:</b> %{x}<br>"
                "<b>Observations:</b> %{y:,}<extra></extra>"
            )
        )

        fig5.update_layout(
            height=450,
            xaxis=dict(
                categoryorder="array",
                categoryarray=list(month_names.values())
            )
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

        st.info(
            "💡 Business Insight: "
            "Monthly trends help identify seasonal variations in bird "
            "observation activity, supporting better planning of field "
            "surveys and conservation monitoring."
        )
        # ============================================================
        # GRAPH 6 — YEAR × HABITAT HEATMAP
        # ============================================================

        st.subheader("📅 Year × Habitat Heatmap")

        heatmap_data = (
            df.dropna(subset=["Year"])
            .groupby(["Year", "Habitat"])
            .size()
            .reset_index(name="Observation_Count")
        )

        heatmap_pivot = heatmap_data.pivot(
            index="Habitat",
            columns="Year",
            values="Observation_Count"
        ).fillna(0)

        fig6 = px.imshow(
            heatmap_pivot,
            text_auto=True,
            aspect="auto",
            title="Observation Activity by Year and Habitat",
            labels={
                "x": "Year",
                "y": "Habitat",
                "color": "Observations"
            },
            color_continuous_scale="Viridis"
        )

        fig6.update_layout(
            height=500
        )

        st.plotly_chart(
            fig6,
            use_container_width=True
        )

        st.info(
            "💡 Business Insight: "
            "The heatmap reveals changes in bird observation activity "
            "across Forest and Grassland habitats over the years, "
            "helping identify important habitat-year patterns for "
            "focused monitoring and conservation planning."
        )
pass


with tab3:
    
# ============================================================
# GRAPH 7 — OBSERVATION HOUR
# ============================================================

    st.subheader("🕐 Observation Hour")

    hour_data = (
        df.dropna(subset=["Observation_Hour"])
        .groupby("Observation_Hour")
        .size()
        .reset_index(name="Observation_Count")
    )

    hour_data["Observation_Hour"] = (
        hour_data["Observation_Hour"].astype(int)
    )

    hour_data = hour_data.sort_values("Observation_Hour")

    fig7 = px.line(
        hour_data,
        x="Observation_Hour",
        y="Observation_Count",
        markers=True,
        title="Bird Observations by Hour of Day",
        labels={
            "Observation_Hour": "Observation Hour",
            "Observation_Count": "Number of Observations"
        },
        template="plotly_white"
    )

    fig7.update_layout(
        height=450
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

    st.info(
        "💡 Business Insight: "
        "The chart identifies peak observation hours, helping "
        "optimize the timing of field surveys and improve the "
        "efficiency of bird monitoring activities."
    )

    # ============================================================
    # GRAPH 8 — TEMPERATURE VS HUMIDITY
    # ============================================================

    st.subheader("🌡️💧 Temperature vs Humidity")

    environment_data = df.dropna(
        subset=["Temperature", "Humidity"]
    ).copy()

    fig8 = px.scatter(
        environment_data,
        x="Temperature",
        y="Humidity",
        color="Habitat",
        hover_data=[
            "Scientific_Name",
            "Habitat"
        ],
        title="Temperature vs Humidity During Bird Observations",
        labels={
            "Temperature": "Temperature",
            "Humidity": "Humidity"
        },
        template="plotly_white"
    )

    fig8.update_layout(
        height=550
    )

    st.plotly_chart(
        fig8,
        use_container_width=True
    )

    st.info(
        "💡 Business Insight: "
        "The relationship between temperature and humidity provides "
        "insights into the environmental conditions associated with "
        "bird observations, supporting better field-survey planning "
        "and habitat monitoring."
    )

    # ============================================================
    # GRAPH 9 — IDENTIFICATION METHOD
    # ============================================================

    st.subheader("🔍 Identification Method")

    id_data = (
        df["ID_Method"]
        .value_counts()
        .reset_index()
    )

    id_data.columns = [
        "ID_Method",
        "Observation_Count"
    ]

    fig9 = px.bar(
        id_data,
        x="ID_Method",
        y="Observation_Count",
        text="Observation_Count",
        title="Bird Observations by Identification Method",
        labels={
            "ID_Method": "Identification Method",
            "Observation_Count": "Number of Observations"
        },
        template="plotly_white"
    )

    fig9.update_traces(
        textposition="outside"
    )

    fig9.update_layout(
        height=500
    )

    st.plotly_chart(
        fig9,
        use_container_width=True
    )

    st.info(
        "💡 Business Insight: "
        "The chart identifies the most commonly used bird "
        "identification methods, helping improve survey "
        "consistency and support better monitoring practices."
    )

    pass


with tab4:
    # ============================================================
    # GRAPH 10 — WATCHLIST SPECIES BY HABITAT
    # ============================================================

    st.subheader("⚠️🌿 Watchlist Species by Habitat")

    watchlist = df[
        df["PIF_Watchlist_Status"]
        .astype(str)
        .str.strip()
        .str.upper()
        .isin(["1", "TRUE", "YES", "Y"])
    ].copy()

    watchlist_data = (
        watchlist.groupby("Habitat")["Scientific_Name"]
        .nunique()
        .reset_index(name="Watchlist_Species")
    )

    fig10 = px.bar(
        watchlist_data,
        x="Habitat",
        y="Watchlist_Species",
        text="Watchlist_Species",
        title="Watchlist Species by Habitat",
        labels={
            "Habitat": "Habitat",
            "Watchlist_Species": "Number of Watchlist Species"
        },
        template="plotly_white"
    )

    fig10.update_traces(
        textposition="outside"
    )

    fig10.update_layout(
        height=450
    )

    st.plotly_chart(
        fig10,
        use_container_width=True
    )

    st.info(
        "💡 Business Insight: "
        "The chart identifies habitats supporting more watchlist "
        "species, helping conservation teams prioritize habitat "
        "protection and focused biodiversity monitoring."
    )

    # ============================================================
    # GRAPH 11 — REGIONAL STEWARDSHIP
    # ============================================================

    st.subheader("🛡️ Regional Stewardship")

    stewardship = df[
        df["Regional_Stewardship_Status"]
        .astype(str)
        .str.strip()
        .str.upper()
        .isin(["1", "TRUE", "YES", "Y"])
    ].copy()

    stewardship_data = (
        stewardship.groupby("Habitat")["Scientific_Name"]
        .nunique()
        .reset_index(name="Stewardship_Species")
    )

    fig11 = px.bar(
        stewardship_data,
        x="Habitat",
        y="Stewardship_Species",
        text="Stewardship_Species",
        title="Regional Stewardship Species by Habitat",
        labels={
            "Habitat": "Habitat",
            "Stewardship_Species": "Stewardship Species"
        },
        template="plotly_white"
    )

    fig11.update_traces(
        textposition="outside"
    )

    fig11.update_layout(
        height=450
    )

    st.plotly_chart(
        fig11,
        use_container_width=True
    )

    st.info(
        "💡 Business Insight: "
        "The chart identifies habitats with a greater presence "
        "of stewardship species, helping prioritize targeted "
        "monitoring and regional conservation planning."
    )

    # ============================================================
    # GRAPH 12 — DISTURBANCE ANALYSIS
    # ============================================================

    st.subheader("⚠️🌳 Disturbance Analysis")

    disturbance_data = (
        df.groupby("Disturbance")
        .size()
        .reset_index(name="Observation_Count")
    )

    fig12 = px.bar(
        disturbance_data,
        x="Disturbance",
        y="Observation_Count",
        text="Observation_Count",
        title="Bird Observations by Disturbance Level",
        labels={
            "Disturbance": "Disturbance Level",
            "Observation_Count": "Number of Observations"
        },
        template="plotly_white"
    )

    fig12.update_traces(
        textposition="outside"
    )

    fig12.update_layout(
        height=450
    )

    st.plotly_chart(
        fig12,
        use_container_width=True
    )

    st.info(
        "💡 Business Insight: "
        "The chart highlights variation in bird observations across "
        "disturbance levels, helping identify areas that may require "
        "focused monitoring and habitat-management attention."
    )
    pass


with tab5:
    # ============================================================
    # GRAPH 13 — ADMINISTRATIVE UNIT HOTSPOTS
    # ============================================================

    st.subheader("📍🔥 Administrative Unit Hotspots")

    admin_data = (
        df.groupby("Admin_Unit_Code")
        .size()
        .reset_index(name="Observation_Count")
    )

    admin_data = (
        admin_data
        .sort_values(
            "Observation_Count",
            ascending=False
        )
        .head(10)
    )

    admin_data = admin_data.sort_values(
        "Observation_Count",
        ascending=True
    )

    fig13 = px.bar(
        admin_data,
        x="Observation_Count",
        y="Admin_Unit_Code",
        orientation="h",
        text="Observation_Count",
        title="Top 10 Administrative Units by Observation Activity",
        labels={
            "Admin_Unit_Code": "Administrative Unit",
            "Observation_Count": "Observations"
        },
        template="plotly_white"
    )

    fig13.update_traces(
        textposition="outside"
    )

    fig13.update_layout(
        height=550
    )

    st.plotly_chart(
        fig13,
        use_container_width=True
    )

    st.info(
        "💡 Business Insight: "
        "The chart highlights administrative units with higher "
        "observation activity, helping prioritize field surveys "
        "and targeted biodiversity monitoring."
    )

    # ============================================================
    # GRAPH 14 — PLOT-LEVEL BIODIVERSITY
    # ============================================================

    st.subheader("🌿🔬 Plot-Level Biodiversity")

    plot_data = (
        df.groupby("Plot_Name")["Scientific_Name"]
        .nunique()
        .reset_index(name="Unique_Species")
    )

    plot_data = (
        plot_data
        .sort_values(
            "Unique_Species",
            ascending=False
        )
        .head(15)
    )

    plot_data = plot_data.sort_values(
        "Unique_Species",
        ascending=True
    )

    fig14 = px.bar(
        plot_data,
        x="Unique_Species",
        y="Plot_Name",
        orientation="h",
        text="Unique_Species",
        title="Top 15 Plots by Species Diversity",
        labels={
            "Plot_Name": "Plot",
            "Unique_Species": "Unique Species"
        },
        template="plotly_white"
    )

    fig14.update_traces(
        textposition="outside"
    )

    fig14.update_layout(
        height=600
    )

    st.plotly_chart(
        fig14,
        use_container_width=True
    )

    st.info(
        "💡 Business Insight: "
        "The chart identifies plots with greater species diversity, "
        "helping conservation teams recognize areas that may be "
        "valuable for biodiversity monitoring and habitat management."
    )

    # ============================================================
    # GRAPH 15 — SEX DISTRIBUTION
    # ============================================================

    st.subheader("👥 Sex Distribution")

    sex_data = (
        df["Sex"]
        .value_counts()
        .reset_index()
    )

    sex_data.columns = [
        "Sex",
        "Observation_Count"
    ]

    fig15 = px.pie(
        sex_data,
        names="Sex",
        values="Observation_Count",
        hole=0.45,
        title="Bird Observation Distribution by Sex",
        template="plotly_white"
    )

    fig15.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig15.update_layout(
        height=500
    )

    st.plotly_chart(
        fig15,
        use_container_width=True
    )

    st.info(
        "💡 Business Insight: "
        "The sex distribution provides an overview of the observed "
        "bird population composition and can support population-level "
        "monitoring and further ecological analysis."
    )
pass










