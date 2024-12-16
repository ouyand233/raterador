import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    """Render the Market Reactions page."""
    st.header("Market Reactions to FOMC Decisions 📊")
    st.write("Here's how major indices performed before and after the latest FOMC meeting:")

    # Sample market reactions data
    market_reactions_data = {
        "Index": ["S&P 500", "NASDAQ", "Dow Jones"],
        "Pre-FOMC (%)": [-0.3, -0.5, 0.1],
        "Post-FOMC (%)": [0.5, 1.0, -0.2],
    }
    reactions_df = pd.DataFrame(market_reactions_data)

    # Display data in a table
    st.subheader("Performance Data")
    st.table(reactions_df)

    # Visualization of market performance before and after FOMC
    st.subheader("Performance Visualization")
    fig = px.bar(
        reactions_df,
        x="Index",
        y=["Pre-FOMC (%)", "Post-FOMC (%)"],
        title="Market Performance Before and After FOMC",
        labels={"value": "Percentage Change", "variable": "Period"},
        barmode="group",
        color_discrete_sequence=["#2E5BFF", "#FF6B6B"]  # Custom color palette for better contrast
    )
    st.plotly_chart(fig)

    # Insights Section
    st.subheader("Key Insights")
    st.markdown("""
    - **NASDAQ**: Experienced the highest post-FOMC performance with a 1% gain, indicating growth-oriented stocks benefitted.
    - **S&P 500**: A moderate 0.5% increase reflects a mixed market sentiment.
    - **Dow Jones**: Declined slightly, possibly due to underperformance in industrial sectors.
    """)

    st.info("Use these insights to better understand how market indices react to FOMC decisions.")

# Entry Point for Standalone Execution
if __name__ == "__main__":
    # Page Configuration
    st.set_page_config(
        page_title="Market Reactions",
        page_icon="📊",
        layout="wide"
    )
    render()
