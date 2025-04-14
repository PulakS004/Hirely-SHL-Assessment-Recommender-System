import sys
import os

# Add the path to your Django app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SHLassign.settings')  # <-- Replace with your project name

import django
django.setup()

import streamlit as st

from Hirely.recommendations import extract_text_from_url, query_assessments

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

st.title("🔍 SHL Assessment Recommender")
st.markdown("""Enter a job description, a job post URL, or a natural language query. We'll find the best assessments for you!
            Examples:  
            - "Hiring a frontend dev skilled in React, HTML, CSS under 45 mins”  
            - “https://jobboard.com/software-engineer-jd” """
            )

user_input = st.text_area("📝 Your Query or JD URL", placeholder="E.g., I'm hiring for a Software Engineer with Python and SQL skills. Limit: 45 mins")

if st.button("Find Assessments"):
    if user_input.strip():
        with st.spinner("Analyzing and finding relevant assessments..."):
            # Check if input is a URL
            try:
                results = query_assessments(user_input)

                if results:
                    st.success(f"Top {len(results)} assessments found:")
                    for i, res in enumerate(results, start=1):
                        st.markdown(f"""
                        **{i}. {res.get('title', 'Untitled')}**
                        - Duration: {res.get('duration_minutes', 'N/A')} minutes
                        - Link to Assessment: ({res.get('link', '#')})
                        - Type: {res.get('test_type', 'N/A')}
                        - Description: {res.get('description', 'No description available.')}
                        """)
                    st.subheader("Raw Response")
                    st.markdown(f"```python\n{results}\n```")
                else:
                    st.warning("No relevant assessments found.")
                    
            except Exception as e:
                st.error(f"Error: {e}")
                
    else:
        st.warning("Please enter a query or Job description URL to proceed.")
        

