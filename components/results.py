import streamlit as st
import pandas as pd
import plotly.express as px

def render_results(results, domains, keywords):
    """
    Render the ranking results
    
    Args:
        results (dict): The results dictionary
        domains (list): List of domains
        keywords (list): List of keywords
    """
    if not results:
        st.info("No results available.")
        return
    
    st.subheader("Ranking Results")
    
    # Create DataFrame from results
    data = []
    for keyword in keywords:
        keyword_results = results.get(keyword, {})
        row = {'Keyword': keyword}
        
        for domain in domains:
            rank = keyword_results.get(domain, None)
            if rank is None:
                row[domain] = "Not found"
            else:
                row[domain] = rank
        
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # Apply styling to highlight rankings
    def highlight_rankings(val):
        if isinstance(val, int):
            if val <= 3:
                return 'background-color: #a8f0a8'  # Light green for top 3
            elif val <= 10:
                return 'background-color: #f5f5a8'  # Light yellow for top 10
            return 'background-color: #f0f0f0'  # Light gray for others
        return ''
    
    # Display the styled table
    st.dataframe(
        df.style.applymap(highlight_rankings, subset=[col for col in df.columns if col != 'Keyword']),
        use_container_width=True,
        height=400
    )
    
    # Summary statistics
    st.subheader("Summary")
    
    # Calculate average rankings for each domain
    summary_data = []
    for domain in domains:
        domain_positions = []
        top_10_count = 0
        not_found_count = 0
        
        for keyword in keywords:
            rank = results.get(keyword, {}).get(domain, None)
            if rank is not None:
                domain_positions.append(rank)
                if rank <= 10:
                    top_10_count += 1
            else:
                not_found_count += 1
        
        avg_position = sum(domain_positions) / len(domain_positions) if domain_positions else None
        
        summary_data.append({
            'Domain': domain,
            'Average Position': round(avg_position, 1) if avg_position else 'N/A',
            'Keywords in Top 10': top_10_count,
            'Keywords Not Ranked': not_found_count,
            'Total Keywords': len(keywords)
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)
    
    # Visualize domain performance with a bar chart
    st.subheader("Domain Performance")
    
    # Create chart data for domains with average positions
    chart_data = []
    for domain in domains:
        domain_positions = []
        for keyword in keywords:
            rank = results.get(keyword, {}).get(domain, None)
            if rank is not None:
                domain_positions.append(rank)
        
        if domain_positions:
            chart_data.append({
                'Domain': domain,
                'Average Position': sum(domain_positions) / len(domain_positions),
                'Keywords Ranked': len(domain_positions)
            })
    
    if chart_data:
        chart_df = pd.DataFrame(chart_data)
        
        # Create the chart if we have data
        if not chart_df.empty and 'Average Position' in chart_df.columns:
            # Invert the y-axis so lower positions (better rankings) appear higher
            fig = px.bar(
                chart_df, 
                x='Domain', 
                y='Average Position',
                color='Keywords Ranked',
                color_continuous_scale='Viridis',
                text='Average Position',
                title='Average Ranking Position by Domain (Lower is Better)'
            )
            
            fig.update_layout(yaxis={'autorange': 'reversed'})
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No ranking data available for visualization.")
