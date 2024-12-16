import streamlit as st
from modules.ai_responder import AzureOpenAIHelper
from modules.data_fetcher import get_fomc_meeting_dates, generate_fomc_minutes_urls
from modules.sentence_transformer import store_in_faiss, query_faiss

def main():
    st.title("Azure OpenAI with FAISS and FOMC Insights")
    st.subheader("Get Real-Time FOMC Meeting Insights and Contextual Responses")

    # Section 1: API Key Input
    api_key = st.text_input("Enter your Azure OpenAI API Key:", type="password")
    if not api_key:
        st.warning("Please enter your API Key to proceed.")
        return

    # Initialize AI Responder
    ai_helper = AzureOpenAIHelper(api_key=api_key)

    # Section 2: FOMC Meeting Data Fetching
    st.header("FOMC Meeting Data")
    if st.button("Fetch FOMC Meeting Dates"):
        with st.spinner("Fetching meeting dates from Wikipedia..."):
            try:
                WIKI_URL = "https://en.wikipedia.org/wiki/History_of_Federal_Open_Market_Committee_actions"
                meeting_dates = get_fomc_meeting_dates(WIKI_URL)
                fomc_urls = generate_fomc_minutes_urls(meeting_dates)
                st.success("FOMC meeting data fetched successfully!")
                st.write("Meeting Dates:", meeting_dates)
                st.write("Generated URLs:", fomc_urls)
            except Exception as e:
                st.error(f"Failed to fetch FOMC meeting data: {e}")

    # Section 3: Store Data in FAISS
    st.header("Store Data in FAISS Index")
    sample_paragraphs = [
        "The FOMC decided to maintain interest rates at 5.25%.",
        "Inflation expectations have declined compared to last quarter.",
        "GDP growth was revised downward due to tighter credit conditions.",
        "The Federal Reserve is monitoring labor market trends closely."
    ]
    if st.button("Store Sample Data in FAISS"):
        with st.spinner("Storing data in FAISS index..."):
            try:
                store_in_faiss(sample_paragraphs)
                st.success("Data stored successfully in FAISS index!")
            except Exception as e:
                st.error(f"Failed to store data in FAISS: {e}")

    # Section 4: Query FAISS Index
    st.header("Query FAISS Index")
    user_query = st.text_input("Enter your question to retrieve relevant context:")
    if st.button("Query FAISS"):
        if user_query:
            with st.spinner("Querying FAISS index for relevant context..."):
                try:
                    results = query_faiss(user_query)
                    st.success("FAISS Query Results:")
                    for result in results:
                        st.write(f"Text: {result['text']} | Distance: {result['distance']:.4f}")
                except Exception as e:
                    st.error(f"Failed to query FAISS: {e}")
        else:
            st.warning("Please enter a query to proceed.")

    # Section 5: Azure OpenAI Response
    st.header("Get AI-Generated Response")
    user_question = st.text_input("Enter your question about the FOMC meeting:")
    temperature = st.slider("Set Response Creativity (Temperature):", 0.0, 2.0, 1.0)
    if st.button("Get AI Response"):
        if user_question:
            with st.spinner("Fetching AI response..."):
                try:
                    response = ai_helper.get_response(
                        message=user_question,
                        instruction=(
                            "You are an assistant providing real-time updates on FOMC meetings. "
                            "Summarize key discussions, decisions, and macroeconomic implications."
                        ),
                        temperature=temperature
                    )
                    if response:
                        st.success("AI Response:")
                        st.write(response)
                    else:
                        st.error("Failed to fetch AI response. Check your API key or inputs.")
                except Exception as e:
                    st.error(f"Error fetching AI response: {e}")
        else:
            st.warning("Please enter a question to proceed.")

if __name__ == "__main__":
    main()
