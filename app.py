import streamlit as st
from pinecone import Pinecone
from openai import OpenAI  # Assuming you're using OpenAI for embedding. Adjust according to your actual client setup for embeddings.
import os
from dotenv import load_dotenv
from utils import *
import json

load_dotenv()
OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
PINECONE_API_KEY = st.secrets['PINECONE_API_KEY']

index_name = 'search-cases'
namespace = "cases_singapore_v2"

pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(index_name)

client = OpenAI(api_key=OPENAI_API_KEY)



# Streamlit app
def main():
    coram_options = load_json('entity_names/corams.json')
    lawyer_options = load_json('entity_names/lawyers.json')
    law_firm_options = load_json('entity_names/law_firms.json')
    case_title_options = load_json('entity_names/case_titles.json')
    citation_options = load_json('entity_names/citations.json')

    st.title("Singapore Law Search Engine")
    st.markdown('This testbench uses a "Vector Search" to help lawyers more easily find cases. This means the search is based on the underlying meaning of words, rather than a traditional text-to-text match. A concrete example is searching for "fines" will return results like "financial penalty" or "charges" because from a contexual meaning perspective, they are similar.')
    st.markdown('The Vector Database has 8109 Singaporean cases from 2000-2024.')
    st.markdown('Note: Single Use Filters are filters that can only be used alone. For example, you cannot use Citation filter with year because the citation already describes the year. Otherwise, you will receive no results.')

    # Search bar
    query = st.text_input("Enter your search query:", "")
    year_selected = st.slider('Case year',2000, 2024, (2000, 2024))

    # Filters
    coram_selected = st.selectbox('Coram', ['All'] + coram_options)
    lawyer_selected = st.selectbox('Lawyer Name', ['All'] + lawyer_options)
    law_firm_selected = st.selectbox('Law Firm', ['All'] + law_firm_options)
    case_type_selected = st.selectbox('Case Type', ['All', 'SGHC', 'SGHCI', 'SGHCR', 'SGHCF', 'SGHCA', 'SGCA', 'SGCAI'])
    case_title_selected = st.selectbox('Case Title (Single Use Filter)', ['All'] + case_title_options)
    citation_selected = st.selectbox('Citation (Single Use Filter)', ['All'] + citation_options)

    if st.button("Search"):
        if query:
            query_embedding = get_embedding(client, query)

            metadata_dict = build_metadata(year_selected, lawyer_selected, law_firm_selected, coram_selected, case_type_selected, case_title_selected, citation_selected)

            pinecone_res = pinecone_index.query( 
                vector=query_embedding,
                top_k=1000,
                include_metadata=True,
                filter = metadata_dict,
                namespace=namespace
                )

            results = pinecone_res['matches']

            unique_results = remove_duplicates(results)


            if unique_results:
                st.markdown(f'<div style="text-align: right;">Results returned:{len(unique_results)}</div><br>', unsafe_allow_html=True)
                for i, match in enumerate(unique_results):
                    case_title = match['metadata'].get('case_title', 'No title available')
                    citation = match['metadata'].get('citation', 'No citation available')
                    section_title = match['metadata'].get('section_title', 'No section title available')
                    link = match['metadata'].get('original_link', 'No link available')
                    text = match['metadata'].get('text', 'No text available')
                    cosine_similarity_score = match.get('score', 'No score available')

                    st.markdown(f'##### [{clean_title(case_title)}]({link})')
                    st.text(citation)
                    st.markdown(f'###### {clean_title(section_title)}')
                    st.markdown(str(text))
                    st.markdown(f"Match : {round(cosine_similarity_score*100, 2)}%")
                    st.markdown(f"***")
            else:
                st.write("No results found.")
        else:
            st.write("Please enter a query to search.")

if __name__ == "__main__":
    main()
