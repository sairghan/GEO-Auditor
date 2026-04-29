import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import WebBaseLoader
import os

# --- Configuration ---
st.set_page_config(page_title="GEO Auditor", page_icon="🌐", layout="wide")
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# --- Logic ---
def get_page_content(url):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        return docs[0].page_content
    except Exception as e:
        return f"Error loading URL: {e}"

def audit_for_geo(content, keyword):
    prompt = f"""
    You are a Generative Engine Optimization (GEO) Auditor.
    
    TARGET KEYWORD: {keyword}
    CONTENT: {content[:15000]}
    
    TASK: Analyze this page for its 'Citation Probability' (the likelihood of an LLM citing this page in a generative response).
    
    1. GEO SCORE (0-100): Score based on depth of information, clarity of entities, and 'citation-worthiness'.
    2. ENTITY SALIENCE: Does the content clearly link the brand/keyword to the topic? 
    3. CITATION SIGNAL ANALYSIS: Does the content contain unique data, original insights, or clear headers that an LLM can easily map to a citation?
    4. GEO FIXES: Give 3 specific strategies to make the content more 'generative-friendly' (e.g., adding original statistics, defining technical terms, structure for citation).
    5. JSON-LD DATA: Generate valid 'Article' or 'Research' Schema JSON-LD that explicitly highlights the page's original research/insights.
    """
    return llm.invoke(prompt).content

# --- UI ---
st.title("🌐 GEO Auditor (Generative Engine Optimization)")
st.subheader("Ensure your content is 'Citation-Ready' for Generative AI models")

url = st.text_input("Enter Page URL to Audit")
keyword = st.text_input("Target Keyword for Citation")

if st.button("Run GEO Audit"):
    if not url or not keyword:
        st.warning("Please provide both a URL and a keyword.")
    else:
        with st.spinner("Analyzing for AI citations..."):
            content = get_page_content(url)
            if "Error" in content:
                st.error(content)
            else:
                report = audit_for_geo(content, keyword)
                st.session_state['geo_report'] = report
                st.success("GEO Audit Complete!")

if 'geo_report' in st.session_state:
    st.markdown(st.session_state['geo_report'])
    st.download_button("Download GEO Report", st.session_state['geo_report'], file_name="geo_report.md")
