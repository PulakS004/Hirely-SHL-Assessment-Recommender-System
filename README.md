# Hirely - SHL Assessment Recommender System 
The SHL Assessment Recommender is an intelligent system that takes a natural language hiring query or a job description URL and returns a structured list of recommended SHL assessments. It combines web scraping, semantic vector search with Qdrant, and reasoning with OpenAI's GPT to provide tailored assessment recommendations.

#Demo

https://github.com/user-attachments/assets/39822b07-659c-4754-aa88-d605f7ad7eb9

## Tech Stack

**Web Scraping:** BeautifulSoup, requests

**Backend Framework:** Django

**Database:** PostgreSQL

**Vector DB:** Qdrant

**Embedding Model:** OpenAI text-embedding-3-small

**Language Model:** OpenAI GPT-3.5-turbo via LangChain

**Frontend:** Streamlit



## Workflow

1. Data Ingestion & Preprocessing
A custom Django management command crawls the SHL product catalog.

Extracts assessment information (title, link, duration, test type, etc.), creates a JSON file and saves it in PostgreSQL.

2. Embedding Generation
Another command generates semantic embeddings from assessment metadata using OpenAI’s text-embedding-3-small model.

These embeddings are indexed in Qdrant for similarity search.

3. User Query Flow
Users provide a hiring query (text) or job description (URL).

If a URL is provided, it’s parsed using BeautifulSoup to extract readable content.

The input is embedded and searched against Qdrant to fetch top 10 similar assessments.

4. LLM Reasoning
Retrieved documents + query are passed into a LangChain pipeline using GPT-3.5-turbo.

The LLM returns a clean Python dictionary list of recommended assessments.

5. Frontend Integration
Streamlit displays the assessment list in a readable format with links, duration, types, and descriptions.




## Demo

Insert gif or link to demo


## Run Locally

Clone the project

```bash
  git clone https://github.com/PulakS004/Hirely-SHL-Assessment-Recommender-System.git
```

Go to the project directory

```bash
  cd SHLassign
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Set up environment variables

```bash
  Add your OPENAI_API_KEY as a user environment variable in system settings.
```

Run Django setup

```bash
    python manage.py makemigrations
    python manage.py migrate
```

Scraping assessments from SHL Product Catalog website and creating embeddingd using custom Django commands

```bash
    python manage.py scrape_assessments
    python manage.py save_assessments
    python manage.py get_embeddings.py
```

Qdrant setup (via Docker)

```bash
    docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```
Running custom Django command for migrating embeddings to Qdrant

```bash
    python manage.py migrate_embeddings_to_qdrant.py
```

Start Streamlit app

```bash
    streamlit run Hirely/frontend/Hirely_app.py
```
