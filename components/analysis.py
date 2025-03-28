import streamlit as st
import pandas as pd
import plotly.express as px

def render_gap_analysis(results, domains, keywords):
    """
    Render gap analysis between domains
    
    Args:
        results (dict): The results dictionary
        domains (list): List of domains
        keywords (list): List of keywords
    """
    if len(domains) < 2:
        st.warning("You need at least two domains to perform gap analysis.")
        return
    
    st.write("""
    Gap analysis helps you identify keywords where your competitors rank better than you.
    Select your primary domain to compare against competitors.
    """)
    
    # Select primary domain
    primary_domain = st.selectbox(
        "Select your primary domain", 
        options=domains,
        index=0
    )
    
    # Get other domains for comparison
    competitor_domains = [d for d in domains if d != primary_domain]
    
    # Create gap analysis data
    gap_data = []
    
    for keyword in keywords:
        keyword_results = results.get(keyword, {})
        primary_rank = keyword_results.get(primary_domain, None)
        
        row = {
            'Keyword': keyword,
            'Your Rank': primary_rank if primary_rank is not None else "Not ranked"
        }
        
        # Add competitor ranks
        best_competitor = None
        best_competitor_rank = None
        
        for competitor in competitor_domains:
            competitor_rank = keyword_results.get(competitor, None)
            row[competitor] = competitor_rank if competitor_rank is not None else "Not ranked"
            
            # Track best competitor for this keyword
            if competitor_rank is not None:
                if (best_competitor_rank is None) or (competitor_rank < best_competitor_rank):
                    best_competitor = competitor
                    best_competitor_rank = competitor_rank
        
        # Calculate rank difference
        if primary_rank is not None and best_competitor_rank is not None:
            row['Rank Difference'] = primary_rank - best_competitor_rank
            row['Best Competitor'] = best_competitor
        else:
            if primary_rank is None and best_competitor_rank is not None:
                row['Rank Difference'] = 999  # Arbitrary high number for sorting
                row['Best Competitor'] = best_competitor
            else:
                row['Rank Difference'] = 0
                row['Best Competitor'] = 'None'
        
        gap_data.append(row)
    
    # Create DataFrame
    gap_df = pd.DataFrame(gap_data)
    
    # Sort by rank difference (biggest gaps first)
    gap_df = gap_df.sort_values('Rank Difference', ascending=False)
    
    # Display opportunities (keywords where competitors rank better)
    st.subheader("Keyword Opportunities")
    
    opportunities = gap_df[gap_df['Rank Difference'] > 0].copy()
    
    if len(opportunities) > 0:
        # Function to highlight significant gaps
        def highlight_gaps(val):
            if isinstance(val, (int, float)) and val > 0:
                if val > 10:
                    return 'background-color: #f8d7da'  # Red for big gaps
                elif val > 5:
                    return 'background-color: #fff3cd'  # Yellow for medium gaps
                return 'background-color: #f0f0f0'  # Light gray for small gaps
            return ''
        
        # Display styled table
        st.dataframe(
            opportunities.style.applymap(highlight_gaps, subset=['Rank Difference']),
            use_container_width=True,
            height=300
        )
        
        # Create visualization of top opportunities
        st.subheader("Top Keyword Opportunities")
        
        # Filter to significant opportunities and limit to top 10
        top_opportunities = opportunities[opportunities['Rank Difference'] > 0].head(10)
        
        if not top_opportunities.empty:
            fig = px.bar(
                top_opportunities, 
                x='Keyword', 
                y='Rank Difference',
                color='Best Competitor',
                title='Top Keyword Opportunities (Larger Bar = Bigger Gap)',
                text='Rank Difference'
            )
            
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(xaxis_tickangle=-45)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.write("""
            The chart above shows keywords where your competitors rank better than you.
            Larger bars indicate a bigger gap in rankings.
            """)
    else:
        st.info("No keyword opportunities found. You are ranking better than competitors for all tracked keywords.")
    
    # Display strengths (keywords where primary domain ranks better)
    st.subheader("Your Keyword Strengths")
    
    strengths = gap_df[gap_df['Rank Difference'] <= 0].copy()
    
    if len(strengths) > 0:
        # Function to highlight strengths
        def highlight_strengths(val):
            if isinstance(val, (int, float)) and val <= 0:
                if val < -10:
                    return 'background-color: #d4edda'  # Green for big advantages
                elif val < -5:
                    return 'background-color: #e2f0d9'  # Light green for medium advantages
                return 'background-color: #f0f0f0'  # Light gray for small advantages
            return ''
        
        # Display styled table
        st.dataframe(
            strengths.style.applymap(highlight_strengths, subset=['Rank Difference']),
            use_container_width=True,
            height=300
        )
    else:
        st.info("No keyword strengths found compared to competitors.")
