import streamlit as st
import os
import pandas as pd
from datetime import datetime

from utils.api_service import SerperAPI
from utils.data_service import DataService
from components.forms import render_input_forms
from components.results import render_results
from components.analysis import render_gap_analysis

# Page configuration
st.set_page_config(
    page_title="SEO Rank Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    st.session_state.location = "United States"
if 'results_history' not in st.session_state:
    st.session_state.results_history = {}
if 'current_results' not in st.session_state:
    st.session_state.current_results = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("SERPER_API_KEY", "")

# Main app layout
st.title("SEO Rank Tracker")
st.markdown("""
Use this tool to track your domain rankings on Google search results.
Track multiple domains and keywords across different locations and search types.
""")

# Initialize services
data_service = DataService()
api_service = SerperAPI(st.session_state.api_key)

# Sidebar for inputs
with st.sidebar:
    st.header("Configuration")
    
    # API Key input
    api_key = st.text_input("Serper.dev API Key", 
                           value=st.session_state.api_key,
                           type="password",
                           help="Enter your Serper.dev API key")
    
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        api_service.set_api_key(api_key)
    
    # Render input forms (domains, keywords, options)
    render_input_forms()
    
    if st.button("Track Rankings", use_container_width=True):
        if not st.session_state.api_key:
            st.error("Please enter your Serper.dev API key")
        elif not st.session_state.domains:
            st.error("Please add at least one domain to track")
        elif not st.session_state.keywords:
            st.error("Please add at least one keyword to track")
        else:
            with st.spinner("Fetching ranking data..."):
                try:
                    results = {}
                    
                    # Determine language based on location
                    language = "tr" if st.session_state.location == "Turkey" else "en"
                    country_code = "tr" if st.session_state.location == "Turkey" else "us"
                    
                    # Get results for each keyword
                    for keyword in st.session_state.keywords:
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
                            rank = data_service.find_domain_rank(search_results, domain, st.session_state.result_size)
                            keyword_results[domain] = rank
                        
                        results[keyword] = keyword_results
                    
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
                    
                    st.success("Ranking data fetched successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error fetching data: {str(e)}")

# Main content
tab1, tab2, tab3 = st.tabs(["Current Results", "Historical Data", "Gap Analysis"])

with tab1:
    # Show current results
    if st.session_state.current_results:
        render_results(st.session_state.current_results, 
                      st.session_state.domains, 
                      st.session_state.keywords)
    else:
        st.info("Track your rankings using the sidebar form to see results here.")

with tab2:
    # Show historical data
    st.header("Historical Ranking Data")
    
    if not st.session_state.results_history:
        st.info("No historical data available yet. Start tracking to collect data.")
    else:
        # Select historical data to view
        timestamps = list(st.session_state.results_history.keys())
        selected_timestamp = st.selectbox("Select historical data", timestamps, index=len(timestamps)-1)
        
        historical_data = st.session_state.results_history[selected_timestamp]
        
        # Show the configuration used for this data
        st.subheader("Tracking Configuration")
        config_col1, config_col2 = st.columns(2)
        with config_col1:
            st.write(f"**Time:** {selected_timestamp}")
            st.write(f"**Search Type:** {historical_data['search_type']}")
            st.write(f"**Result Size:** Top {historical_data['result_size']}")
        with config_col2:
            st.write(f"**Location:** {historical_data['location']}")
            st.write(f"**Domains Tracked:** {', '.join(historical_data['domains'])}")
            st.write(f"**Keywords Tracked:** {', '.join(historical_data['keywords'])}")
        
        # Show historical results
        render_results(historical_data['results'], 
                      historical_data['domains'], 
                      historical_data['keywords'])
        
        # Option to export data
        if st.button("Export Historical Data as CSV"):
            export_df = data_service.results_to_dataframe(
                historical_data['results'], 
                historical_data['domains'], 
                historical_data['keywords']
            )
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"seo_rankings_{selected_timestamp.replace(':', '-').replace(' ', '_')}.csv",
                mime="text/csv",
            )

with tab3:
    # Gap analysis between domains
    st.header("Domain Gap Analysis")
    
    if not st.session_state.current_results:
        st.info("Track your rankings first to see gap analysis.")
    elif len(st.session_state.domains) < 2:
        st.warning("Add at least two domains to perform gap analysis.")
    else:
        render_gap_analysis(st.session_state.current_results, 
                           st.session_state.domains, 
                           st.session_state.keywords)

# Footer
st.markdown("---")
st.markdown("SEO Rank Tracker powered by Serper.dev API")
