import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="FOMC Trader's Dashboard", page_icon="📊", layout="wide")

# Sidebar Title
st.sidebar.title("FOMC Trader's Assistant 📈")
st.sidebar.markdown("Get actionable insights and make better trading decisions.")
st.sidebar.markdown("---")

# Initialize session state for navigation
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "Meeting Summary"  # Default tab

# Sidebar Navigation Buttons
if st.sidebar.button("Meeting Summary", key="summary"):
    st.session_state.current_tab = "Meeting Summary"

if st.sidebar.button("Market Reactions", key="reactions"):
    st.session_state.current_tab = "Market Reactions"

if st.sidebar.button("Interest Rate Trends", key="rates"):
    st.session_state.current_tab = "Interest Rate Trends"

if st.sidebar.button("Chatbot Assistant", key="chatbot"):
    st.session_state.current_tab = "Chatbot Assistant"

if st.sidebar.button("Trading Cheat Sheet", key="cheatsheet"):
    st.session_state.current_tab = "Trading Cheat Sheet"

# Sample FOMC Data
fomc_summary = """
**Latest FOMC Decision**:  
- The Federal Reserve maintained the interest rate at **5.25%**, emphasizing their focus on curbing inflation.  
- **Key Takeaways**:  
   1. Inflation remains above target but is trending downward.  
   2. The Fed hinted at potential rate hikes if inflation persists.  
   3. Markets interpreted this as neutral to slightly hawkish, leading to mixed reactions.  
"""

market_reactions_data = {
    "Index": ["S&P 500", "NASDAQ", "Dow Jones"],
    "Pre-FOMC (%)": [-0.3, -0.5, 0.1],
    "Post-FOMC (%)": [0.5, 1.0, -0.2],
}

interest_rate_data = {
    "Meeting Date": ["2023-12", "2024-03", "2024-06", "2024-09", "2024-12"],
    "Interest Rate (%)": [4.50, 4.75, 5.00, 5.25, 5.25],
}

# Main Content Based on the Selected Tab
st.title("FOMC Trader's Dashboard 📖")

# **1. Meeting Summary**
if st.session_state.current_tab == "Meeting Summary":
    st.header("FOMC Meeting Summary 🌟")
    st.markdown(fomc_summary)
    st.info("Understanding the Fed's decisions can help you predict how the stock market might react.")
    st.write("""
    **Quick Tips for Trading FOMC Outcomes**:  
    - Rate hikes can pressure growth stocks (tech-heavy indices like NASDAQ).  
    - Dovish comments (pausing rate hikes) often boost market sentiment.  
    """)

# **2. Market Reactions**
elif st.session_state.current_tab == "Market Reactions":
    st.header("Market Reactions to FOMC Decisions 📊")
    st.write("Here's how major indices performed before and after the latest FOMC meeting:")
    reactions_df = pd.DataFrame(market_reactions_data)
    st.table(reactions_df)

    # Example visualization using Plotly
    fig = px.bar(reactions_df, x="Index", y=["Pre-FOMC (%)", "Post-FOMC (%)"],
                 title="Market Performance Before and After FOMC",
                 labels={"value": "Percentage Change", "variable": "Period"},
                 barmode="group")
    st.plotly_chart(fig)

# **3. Interest Rate Trends**
elif st.session_state.current_tab == "Interest Rate Trends":
    st.header("Interest Rate Trends 📈")
    st.write("Understand how interest rates have changed historically and what projections look like.")
    rates_df = pd.DataFrame(interest_rate_data)
    st.line_chart(rates_df.set_index("Meeting Date"), width=0, height=0)
    st.markdown("""
    **Why It Matters**:  
    - Rising rates can slow economic growth, affecting cyclical and growth stocks.  
    - Stable or falling rates often signal a positive environment for equities.  
    """)

# **4. Chatbot Assistant**
elif st.session_state.current_tab == "Chatbot Assistant":
    st.header("Chat with the Assistant 🤖")
    st.write("Ask me questions about FOMC meetings, interest rates, or how they affect stocks!")
    user_query = st.text_input("Enter your question:")

    # Basic chatbot logic
    def chatbot_response(query):
        if "interest rate" in query.lower():
            return "Interest rates represent the cost of borrowing money. Higher rates tend to slow the economy and hurt stock prices."
        elif "inflation" in query.lower():
            return "Inflation is when prices rise over time. The Fed raises rates to control inflation."
        elif "stocks" in query.lower():
            return "Higher rates often hurt growth stocks (like tech), while stable rates benefit equities overall."
        elif "next meeting" in query.lower():
            return "The next FOMC meeting is scheduled for September 20, 2024."
        else:
            return "I can help with questions about interest rates, inflation, and the stock market. Try asking about these topics!"

    if user_query:
        st.write(f"**Bot:** {chatbot_response(user_query)}")

# **5. Trading Cheat Sheet**
elif st.session_state.current_tab == "Trading Cheat Sheet":
    st.header("FOMC Trading Cheat Sheet 📖")
    st.markdown("""
    **Common Scenarios**:  
    1. **Rate Hike**:  
       - Likely Impact: Growth stocks (e.g., tech) decline; value stocks and bonds may perform better.  
       - Suggested Action: Consider defensive sectors like utilities and healthcare.  

    2. **Rate Hold**:  
       - Likely Impact: Market stability; may benefit growth and cyclical stocks.  
       - Suggested Action: Monitor commentary for future hikes or cuts.  

    3. **Rate Cut**:  
       - Likely Impact: Broad market rally, especially in growth sectors.  
       - Suggested Action: Focus on high-beta stocks or ETFs.  
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.write("📧 **Contact us**: fomc-trader-support@example.com")
