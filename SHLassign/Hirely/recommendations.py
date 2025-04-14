import requests
import json
from bs4 import BeautifulSoup
import streamlit as st

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from langchain.prompts import ChatPromptTemplate

#For using langchain's integration with Qdrant
from langchain_qdrant import QdrantVectorStore
#For Qdrant client
from qdrant_client import QdrantClient

from django.conf import settings

from .models import Assessment

OPENAI_API_KEY = settings.OPENAI_API_KEY

embedding = OpenAIEmbeddings(model= "text-embedding-3-small", openai_api_key = OPENAI_API_KEY)

#Connecting to Qdrant
qdrant = QdrantClient(host="localhost", port=6333)

vectorstore = QdrantVectorStore(
    client = qdrant,
    collection_name="assessments",
    embedding= embedding
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

llm = ChatOpenAI(model_name = "gpt-3.5-turbo", openai_api_key= OPENAI_API_KEY)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You're a helpful assistant that recommends SHL assessments. "
     "Given a job description or a hiring query and context from a vector store, return a list (1 to 10) of assessments "
     "in Python dictionary format with keys: title, link, duration_minutes, test_type, description. "
     "Only include relevant items. Return the final output as a valid Python dictionary, not a string or JSON."),
    ("human", "Query: {query}\n\nContext:\n{context}")
])

qa_chain = prompt | llm 

#Extract main text from URL
def extract_text_from_url(url: str) -> str:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator="", strip=True)
            return text[:3000]
        return ""
    except Exception as e:
        print(f"Error extracting from url: {e}")
        return ""
  
#Handle Natural Language and Job Description inputs
""" 
def query_assessments(input_text: str) -> list:
    if input_text.startswith("http://") or input_text.startswith("https://"):
        input_text = extract_text_from_url(input_text)
    
    query_embedding = embedding.embed_query(input_text)
    st.write("Query embedding (first 5 values):", query_embedding[:5])
    
    docs = retriever.invoke(input_text)
    
    if not docs:
        st.warning("No documents retrieved from Qdrant.")
        return []
    
    result = qa_chain.invoke({"query": input_text})
    response_text = result["content"] if isinstance(result, dict) else result
        
    try:
        json_data = json.loads(response_text)
        return json_data
    except Exception as e:
        st.write("Parsing error: {e}")
        st.write("Response was:", response_text)
        return []
    
"""
def query_assessments(input_text: str) -> list:
    if input_text.startswith("http://") or input_text.startswith("https://"):
        input_text = extract_text_from_url(input_text)

    query_embedding = embedding.embed_query(input_text)
    print("Query embedding (first 5 values):", query_embedding[:5])

    docs = retriever.invoke(input_text)

    if not docs:
        print("No documents retrieved from Qdrant.")
        return []

    context = "\n\n".join([doc.page_content for doc in docs])

    result = qa_chain.invoke({"query": input_text, "context": context})

    # Handle response as dictionary directly
    response_dict = result.content if hasattr(result, "content") else result

    try:
        if isinstance(response_dict, dict):
            return response_dict.get("assessments", [])
        elif isinstance(response_dict, str):
            parsed = eval(response_dict)
            if isinstance(parsed, dict):
                return parsed.get("assessments", [])
            elif isinstance(parsed, list):
                return parsed
        print("Unexpected structure:", response_dict)
        return []
    except Exception as e:
        print("Parsing error:", e)
        print("Response was:", response_dict)
        return []


