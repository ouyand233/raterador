import streamlit as st
import os
import sys

# Dynamically add the project root to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fomc_dashboard.modules.ai_responder import AzureOpenAIHelper
from fomc_dashboard.modules.sentence_transformer import query_faiss

def main():
    # Page Configuration
    st.set_page_config(page_title="RateRadar: FOMC Insights", page_icon="📡", layout="wide")

    # Custom Styling for UX Enhancements
    st.markdown("""
        <style>
        /* Header Styling */
        .main-title {
            text-align: center;
            font-size: 32px;  /* Reduced size for better harmony */
            font-weight: bold;
            color: #2E5BFF;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;  /* Slightly smaller than before */
            color: #5D5FEF;
            margin-top: -10px;  /* Tighten spacing between title and subtitle */
        }
        .slogan {
            text-align: center;
            font-size: 16px;  /* Smaller, complementary to title */
            font-style: italic;
            color: #666666;
            margin-bottom: 20px;  /* Add space below slogan */
        }
        /* AI Response Box */
        .response-box {
            background-color: #F9F9F9;  /* Light gray background */
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #DDDDDD;  /* Subtle border */
            font-size: 18px;  /* Increased font size for better readability */
            color: #333333;
        }
        /* Footer Styling */
        .footer {
            text-align: center;
            font-size: 14px;
            color: #888888;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header Section
    st.markdown('<h1 class="main-title">📡 RateRadar: Your FOMC Companion</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">The ultimate guide to FOMC decisions, market reactions, and economic insights.</p>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">Track the Fed. Predict the Market. Stay Ahead.</p>', unsafe_allow_html=True)

    st.markdown("---")

    # Absolute Path for Image
    absolute_image_path = "D:/PythonProject2/fomc_dashboard/assets/powell.jpg"  # Full path to the image
    try:
        st.image(
            absolute_image_path,
            caption="Chairman Jerome Powell, Federal Reserve",
            use_column_width=True  # Resize the image
        )
    except Exception as e:
        st.error(f"Error loading image: {e}")

    st.markdown("---")

    # API Key Input Section
    with st.expander("🔐 Set Up Your Assistant: Enter Azure OpenAI API Key", expanded=True):
        api_key = st.text_input("Enter API Key:", type="password", placeholder="Your Azure OpenAI API Key")

    if not api_key:
        st.warning("⚠️ Please enter your API key to start using the assistant.")
        return

    # Initialize AI Responder
    ai_helper = AzureOpenAIHelper(api_key=api_key)

    # Main Chat Assistant Section
    st.subheader("🤖 Your Personalized FOMC Assistant")
    st.markdown("""
    - Ask questions about **FOMC meetings**, interest rates, or economic trends.  
    - Get real-time insights tailored for **traders**, **investors**, and **economy enthusiasts**.  
    """)

    # Two-Column Layout for Input and Output
    col1, col2 = st.columns([1.5, 2.5])

    with col1:
        st.markdown("**Ask Your Question Here:**")
        user_question = st.text_input(
            "Example: 'What were the FOMC decisions in December 2023?'",
            placeholder="Type your question here...",
            key="user_input"
        )

    with col2:
        st.markdown("**Assistant's Response:**")
        response_placeholder = st.empty()  # Placeholder for the AI response

    # Handle User Question
    if user_question:
        with st.spinner("⏳ Gathering insights for you..."):
            try:
                # Query FAISS for context
                faiss_results = query_faiss(user_question)
                if not faiss_results:
                    response_placeholder.error("No relevant data found for your query.")
                    return

                # Combine FAISS results into context
                context = "\n".join([result['text'] for result in faiss_results])

                # Combine context and question into a prompt
                combined_prompt = f"Context: {context}\n\nQuestion: {user_question}\n\nAnswer concisely as a personal assistant."

                # Get AI Response
                ai_response = ai_helper.get_response(
                    message=combined_prompt,
                    instruction="You are an assistant providing insights on FOMC meetings, interest rates, and economic policy.",
                    temperature=0.7
                )

                # Display AI Response
                if ai_response:
                    response_placeholder.markdown(f"""
                    <div class="response-box">{ai_response}</div>
                    """, unsafe_allow_html=True)
                else:
                    response_placeholder.error("Sorry, I could not retrieve a response. Please try again.")

            except Exception as e:
                response_placeholder.error(f"An error occurred: {e}")

    # Footer Section with Slogan
    st.markdown("---")
    st.markdown('<p class="footer">📡 RateRadar: Your trusted companion for navigating FOMC insights and decisions.</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
