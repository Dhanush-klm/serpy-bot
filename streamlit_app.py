import streamlit as st
from serpapi import GoogleSearch
from transformers import pipeline
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def summarize_snippets(snippets):
    model_name = "sshleifer/distilbart-cnn-12-6"
    revision = "a4f8f3e"
    summarizer = pipeline("summarization", model=model_name, revision=revision, use_auth_token=True)  # Adjusted for huggingface_hub updates
    try:
        summary = summarizer(snippets, max_length=1000, min_length=200)
        return summary[0]['summary_text'] if summary else "No summary available."
    except Exception as e:
        logging.error("Failed to summarize: %s", str(e))
        return f"An error occurred: {str(e)}"

# Streamlit interface
st.title('SERPY-BOT')
query = st.text_input("Enter your search query:")

if st.button('Search and Summarize'):
    params = {
      "engine": "google",
      "q": query,
      "api_key": "your_api_key_here",  # Ensure using the correct API key
      "num": 15
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        answer_box = results.get("answer_box", {})

        snippets = [result.get('snippet') for result in organic_results if result.get('snippet')]
        
        # Extract answer box content
        if answer_box:
            snippets.extend([value for key, value in answer_box.items() if key in ['snippet', 'title', 'description', 'linked_snippet'] and value])
        
        snippets_text = " ".join(snippets)
        summary = summarize_snippets(snippets_text)
        st.markdown("### Summary:")
        st.markdown(f"**{summary}**")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logging.error("Error processing search or summarization: %s", str(e))

st.markdown("<style>body {background-color: black;}</style>", unsafe_allow_html=True)  # Change the background to black
