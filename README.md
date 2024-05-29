# Singapore Law Search Engine

## Overview
This application was designed to allow client to easily test Vector Search capabilities. The search engine helps lawyers find Singaporean cases more effectively. 

The Vector Database contains 8109 Singaporean cases from 2000-2024. Users can apply various filters such as year, lawyer name, law firm, coram, case type, case title, and citation to refine their search results.

All components were built using Streamlit for easy deployability and simplicity. The core logic involves:
1) Getting the user query
2) Converting the user query to an embedding
3) Searching vector database for similar documents using Pinecone Algorithm
4) Parsing retrieved documents and displaying to the user

## Installation
Installation of repo is as simple as creating a virtual requirement (if needed) and installing the dependencies in requirements.txt

## Code Structure
app.py
Contains front-end code and API calls to Pinecone

utils.py
Helper functions used in utils.py

entity_names
JSON list of filters and retrieved in app.py