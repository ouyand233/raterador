import pandas as pd
import plotly.express as px
import streamlit as st

# Ensure set_page_config is called only when running standalone
if __name__ == "__main__":
    st.set_page_config(
        page_title="FOMC SEP Projections",
        page_icon="📊",
        layout="wide"
    )

def render():
    """Render the SEP Projections Page."""
    # Page Title and Introduction
    st.title("📊 FOMC Participants' Projections for the Federal Funds Rate")
    st.markdown("""
    The **Federal Open Market Committee (FOMC)** releases projections for the federal funds rate,  
    showing where participants think rates are headed in the coming years.

    - **Why it matters**: Projections influence markets and investor sentiment.  
    - Use the dropdown below to explore year-by-year projections for federal funds rates.  
    """)

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

    # Convert data to DataFrame and reshape it
    df = pd.DataFrame(data)
    df_melted = df.melt(id_vars=["Rate (%)"], var_name="Year", value_name="Count")

    # User selection for year
    st.subheader("🔍 Explore Projections")
    selected_year = st.selectbox("📅 **Select a Year:**", options=["2024", "2025", "2026", "2027"])

    # Filter data for the selected year
    filtered_data = df_melted[(df_melted["Year"] == selected_year) & (df_melted["Count"] > 0)]

    # Show a warning if no data is available
    if filtered_data.empty:
        st.warning(f"No projections available for {selected_year}.")
        return

    # Bar chart visualization
    fig = px.bar(
        filtered_data,
        x="Rate (%)",
        y="Count",
        title=f"📈 Federal Funds Rate Projections for {selected_year}",
        labels={"Count": "Number of Participants", "Rate (%)": "Rate Range (%)"},
        color="Rate (%)",
        color_discrete_sequence=px.colors.sequential.Blues,
    )
    fig.update_layout(
        xaxis_title="Rate Range (%)",
        yaxis_title="Number of Participants",
        template="plotly_white",
        font=dict(size=14),
        title_x=0.5,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Insights Section
    st.subheader("📌 Key Insights")
    st.markdown(f"""
    - In **{selected_year}**, projections show most participants expect rates to fall within specific ranges.
    - These projections influence policy discussions and provide insights into how the Fed plans to manage **inflation** and **employment** goals.
    """)
    st.info("💡 Use these insights to align your market expectations and trading strategies.")

# Ensure standalone execution
if __name__ == "__main__":
    render()
