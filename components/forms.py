import streamlit as st

def render_input_forms():
    """Render the simplified input forms for domains, keywords, and search options"""
    
    # Domains input (bulk)
    st.subheader("Domains")
    domains_input = st.text_area(
        "Enter domains (one per line)",
        placeholder="example.com\nanothersite.com",
        height=100
    )
    
    # Keywords input (bulk)
    st.subheader("Keywords")
    keywords_input = st.text_area(
        "Enter keywords (one per line)",
        placeholder="keyword1\nkeyword2\nkeyword3",
        height=100
    )
    
    # Only display simple search options
    col1, col2 = st.columns(2)
    
    with col1:
        # Search type
        st.session_state.search_type = st.selectbox(
            "Search Type",
            options=["search", "images"],
            index=0
        )
    
    with col2:
        # Location with better UI
        st.session_state.location = st.radio(
            "Location",
            options=["Turkey", "United States"],
            index=0,  # Default to Turkey
            horizontal=True
        )
    
    # Result size with better UI
    st.session_state.result_size = st.select_slider(
        "Result Size",
        options=[10, 20, 50, 100],
        value=st.session_state.result_size
    )
    
    # Track button with more prominence
    track_btn = st.button("Check Rankings", use_container_width=True, type="primary")
    
    # Process input values if track button was clicked
    if track_btn:
        # Process domains
        if domains_input:
            # Clear previous domains
            st.session_state.domains = []
            # Add new domains
            domain_list = [d.strip().replace("https://", "").replace("http://", "") 
                          for d in domains_input.split("\n") if d.strip()]
            st.session_state.domains = domain_list
        
        # Process keywords
        if keywords_input:
            # Clear previous keywords
            st.session_state.keywords = []
            # Add new keywords
            keyword_list = [k.strip() for k in keywords_input.split("\n") if k.strip()]
            st.session_state.keywords = keyword_list
    
    # Return track button status to use in app.py
    return track_btn
