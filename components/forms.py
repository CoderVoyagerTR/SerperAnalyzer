import streamlit as st

def render_input_forms():
    """Render the input forms for domains, keywords, and search options"""
    
    # Domain input
    st.subheader("💻 Domains to Track")
    
    # Add new domain with improved UX
    new_domain = st.text_input(
        "Add Domain", 
        placeholder="E.g., example.com (without https://)",
        help="Enter the domain without protocol (http/https)"
    )
    
    # Domain example and add button in single row
    st.caption("Example: google.com, example.com")
    
    # Add domain button
    if st.button("➕ Add Domain", key="add_domain_btn", use_container_width=True):
        if new_domain:
            # Basic validation - ensure no http/https and clean the domain
            new_domain = new_domain.strip().replace("https://", "").replace("http://", "")
            if new_domain and new_domain not in st.session_state.domains:
                st.session_state.domains.append(new_domain)
                st.rerun()
            elif new_domain in st.session_state.domains:
                st.warning("This domain is already in your list.")
    
    # List current domains with better styling
    if st.session_state.domains:
        st.write("**Current Domains:**")
        for i, domain in enumerate(st.session_state.domains):
            st.markdown(f"🔹 {domain} [{i+1}]")
            if st.button("🗑️ Remove", key=f"remove_domain_{i}", help="Remove this domain"):
                st.session_state.domains.pop(i)
                st.rerun()
    
    st.markdown("---")
    
    # Keywords input
    st.subheader("🔍 Keywords to Track")
    
    # Add new keyword with improved UX
    new_keyword = st.text_input(
        "Add Keyword", 
        placeholder="E.g., seo tools",
        help="Enter a keyword to track"
    )
    
    # Keyword example
    st.caption("Example: seo tools, digital marketing")
    
    # Add keyword button
    if st.button("➕ Add Keyword", key="add_keyword_btn", use_container_width=True):
        if new_keyword:
            new_keyword = new_keyword.strip()
            if new_keyword and new_keyword not in st.session_state.keywords:
                st.session_state.keywords.append(new_keyword)
                st.rerun()
            elif new_keyword in st.session_state.keywords:
                st.warning("This keyword is already in your list.")
    
    # List current keywords with better styling
    if st.session_state.keywords:
        st.write("**Current Keywords:**")
        for i, keyword in enumerate(st.session_state.keywords):
            st.markdown(f"🔹 {keyword} [{i+1}]")
            if st.button("🗑️ Remove", key=f"remove_keyword_{i}", help="Remove this keyword"):
                st.session_state.keywords.pop(i)
                st.rerun()
    
    st.markdown("---")
    
    # Bulk add keywords with better styling
    st.subheader("📋 Bulk Add Keywords")
    bulk_keywords = st.text_area(
        "Enter multiple keywords (one per line)",
        placeholder="keyword1\nkeyword2\nkeyword3",
        height=100
    )
    
    if st.button("Add All Keywords", use_container_width=True):
        if bulk_keywords:
            new_keywords = [k.strip() for k in bulk_keywords.split("\n") if k.strip()]
            added_count = 0
            for keyword in new_keywords:
                if keyword and keyword not in st.session_state.keywords:
                    st.session_state.keywords.append(keyword)
                    added_count += 1
            if added_count > 0:
                st.success(f"Added {added_count} new keywords")
                st.rerun()
            else:
                st.info("No new keywords to add")
    
    st.markdown("---")
    
    # Search options with improved layout
    st.subheader("⚙️ Search Options")
    
    # Search type
    st.session_state.search_type = st.selectbox(
        "Search Type",
        options=["search", "images", "news"],
        index=0,
        help="Type of search to perform"
    )
    
    # Location with better UI
    st.session_state.location = st.radio(
        "Location",
        options=["Turkey", "United States"],
        index=1 if st.session_state.location == "United States" else 0,
        help="Search location affects results and language",
        horizontal=True
    )
    
    # Result size with better UI
    st.session_state.result_size = st.select_slider(
        "Result Size",
        options=[10, 20, 50, 100],
        value=st.session_state.result_size,
        help="Maximum number of results to check"
    )
    
    # Language info based on location
    language = "🇹🇷 Turkish" if st.session_state.location == "Turkey" else "🇺🇸 English"
    st.info(f"Language: {language}")
    
    # Track button with more prominence
    st.markdown("---")
    track_btn = st.button("🚀 Track Rankings", use_container_width=True, type="primary")
    
    # Return track button status to use in app.py
    return track_btn
