import streamlit as st
import os
import pandas as pd
from datetime import datetime

# Page configuration - Must be the first Streamlit command
st.set_page_config(
    page_title="SEO Rank Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.api_service import SerperAPI
from utils.data_service import DataService
from components.forms import render_input_forms

# Custom CSS to improve the appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #424242;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background-color: #1E88E5;
        color: white;
    }
    .footer {
        margin-top: 3rem;
        text-align: center;
        color: #9E9E9E;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'domains' not in st.session_state:
    st.session_state.domains = []
if 'keywords' not in st.session_state:
    st.session_state.keywords = []
if 'search_type' not in st.session_state:
    st.session_state.search_type = "search"
if 'result_size' not in st.session_state:
    st.session_state.result_size = 10
if 'location' not in st.session_state:
    st.session_state.location = "Turkey"
if 'results_history' not in st.session_state:
    st.session_state.results_history = {}
if 'current_results' not in st.session_state:
    st.session_state.current_results = None

# Simple header
st.markdown("# SEO Rank Tracker")
st.markdown("Check your domain rankings on Google search results")

# Initialize services
data_service = DataService()
api_service = SerperAPI()

# Render simplified input forms
track_button_clicked = render_input_forms()

# Process tracking if button is clicked
if track_button_clicked:
    if not st.session_state.domains:
        st.error("Please add at least one domain")
    elif not st.session_state.keywords:
        st.error("Please add at least one keyword")
    else:
        with st.spinner("Fetching ranking data..."):
            try:
                results = {}
                
                # Progress bar for tracking
                progress_bar = st.progress(0)
                total_items = len(st.session_state.keywords)
                
                # Determine language based on location
                language = "tr" if st.session_state.location == "Turkey" else "en"
                country_code = "tr" if st.session_state.location == "Turkey" else "us"
                
                # Get results for each keyword
                for i, keyword in enumerate(st.session_state.keywords):
                    progress_text = f"Processing: {keyword}"
                    st.caption(progress_text)
                    
                    search_results = api_service.get_search_results(
                        keyword, 
                        st.session_state.search_type,
                        st.session_state.location,
                        language,
                        country_code
                    )
                    
                    # Find rankings for each domain
                    keyword_results = {}
                    for domain in st.session_state.domains:
                        result = data_service.find_domain_rank(search_results, domain, st.session_state.result_size)
                        keyword_results[domain] = result
                    
                    results[keyword] = keyword_results
                    
                    # Update progress
                    progress_bar.progress((i + 1) / total_items)
                
                # Store the current results
                st.session_state.current_results = results
                
                # Add to history with timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.results_history[timestamp] = {
                    'results': results,
                    'domains': st.session_state.domains.copy(),
                    'keywords': st.session_state.keywords.copy(),
                    'search_type': st.session_state.search_type,
                    'result_size': st.session_state.result_size,
                    'location': st.session_state.location,
                }
                
                st.success("Rankings found!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")

# Display results in a simplified format
if st.session_state.current_results:
    st.markdown("## Results")
    
    # Get results using the updated data service
    df = data_service.results_to_dataframe(
        st.session_state.current_results, 
        st.session_state.domains, 
        st.session_state.keywords
    )
    
    # Create two tables - one for rankings and one for URLs
    st.markdown("### Rankings")
    
    # Filter columns for rankings only (exclude URL columns)
    ranking_cols = ['Keyword'] + [col for col in df.columns if not col.endswith('_url') and col != 'Keyword']
    ranking_df = df[ranking_cols]
    
    # Display the rankings table
    st.dataframe(ranking_df, use_container_width=True, height=300)
    
    st.markdown("### URLs")
    url_data = []
    
    # Create a table with keywords and found URLs
    for _, row in df.iterrows():
        url_row = {'Keyword': row['Keyword']}
        
        for domain in st.session_state.domains:
            url_col = f"{domain}_url"
            if url_col in row and row[url_col]:
                url_row[domain] = row[url_col]
            else:
                url_row[domain] = "Not found"
        
        url_data.append(url_row)
    
    url_df = pd.DataFrame(url_data)
    st.dataframe(url_df, use_container_width=True, height=300)
    
    # Add simple CSV export button for complete data
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Complete Data (CSV)",
        data=csv,
        file_name="seo_rankings.csv",
        mime="text/csv"
    )
else:
    st.info("Enter domains and keywords then click 'Check Rankings' to see results here.")