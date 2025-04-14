import requests
from bs4 import BeautifulSoup
import json
import time
import re

import openai
from django.conf import settings

from .models import Assessment

openai.api_key = settings.OPENAI_API_KEY

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

#Extract assessments function
def extract_assessments(start: int):
    params={
        "page": 32,
        "start": start,
        "type": [1,1]
    }
    
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    if response.status_code != 200:
        print(f"Failed at start={start}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    
    assessment_blocks = soup.find_all("tr", attrs={"data-entity-id": True})

    for block in assessment_blocks:
        title_tag = block.find("td", class_="custom__table-heading__title")
        if  title_tag:
          link_tag = block.find("a", href=True)
          if link_tag:
            title = title_tag.text.strip()
            relative_link = link_tag["href"].strip()
            full_link = "https://www.shl.com" + relative_link

            general_cols = block.find_all("td", class_="custom__table-heading__general")
            remote_support = False
            adaptive_support = False
            if len(general_cols) >=2:
              remote_support = general_cols[0].find("span", class_="catalogue__circle -yes") is not None
              adaptive_support = general_cols[1].find("span", class_="catalogue__circle -yes") is not None

            key_col = block.find("td", class_="custom__table-heading__general product-catalogue__keys")
            if key_col:
              key_spans = key_col.find_all("span", class_="product-catalogue__key")
              keys = [span.text.strip() for span in key_spans if span.text.strip()]

              description, duration_min = get_description_and_duration_from_detail_page(full_link)

        results.append({
            "title": title,
            "link": full_link,
            "description": description,
            "remote_support": remote_support,
            "adaptive_support": adaptive_support,
            "test_type": keys,
            "duration_minutes": duration_min
        })

    return results


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

#Get description and duration function
def get_description_and_duration_from_detail_page(url):
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all repeated sections
        all_blocks = soup.find_all("div", class_="product-catalogue-training-calendar__row typ")
        
        duration = None
        description = None

        for block in all_blocks:
            heading = block.find("h4")
            if heading:
                heading_text = heading.text.strip()
                
                if "Description" in heading_text:
                    p_tag = block.find("p")
                    if p_tag:
                        description = p_tag.text.strip()
                        
                elif "Assessment length" in heading_text:
                    p_tag = block.find("p")
                    if p_tag:
                        match = re.search(r"\d+", p_tag.text.strip() if p_tag else None)
                        if match:
                            duration = int(match.group())
        
        if duration is None:
            print("Assessment length not found.")
            
        return description, duration
    
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return None, None

#Dictionary for test-type
TEST_TYPE_MAP = {
    "A": "Ability and Aptitude",
    "B": "Biodata and Situational Judgement",
    "C": "Competencies",
    "D": "Development and 360",
    "E": "Assessment Exercises",
    "K": "Knowledge and Skills",
    "P": "Personality and Behaviour",
    "S": "Simulations"
}


#Function to convert each assessment detail into a string
def get_embedding_text(assessment):
    types_full = [TEST_TYPE_MAP.get(t, t) for t in assessment.test_type]
    return (
        f"Title: {assessment.title}. "
        f"Description: {assessment.description}"
        f"Remote Support: {assessment.remote_support}. "
        f"Adaptive Support: {assessment.adaptive_support}. "
        f"Types: {', '.join(types_full)} "
        f"Duration: {assessment.duration_min or 'unknown'} minutes."
    )
    
#Function to convert generate OpenAI Embeddings 
def generate_embedding(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding