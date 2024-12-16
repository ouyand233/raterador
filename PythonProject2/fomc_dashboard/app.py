import sys
import os
import streamlit as st

# Dynamically add the project root to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fomc_dashboard.modules.ai_responder import AzureOpenAIHelper
from fomc_dashboard.modules.sentence_transformer import query_faiss

def main():
    # Page Configuration
    st.set_page_config(page_title="RateRadar: FOMC Insights", page_icon="📡", layout="wide")

    # Absolute Path for Image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, "../.."))
    image_path = os.path.join(root_dir, "assets/powell.jpg")

    # Custom Styling (Set New Color Theme)
    st.markdown("""
        <style>
        .main-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #2E5BFF;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #5D5FEF;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header Section
    st.markdown('<h1 class="main-title">📡 RateRadar: Your FOMC Companion</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Track the Fed. Predict the Market. Stay Ahead.</p>', unsafe_allow_html=True)

    # Load and Display the Image
    try:
        with open(image_path, "rb") as file:
            image_data = file.read()

        st.image(image_data, caption="Chairman Jerome Powell, Federal Reserve", use_column_width=True)
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
        response_placeholder = st.empty()

    if user_question:
        with st.spinner("⏳ Gathering insights for you..."):
            try:
                faiss_results = query_faiss(user_question)
                if not faiss_results:
                    response_placeholder.error("No relevant data found for your query.")
                    return

                context = "\n".join([result['text'] for result in faiss_results])
                combined_prompt = f"Context: {context}\n\nQuestion: {user_question}\n\nAnswer concisely."

                ai_response = ai_helper.get_response(
                    message=combined_prompt,
                    instruction="You are an assistant providing FOMC insights.",
                    temperature=0.7
                )

                if ai_response:
                    response_placeholder.markdown(f"""
                    <div class="response-box">{ai_response}</div>
                    """, unsafe_allow_html=True)
                else:
                    response_placeholder.error("Sorry, no response available. Please try again.")

            except Exception as e:
                response_placeholder.error(f"An error occurred: {e}")

    st.markdown("---")
    st.markdown('<p class="footer">📡 RateRadar: Your trusted
