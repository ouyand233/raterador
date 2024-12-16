import streamlit as st
from modules.ai_responder import AzureOpenAIHelper
from modules.sentence_transformer import query_faiss

def main():
    # Minimalist interface
    st.title("FOMC Insights Chat")
    st.subheader("Ask your questions about FOMC meetings and get insightful responses!")

    # Step 1: User provides API key (only once, can be hidden if hardcoded)
    api_key = st.text_input("Enter your Azure OpenAI API Key:", type="password", placeholder="Your Azure OpenAI API Key")
    if not api_key:
        st.warning("Please enter your API key to use the app.")
        return

    # Initialize AI Responder
    ai_helper = AzureOpenAIHelper(api_key=api_key)

    # Step 2: Input for user questions
    user_question = st.text_input("Ask a question:", placeholder="Example: What were the FOMC decisions in September 2023?")
    if user_question:
        # Process the question: query FAISS for context + ChatGPT for the response
        with st.spinner("Retrieving insights..."):
            try:
                # Query FAISS for relevant context
                faiss_results = query_faiss(user_question)
                if not faiss_results:
                    st.error("No relevant data found in the FAISS index.")
                    return

                # Combine FAISS results into context
                context = "\n".join([result['text'] for result in faiss_results])

                # Combine context and user question into a single prompt
                combined_prompt = f"Context: {context}\n\nQuestion: {user_question}\n\nAnswer the question using the context provided."

                # Generate AI response using Azure OpenAI
                ai_response = ai_helper.get_response(
                    message=combined_prompt,
                    instruction="You are an assistant providing insights on FOMC meetings.",
                    temperature=0.7  # Adjust for creativity
                )

                # Display the AI-generated response
                if ai_response:
                    st.success("Response:")
                    st.write(ai_response)
                else:
                    st.error("Failed to retrieve a response. Please try again.")

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
