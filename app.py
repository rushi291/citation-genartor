import requests
import streamlit as st
import spacy

# Download the spaCy model if it hasn't been downloaded already
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Fetch data from the paginated API
def fetch_data(api_url):
    data = []
    page = 1
    while True:
        response = requests.get(api_url, params={'page': page})
        if response.status_code != 200:
            st.error("Failed to fetch data from the API.")
            break
        page_data = response.json()
        if 'data' not in page_data or not page_data['data']['data']:
            break
        data.extend(page_data['data']['data'])
        page += 1
    return data

# Identify citations using NLP
def identify_citations(response_data):
    citations = []
    for obj in response_data:
        response_text = obj.get('response', '')
        sources = obj.get('source', [])
        response_doc = nlp(response_text.lower())
        found_citations = []
        for source in sources:
            if isinstance(source, dict):
                source_context = source.get('context', '')
                if isinstance(source_context, str):
                    source_doc = nlp(source_context.lower())
                    # Check if the response text contains tokens similar to the source context
                    if response_doc.similarity(source_doc) > 0.7:  # Similarity threshold
                        found_citations.append({
                            "context": source_context,
                            "id": source.get('id', ''),
                            "link": source.get('link', '')
                        })
            else:
                st.warning("Unexpected source format: expected a dictionary.")
        citations.append({
            "response": response_text,
            "citations": found_citations
        })
    return citations

def main():
    st.title("Citations Viewer")
    api_url = "https://devapi.beyondchats.com/api/get_message_with_sources"
    st.write("Fetching data from the API...")
    response_data = fetch_data(api_url)
    if response_data:
        st.write("Identifying citations...")
        citations = identify_citations(response_data)
        st.subheader("Citations:")
        if citations:
            for citation_info in citations:
                response_text = citation_info["response"]
                found_citations = citation_info["citations"]
                st.write(f"**Response:** {response_text}")
                if found_citations:
                    for citation in found_citations:
                        st.write(f"Context: {citation['context']}")
                        st.write(f"ID: {citation['id']}, Link: {citation['link']}")
                else:
                    st.write("No citations found for this response.")
                st.write("---")  # Separator between responses
        else:
            st.write("No citations found.")

if __name__ == "__main__":
    main()