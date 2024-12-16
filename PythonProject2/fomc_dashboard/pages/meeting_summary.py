import streamlit as st

def render():
    """Render the Meeting Summary page."""
    # Page Title
    st.title("📝 FOMC Meeting Summary")
    st.markdown("""
    Stay informed with the latest decisions from the **Federal Open Market Committee (FOMC)**:  
    - Key takeaways from recent meetings.  
    - Insights into monetary policy goals and market implications.  
    """)

    # Key Meeting Highlights
    st.subheader("🔑 Key Highlights from the Latest Meeting")
    st.markdown("""
    - **Date**: December 13, 2023  
    - **Decision**: The Federal Reserve maintained the federal funds rate at **5.25%**, in line with market expectations.  
    - **Goals**:  
        - **Inflation**: The Fed remains committed to reducing inflation to its 2% target.  
        - **Employment**: The labor market remains resilient despite higher interest rates.  
    - **Forward Guidance**:  
        - The Fed signaled a **data-dependent approach**, leaving the door open for future rate hikes if inflation remains persistent.
    """)

    # Market Reactions
    st.subheader("📈 Market Reactions")
    st.markdown("""
    - **Equities**:  
        - S&P 500 gained **0.5%** post-meeting as markets interpreted the Fed's stance as neutral.  
        - NASDAQ climbed **1%**, benefiting from stability in rate expectations.
    - **Bonds**:  
        - The 10-year Treasury yield dropped by **0.1%**, reflecting eased rate hike fears.  
    - **Currency**:  
        - The US Dollar weakened slightly against major currencies due to dovish undertones.  
    """)

    # Fed's Economic Outlook
    st.subheader("📊 Fed's Economic Outlook")
    st.markdown("""
    - **Inflation**: Expected to return to the 2% target by mid-2025.  
    - **GDP Growth**: Moderate growth of **1.8%** forecasted for 2024.  
    - **Unemployment Rate**: Projected to rise slightly to **4.1%** in 2024.  
    """)

    # Key Insights
    st.subheader("📌 Key Insights for Traders and Investors")
    st.markdown("""
    - The Fed's data-dependent approach signals **caution**, but stability in rates could benefit equities, particularly in growth sectors.  
    - Bond markets may stabilize if rate hike expectations ease further.  
    - Investors should monitor upcoming **CPI reports** and **labor market data** to anticipate future rate moves.
    """)

    # Actionable Takeaways
    st.info("""
    💡 **Actionable Takeaways**:  
    - Growth stocks (e.g., tech) may perform well in a stable rate environment.  
    - Keep an eye on Treasury yields and the USD for signs of changing sentiment.  
    - Follow Fed commentary for clues on rate hike timing.
    """)

# Ensure standalone execution
if __name__ == "__main__":
    st.set_page_config(
        page_title="FOMC Meeting Summary",
        page_icon="📝",
        layout="wide"
    )
    render()
