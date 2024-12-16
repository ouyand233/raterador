import pandas as pd
import plotly.express as px
import streamlit as st

# Sidebar Navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio(
    "Choose a feature:",
    ["Homepage", "FOMC Projections Visual"]
)

# Homepage
if page == "Homepage":
    st.title("🏠 Welcome to the Data Visualization App")
    st.write(
        """
        Use the sidebar to navigate to different features of this app.  
        - View **FOMC Participants' Projections** for the Federal Funds Rate.  
        - Explore other interactive visuals or tools.  
        """
    )

# FOMC Projections Visual Page
elif page == "FOMC Projections Visual":
    # Title and Introduction
    st.title("📊 FOMC Participants' Projections for the Federal Funds Rate")
    st.markdown(
        """
        See where the **Federal Open Market Committee (FOMC)** thinks rates are headed!  
        Each dot shows a participant's projection for the federal funds rate, aiming for **maximum employment** and **stable inflation**.

        ⚠️ **Note:** These projections are **not binding**, but they’re the **most likely predictions** because the **final rate is decided by a vote**!  

        Use the dropdown below to explore projections for each year. 📅
        """
    )

    # Data preparation
    data = {
        "Rate (%)": [
            "2-2.25", "2.25-2.5", "2.5-2.75", "2.75-3", "3.0-3.25", "3.25-3.5",
            "3.5-3.75", "3.75-4", "4-4.25", "4.25-4.5", "4.5-4.75", "4.75-5",
            "5.25-5.5", "5.5-5.75", "5.75-6"
        ],
        "2024": [0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 7, 2, 0, 0, 0],
        "2025": [0, 0, 0, 0, 2, 6, 6, 3, 1, 1, 0, 0, 0, 0, 0],
        "2026": [0, 1, 3, 6, 2, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],
        "2027": [0, 2, 3, 5, 2, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    }

    # Convert data to DataFrame
    df = pd.DataFrame(data)
    df_melted = df.melt(id_vars=["Rate (%)"], var_name="Year", value_name="Count")

    # Streamlit UI for year selection
    selected_year = st.selectbox("📅 **Select a Year:**", options=["2024", "2025", "2026", "2027"])

    # Filter data for the selected year and exclude zero counts
    filtered_data = df_melted[(df_melted["Year"] == selected_year) & (df_melted["Count"] > 0)]

    # Create the interactive bar chart with a professional color palette
    fig = px.bar(
        filtered_data,
        x="Rate (%)",
        y="Count",
        title=f"📈 FOMC Rate Projections for {selected_year}",
        labels={"Count": "Number of Participants", "Rate (%)": "Rate Range (%)"},
        color="Rate (%)",
        color_discrete_sequence=px.colors.qualitative.Prism,  # Professional color palette
    )

    # Customize layout for better readability
    fig.update_layout(
        xaxis_title="Rate Range (%)",
        yaxis_title="Number of Participants",
        showlegend=False,
        template="plotly_white",
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)

