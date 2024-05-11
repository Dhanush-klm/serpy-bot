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
    answer_box = results.get("answer_box", [])

    links = []
    snippets = []
    

    for result in organic_results:
        title = result.get('title')
        snippet = result.get('snippet')
        link = result.get('link')
        links.append(link)
        snippets.append(snippet)
        st.markdown(f"**{title}**: {snippet}\n\n")
        # st.write(f"snippets: {snippets_text}")

    # Add snippet from answer box to snippets list
    snippets.append(answer_box['snippet'])

    # Join snippets into a single text block for summarization
    # After collecting snippets in the Streamlit app
    snippets_text = " ".join(snippets)
    summary = summarize_snippets(snippets_text)
    #st.write("Summary:", summary)

    #st.write(f"snippets: {snippets_text}")
    st.markdown("### Summary:")
    st.markdown(f"**{summary}**")  # Display the summary in bold
    st.markdown("<style>body {background-color: black;}</style>", unsafe_allow_html=True)  # Change the background to black



