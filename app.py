import streamlit as st
import os
import pandas as pd
import io
from datetime import datetime
from openpyxl import Workbook

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
                        country_code,
                        st.session_state.result_size  # Pass the result size to API
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
    
    # Create a combined table with domains and URLs
    combined_data = []
    
    for keyword in st.session_state.keywords:
        keyword_results = st.session_state.current_results.get(keyword, {})
        row = {'Keyword': keyword}
        
        # Add rank and URL for each domain
        for domain in st.session_state.domains:
            result = keyword_results.get(domain, None)
            
            # Add rank
            if result is None:
                row[f"{domain} Rank"] = "Not found"
                row[f"{domain} URL"] = ""
            else:
                # Unpack the tuple (rank, url)
                rank, url = result
                # Convert all ranks to string for consistency
                row[f"{domain} Rank"] = str(rank) if rank else "Not found"
                row[f"{domain} URL"] = url if url else ""
        
        combined_data.append(row)
    
    # Create the combined dataframe
    combined_df = pd.DataFrame(combined_data)
    
    # Display the combined table
    st.dataframe(combined_df, use_container_width=True, height=400)
    
    # Add export buttons (CSV and Excel)
    col1, col2 = st.columns(2)
    
    # CSV export
    with col1:
        csv = combined_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="seo_rankings.csv",
            mime="text/csv"
        )
    
    # Excel export
    with col2:
        # Create an Excel file in memory
        output = io.BytesIO()
        
        # Create a workbook and add data
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            combined_df.to_excel(writer, sheet_name='Rankings', index=False)
            
        # Set pointer to the beginning of the stream
        output.seek(0)
        
        # Download button for Excel
        st.download_button(
            label="Download as Excel",
            data=output,
            file_name="seo_rankings.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Enter domains and keywords then click 'Check Rankings' to see results here.")