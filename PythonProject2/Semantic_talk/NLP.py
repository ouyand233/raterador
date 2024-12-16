import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import PyPDF2
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load Predefined Hawkish/Dovish Words for Classification
hawkish_terms = ["tighten", "inflation", "hike", "reduce liquidity", "restrictive"]
dovish_terms = ["accommodative", "stimulus", "easing", "cut rates", "lower interest"]


# Function to clean text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespaces
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    return text


# Function for Sentiment Classification
def classify_sentiment(text):
    cleaned_text = clean_text(text)
    hawkish_score = sum(cleaned_text.count(term) for term in hawkish_terms)
    dovish_score = sum(cleaned_text.count(term) for term in dovish_terms)

    if hawkish_score > dovish_score:
        return "Hawkish", hawkish_score, dovish_score
    elif dovish_score > hawkish_score:
        return "Dovish", hawkish_score, dovish_score
    else:
        return "Neutral", hawkish_score, dovish_score


# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Streamlit App
st.title("🦅 FOMC Sentiment Analysis Tool")
st.markdown("""
Upload FOMC statements or minutes (TXT or PDF format) to analyze whether the tone is **Hawkish** (favoring restrictive monetary policy) 
or **Dovish** (favoring accommodative monetary policy). The tool will classify the sentiment and provide a word cloud 
to visualize key terms. 📊
""")

# File Upload
uploaded_file = st.file_uploader("Upload a file (TXT or PDF format)", type=["txt", "pdf"])

if uploaded_file:
    # Determine file type and extract text
    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    else:
        st.error("Unsupported file format.")
        st.stop()

    # Run Sentiment Analysis
    sentiment, hawkish_score, dovish_score = classify_sentiment(text)

    # Display Results
    st.subheader(f"📈 Sentiment Analysis Result: **{sentiment}**")
    st.write(f"- **Hawkish Score:** {hawkish_score}")
    st.write(f"- **Dovish Score:** {dovish_score}")

    # Generate Word Cloud
    st.subheader("Word Cloud of Uploaded Document")
    wordcloud = WordCloud(background_color="white", width=800, height=400).generate(clean_text(text))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

    # Keyword Analysis
    st.subheader("Top Hawkish and Dovish Terms")
    st.write("**Hawkish Terms Found:**", ", ".join([term for term in hawkish_terms if term in text]))
    st.write("**Dovish Terms Found:**", ", ".join([term for term in dovish_terms if term in text]))
