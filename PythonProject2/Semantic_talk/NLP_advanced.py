import streamlit as st
from transformers import pipeline
import PyPDF2
import re


# Load FinBERT Sentiment Analysis Pipeline
@st.cache_resource  # Cache the model to avoid reloading
def load_finbert_model():
    return pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")


finbert = load_finbert_model()


# Function to clean text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespaces
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters
    return text


# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Function to split text into smaller chunks
def split_text_into_chunks(text, chunk_size=512):
    """
    Splits the input text into smaller chunks of a specified size.
    Args:
        text (str): The input text to be split.
        chunk_size (int): Maximum number of characters in each chunk (default: 512).
    Returns:
        list: A list of text chunks.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


# Streamlit App
st.title("🦅 FOMC Sentiment Analysis with FinBERT")
st.markdown("""
Upload FOMC statements or minutes (TXT or PDF format) to analyze whether the tone is 
**Positive, Negative, or Neutral** based on sentiment analysis using **FinBERT**, a financial domain-specific model. 📊
""")

# File Upload
uploaded_file = st.file_uploader("Upload a file (TXT or PDF format)", type=["txt", "pdf"])

if uploaded_file:
    # Extract text from the uploaded file
    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    else:
        st.error("Unsupported file format.")
        st.stop()

    # Clean the text
    cleaned_text = clean_text(text)

    # Split the text into smaller chunks
    chunks = split_text_into_chunks(cleaned_text, chunk_size=512)

    # Analyze each chunk
    st.subheader("📈 Sentiment Analysis Results")
    overall_sentiments = []
    for i, chunk in enumerate(chunks):
        result = finbert(chunk)
        sentiment = result[0]["label"]
        confidence = result[0]["score"]
        overall_sentiments.append((sentiment, confidence))

        # Display results for each chunk
        st.write(f"**Chunk {i + 1}:**")
        st.write(f"- **Sentiment:** {sentiment}")
        st.write(f"- **Confidence Score:** {confidence:.2f}")

    # Aggregate sentiment results
    sentiment_counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    for sentiment, _ in overall_sentiments:
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
        else:
            st.warning(f"Unexpected sentiment label: {sentiment}")

    # Display overall sentiment summary
    st.subheader("📊 Overall Sentiment Summary")
    st.write(f"**Positive Chunks:** {sentiment_counts['POSITIVE']}")
    st.write(f"**Negative Chunks:** {sentiment_counts['NEGATIVE']}")
    st.write(f"**Neutral Chunks:** {sentiment_counts['NEUTRAL']}")
