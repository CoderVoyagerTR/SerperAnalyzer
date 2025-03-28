import streamlit as st

def render_input_forms():
    """Render the input forms for domains, keywords, and search options"""
    
    # Domain input
    st.subheader("Domains to Track")
    
    # List current domains
    if st.session_state.domains:
        for i, domain in enumerate(st.session_state.domains):
            cols = st.columns([4, 1])
            cols[0].text(domain)
            if cols[1].button("Remove", key=f"remove_domain_{i}"):
                st.session_state.domains.pop(i)
                st.rerun()
    
    # Add new domain
    new_domain = st.text_input(
        "Add Domain", 
        placeholder="E.g., example.com (without https://)",
        help="Enter the domain without protocol (http/https)"
    )
    
    if st.button("Add Domain"):
        if new_domain:
            # Basic validation - ensure no http/https and clean the domain
            new_domain = new_domain.strip().replace("https://", "").replace("http://", "")
            if new_domain and new_domain not in st.session_state.domains:
                st.session_state.domains.append(new_domain)
                st.rerun()
            elif new_domain in st.session_state.domains:
                st.warning("This domain is already in your list.")
    
    st.markdown("---")
    
    # Keywords input
    st.subheader("Keywords to Track")
    
    # List current keywords
    if st.session_state.keywords:
        for i, keyword in enumerate(st.session_state.keywords):
            cols = st.columns([4, 1])
            cols[0].text(keyword)
            if cols[1].button("Remove", key=f"remove_keyword_{i}"):
                st.session_state.keywords.pop(i)
                st.rerun()
    
    # Add new keyword
    new_keyword = st.text_input(
        "Add Keyword", 
        placeholder="E.g., seo tools",
        help="Enter a keyword to track"
    )
    
    if st.button("Add Keyword"):
        if new_keyword:
            new_keyword = new_keyword.strip()
            if new_keyword and new_keyword not in st.session_state.keywords:
                st.session_state.keywords.append(new_keyword)
                st.rerun()
            elif new_keyword in st.session_state.keywords:
                st.warning("This keyword is already in your list.")
    
    # Bulk add keywords
    with st.expander("Bulk Add Keywords"):
        bulk_keywords = st.text_area(
            "Enter multiple keywords (one per line)",
            placeholder="seo tools\ndigital marketing\n..."
        )
        
        if st.button("Add All Keywords"):
            if bulk_keywords:
                new_keywords = [k.strip() for k in bulk_keywords.split("\n") if k.strip()]
                for keyword in new_keywords:
                    if keyword and keyword not in st.session_state.keywords:
                        st.session_state.keywords.append(keyword)
                st.rerun()
    
    st.markdown("---")
    
    # Search options
    st.subheader("Search Options")
    
    # Search type
    st.session_state.search_type = st.selectbox(
        "Search Type",
        options=["search", "images", "news"],
        index=0,
        help="Type of search to perform"
    )
    
    # Result size
    st.session_state.result_size = st.select_slider(
        "Result Size",
        options=[10, 20, 50, 100],
        value=st.session_state.result_size,
        help="Maximum number of results to check"
    )
    
    # Location
    st.session_state.location = st.radio(
        "Location",
        options=["Turkey", "United States"],
        index=1 if st.session_state.location == "United States" else 0,
        help="Search location affects results and language"
    )
