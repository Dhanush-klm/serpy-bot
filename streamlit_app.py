import streamlit as st
from serpapi import GoogleSearch
from transformers import pipeline

def summarize_snippets(snippets):
    model_name = "sshleifer/distilbart-cnn-12-6"
    revision = "a4f8f3e"
    summarizer = pipeline("summarization", model=model_name, revision=revision)
    try:
        # Increase max_length and min_length for longer summaries
        summary = summarizer(snippets, max_length=1000, min_length=200)  # Adjusted values
        if summary and 'summary_text' in summary[0]:
            return summary[0]['summary_text']
        else:
            return "No summary available."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit interface
st.title('SERPY-BOT')
query = st.text_input("Enter your search query:")

if st.button('Search and Summarize'):
    params = {
      "engine": "google",
      "q": query,
      "api_key": "81f8af02e883bda0668d2d66290fc9bcbbca7c24c8403b76f38f241269988bd0",
      "num": 15
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results.get("organic_results", [])
    answer_box = results.get("answer_box", {})

    snippets = []
    
    for result in organic_results:
        snippet = result.get('snippet')
        if snippet:
            snippets.append(snippet)

    # Handle answer box content; include relevant fields like title or snippets
    if answer_box:
        if 'snippet' in answer_box and answer_box['snippet']:
            snippets.append(answer_box['snippet'])
        if 'title' in answer_box and answer_box['title']:
            snippets.append(answer_box['title'])

    # Append other data that could be relevant from the answer box
    for key in ['description', 'linked_snippet']:
        if key in answer_box and answer_box[key]:
            snippets.append(answer_box[key])

    # Join snippets into a single text block for summarization
    snippets_text = " ".join(snippets)
    summary = summarize_snippets(snippets_text)
    st.write("snippets_text")
    st.markdown("### Summary:")
    st.markdown(f"**{summary}**")  # Display the summary in bold
    st.markdown("<style>body {background-color: black;}</style>", unsafe_allow_html=True)  # Change the background to black
