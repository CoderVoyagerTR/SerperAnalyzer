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
from components.results import render_results
from components.analysis import render_gap_analysis

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
    st.session_state.location = "United States"
if 'results_history' not in st.session_state:
    st.session_state.results_history = {}
if 'current_results' not in st.session_state:
    st.session_state.current_results = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = "46b91285ab5322e2dac2105c22d31aa73d886220"

# Header with icon
st.markdown('<div class="main-header">📊 SEO Rank Tracker</div>', unsafe_allow_html=True)
st.markdown("""
<div class="sub-header">
Track your domain rankings on Google search results across different locations and search types. 
Compare with competitors and identify keyword opportunities.
</div>
""", unsafe_allow_html=True)

# Initialize services
data_service = DataService()
api_service = SerperAPI(st.session_state.api_key)

# Two-column layout
main_col1, main_col2 = st.columns([2, 3])

with main_col1:
    st.subheader("📝 Tracking Configuration")
    
    # Status for API key
    st.markdown("**API Status**")
    if st.session_state.api_key:
        st.success("API Key is configured")
    else:
        st.error("API Key is not configured")
    
    # Render improved input forms
    track_button_clicked = render_input_forms()
    
    # Process tracking if button is clicked
    if track_button_clicked:
        if not st.session_state.domains:
            st.error("Please add at least one domain to track")
        elif not st.session_state.keywords:
            st.error("Please add at least one keyword to track")
        else:
            with st.spinner("🔍 Fetching ranking data..."):
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
                        progress_text = f"Processing keyword: {keyword} ({i+1}/{total_items})"
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
                            rank = data_service.find_domain_rank(search_results, domain, st.session_state.result_size)
                            keyword_results[domain] = rank
                        
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
                    
                    st.success("✅ Ranking data fetched successfully!")
                    st.balloons()
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error fetching data: {str(e)}")

with main_col2:
    # Results tabs with better styling
    tab1, tab2, tab3 = st.tabs(["📊 Current Results", "📅 Historical Data", "🔄 Gap Analysis"])
    
    with tab1:
        # Show current results
        if st.session_state.current_results:
            render_results(st.session_state.current_results, 
                          st.session_state.domains, 
                          st.session_state.keywords)
        else:
            st.info("👈 Configure your tracking parameters and click 'Track Rankings' to see results here.")
            
            # Example image
            st.markdown("### Example Results View")
            st.image("https://i.imgur.com/JZT8UR5.png", caption="Example ranking results visualization")
    
    with tab2:
        # Show historical data with improved layout
        st.header("📅 Historical Ranking Data")
        
        if not st.session_state.results_history:
            st.info("No historical data available yet. Start tracking to collect data.")
            st.markdown("""
            ### Why Track Historical Data?
            
            - 📈 Monitor ranking improvements over time
            - 🔍 Identify trends and patterns
            - 📊 Measure SEO campaign effectiveness
            - 📋 Create reports for clients or stakeholders
            """)
        else:
            # Select historical data to view with better UI
            timestamps = list(st.session_state.results_history.keys())
            selected_timestamp = st.selectbox(
                "Select historical data point", 
                timestamps, 
                index=len(timestamps)-1,
                format_func=lambda x: f"📅 {x}"
            )
            
            historical_data = st.session_state.results_history[selected_timestamp]
            
            # Show the configuration used for this data with better styling
            st.subheader("📝 Tracking Configuration")
            
            # Use columns for better layout
            config_col1, config_col2, config_col3 = st.columns(3)
            with config_col1:
                st.markdown(f"**🕒 Time:** {selected_timestamp}")
                st.markdown(f"**🔍 Search Type:** {historical_data['search_type']}")
            with config_col2:
                st.markdown(f"**📊 Result Size:** Top {historical_data['result_size']}")
                st.markdown(f"**🌎 Location:** {historical_data['location']}")
            with config_col3:
                # Download button in the third column
                export_df = data_service.results_to_dataframe(
                    historical_data['results'], 
                    historical_data['domains'], 
                    historical_data['keywords']
                )
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"seo_rankings_{selected_timestamp.replace(':', '-').replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            # Show tracked items
            st.markdown("**🔍 Tracked Items:**")
            st.markdown(f"**Domains:** {', '.join(historical_data['domains'])}")
            st.markdown(f"**Keywords:** {', '.join(historical_data['keywords'])}")
            
            # Show historical results
            render_results(historical_data['results'], 
                          historical_data['domains'], 
                          historical_data['keywords'])
    
    with tab3:
        # Gap analysis between domains with better styling
        st.header("🔄 Domain Gap Analysis")
        
        if not st.session_state.current_results:
            st.info("Track your rankings first to see gap analysis.")
            st.markdown("""
            ### What is Gap Analysis?
            
            Gap analysis helps you identify keywords where:
            
            - 🔴 Competitors rank better than you
            - 🟢 You rank better than competitors
            - ⚪ Opportunities exist to improve rankings
            
            Add at least two domains to unlock this powerful feature!
            """)
        elif len(st.session_state.domains) < 2:
            st.warning("⚠️ Add at least two domains to perform gap analysis.")
            st.markdown("Gap analysis requires comparing at least two domains to identify ranking differences and opportunities.")
        else:
            render_gap_analysis(st.session_state.current_results, 
                               st.session_state.domains, 
                               st.session_state.keywords)

# Footer with improved styling
st.markdown("""
<div class="footer">
    <p>📊 SEO Rank Tracker | Powered by Serper.dev API</p>
    <p>Version 1.0 | © 2025</p>
</div>
""", unsafe_allow_html=True)