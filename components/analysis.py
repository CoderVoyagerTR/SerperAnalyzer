import streamlit as st
import pandas as pd
import plotly.express as px

def render_gap_analysis(results, domains, keywords):
    """
    Render gap analysis between domains with improved UI
    
    Args:
        results (dict): The results dictionary
        domains (list): List of domains
        keywords (list): List of keywords
    """
    if len(domains) < 2:
        st.warning("⚠️ You need at least two domains to perform gap analysis.")
        return
    
    st.markdown("""
    ### 🔄 Competitive Gap Analysis
    
    Gap analysis identifies keywords where:
    - 🔴 Your competitors rank better than you (opportunities)
    - 🟢 You rank better than competitors (strengths)
    
    Select your primary domain to compare against competitors.
    """)
    
    # Select primary domain with improved UI
    primary_domain = st.selectbox(
        "Select your primary domain", 
        options=domains,
        index=0,
        format_func=lambda x: f"🏠 {x} (Primary)"
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
                row['Rank Difference'] = 100  # More reasonable number for not ranked
                row['Best Competitor'] = best_competitor
            else:
                row['Rank Difference'] = 0
                row['Best Competitor'] = 'None'
        
        gap_data.append(row)
    
    # Create DataFrame
    gap_df = pd.DataFrame(gap_data)
    
    # Sort by rank difference (biggest gaps first)
    gap_df = gap_df.sort_values('Rank Difference', ascending=False)
    
    # Create summary metrics
    summary_col1, summary_col2 = st.columns(2)
    
    with summary_col1:
        # Opportunities summary
        opportunity_count = len(gap_df[gap_df['Rank Difference'] > 0])
        st.metric(
            "🔴 Keyword Opportunities", 
            f"{opportunity_count}",
            help=f"Number of keywords where competitors rank better than {primary_domain}"
        )
        
        # Average gap
        avg_gap = gap_df[gap_df['Rank Difference'] > 0]['Rank Difference'].mean()
        if not pd.isna(avg_gap):
            st.metric(
                "📏 Average Rank Gap", 
                f"{avg_gap:.1f} positions",
                help="Average difference in ranking positions for opportunities"
            )
    
    with summary_col2:
        # Strengths summary
        strength_count = len(gap_df[gap_df['Rank Difference'] <= 0])
        st.metric(
            "🟢 Keyword Strengths", 
            f"{strength_count}",
            help=f"Number of keywords where {primary_domain} ranks better than competitors"
        )
        
        # Top competitor
        if competitor_domains:
            top_competitor_counts = gap_df[gap_df['Best Competitor'] != 'None']['Best Competitor'].value_counts()
            if not top_competitor_counts.empty:
                top_competitor = top_competitor_counts.index[0]
                top_competitor_win_count = top_competitor_counts.iloc[0]
                
                st.metric(
                    "🥇 Top Competitor", 
                    f"{top_competitor}",
                    help=f"Competitor that ranks better than you for {top_competitor_win_count} keywords"
                )
    
    # Display opportunities (keywords where competitors rank better)
    st.markdown("### 🎯 Keyword Opportunities")
    st.markdown("These keywords represent optimization opportunities where competitors rank better than you.")
    
    opportunities = gap_df[gap_df['Rank Difference'] > 0].copy()
    
    if len(opportunities) > 0:
        # Function to highlight significant gaps with improved colors
        def highlight_gaps(val):
            if isinstance(val, (int, float)) and val > 0:
                if val > 20:
                    return 'background-color: #ffcdd2; color: #b71c1c; font-weight: bold;'  # Dark red for huge gaps
                elif val > 10:
                    return 'background-color: #f8d7da; color: #c62828;'  # Red for big gaps
                elif val > 5:
                    return 'background-color: #fff3cd; color: #f57f17;'  # Yellow for medium gaps
                return 'background-color: #f0f0f0; color: #424242;'  # Light gray for small gaps
            return ''
        
        # Display styled table with better formatting
        st.dataframe(
            opportunities.style.map(highlight_gaps, subset=['Rank Difference']),
            use_container_width=True,
            height=300
        )
        
        # Create visualization of top opportunities with improved design
        st.markdown("### 📊 Top Keyword Opportunities")
        
        # Filter to significant opportunities and limit to top 10
        top_opportunities = opportunities[opportunities['Rank Difference'] > 0].head(10)
        
        if not top_opportunities.empty:
            # Use two columns for different visualizations
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # Bar chart with better styling
                fig1 = px.bar(
                    top_opportunities, 
                    x='Keyword', 
                    y='Rank Difference',
                    color='Best Competitor',
                    title='Top Keyword Gaps',
                    text='Rank Difference',
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                
                fig1.update_traces(texttemplate='%{text}', textposition='outside')
                fig1.update_layout(
                    xaxis_tickangle=-45,
                    xaxis_title="Keywords",
                    yaxis_title="Rank Difference (Higher = Bigger Gap)",
                    legend_title="Competitors",
                    height=400
                )
                
                st.plotly_chart(fig1, use_container_width=True, key="opportunity_bar_chart")
            
            with chart_col2:
                # Create a scatter plot showing your rank vs competitor rank
                scatter_data = top_opportunities.copy()
                scatter_data['Competitor Rank'] = scatter_data.apply(
                    lambda row: row['Your Rank'] - row['Rank Difference'] 
                    if isinstance(row['Your Rank'], (int, float)) else 0, 
                    axis=1
                )
                
                fig2 = px.scatter(
                    scatter_data,
                    x='Your Rank',
                    y='Competitor Rank',
                    color='Best Competitor',
                    size='Rank Difference',
                    hover_name='Keyword',
                    title='Your Rank vs Competitor Rank',
                    labels={'Your Rank': 'Your Position', 'Competitor Rank': 'Competitor Position'},
                    height=400,
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                
                # Add reference line (y=x)
                fig2.add_shape(
                    type='line',
                    line=dict(dash='dash', color='gray'),
                    y0=0, x0=0,
                    y1=100, x1=100
                )
                
                # Invert axes so that lower (better) ranks are at the top-left
                fig2.update_layout(
                    xaxis=dict(autorange='reversed', title='Your Position (Lower is Better)'),
                    yaxis=dict(autorange='reversed', title='Competitor Position (Lower is Better)')
                )
                
                st.plotly_chart(fig2, use_container_width=True, key="opportunity_scatter_chart")
            
            st.markdown("""
            💡 **How to read these charts:**
            - In the bar chart, taller bars represent bigger ranking gaps where competitors outperform you
            - In the scatter plot, points below the diagonal line show keywords where competitors rank better than you
            - The size of each bubble represents the magnitude of the ranking gap
            """)
    else:
        st.success("🎉 No keyword opportunities found. You are ranking better than competitors for all tracked keywords.")
    
    # Display strengths (keywords where primary domain ranks better)
    st.markdown("### 💪 Your Keyword Strengths")
    st.markdown("These keywords represent areas where you outperform your competitors.")
    
    strengths = gap_df[gap_df['Rank Difference'] <= 0].copy()
    
    if len(strengths) > 0:
        # Function to highlight strengths with improved colors
        def highlight_strengths(val):
            if isinstance(val, (int, float)) and val <= 0:
                if val < -20:
                    return 'background-color: #c8e6c9; color: #1b5e20; font-weight: bold;'  # Dark green for huge advantages
                elif val < -10:
                    return 'background-color: #d4edda; color: #2e7d32;'  # Green for big advantages
                elif val < -5:
                    return 'background-color: #e2f0d9; color: #388e3c;'  # Light green for medium advantages
                return 'background-color: #f0f0f0; color: #424242;'  # Light gray for small advantages
            return ''
        
        # Display styled table with better formatting
        st.dataframe(
            strengths.style.map(highlight_strengths, subset=['Rank Difference']),
            use_container_width=True,
            height=300
        )
        
        # Create a visualization of top strengths
        top_strengths = strengths.sort_values('Rank Difference', ascending=True).head(10)
        
        if not top_strengths.empty:
            fig3 = px.bar(
                top_strengths,
                x='Keyword',
                y='Rank Difference',
                color='Best Competitor',
                title='Your Top Ranking Advantages',
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            fig3.update_layout(
                xaxis_tickangle=-45,
                yaxis_title="Rank Advantage (More Negative = Bigger Advantage)",
                height=400
            )
            
            st.plotly_chart(fig3, use_container_width=True, key="strength_bar_chart")
            
            st.markdown("""
            💡 **Competitive Advantage Analysis:**
            - Negative values show how many positions better you rank compared to competitors
            - These are keywords you should maintain and leverage in your content strategy
            - Consider creating more content related to these strength keywords
            """)
    else:
        st.info("No keyword strengths found compared to competitors. Focus on improving rankings for opportunity keywords.")
