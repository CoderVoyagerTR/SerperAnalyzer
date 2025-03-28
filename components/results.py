import streamlit as st
import pandas as pd
import plotly.express as px

def render_results(results, domains, keywords):
    """
    Render the ranking results with improved UI and visualizations
    
    Args:
        results (dict): The results dictionary
        domains (list): List of domains
        keywords (list): List of keywords
    """
    if not results:
        st.info("No results available.")
        return
    
    st.subheader("📊 Ranking Results")
    
    # Create summary metrics at the top
    st.markdown("### 📈 Performance Overview")
    
    # Calculate metrics for each domain
    domain_metrics = {}
    for domain in domains:
        domain_positions = []
        top_3_count = 0
        top_10_count = 0
        top_30_count = 0
        not_found_count = 0
        
        for keyword in keywords:
            rank = results.get(keyword, {}).get(domain, None)
            if rank is not None:
                domain_positions.append(rank)
                if rank <= 3:
                    top_3_count += 1
                if rank <= 10:
                    top_10_count += 1
                if rank <= 30:
                    top_30_count += 1
            else:
                not_found_count += 1
        
        avg_position = sum(domain_positions) / len(domain_positions) if domain_positions else None
        best_position = min(domain_positions) if domain_positions else None
        
        domain_metrics[domain] = {
            'avg_position': avg_position,
            'best_position': best_position,
            'top_3_count': top_3_count,
            'top_10_count': top_10_count,
            'top_30_count': top_30_count,
            'not_found_count': not_found_count,
            'keywords_ranked': len(domain_positions),
            'keywords_coverage_pct': (len(domain_positions) / len(keywords)) * 100 if keywords else 0
        }
    
    # Display summary metrics in columns
    metric_columns = st.columns(len(domains))
    for i, domain in enumerate(domains):
        metrics = domain_metrics[domain]
        with metric_columns[i]:
            st.markdown(f"### 🌐 {domain}")
            
            # Average position metric
            avg_pos = metrics['avg_position']
            if avg_pos is not None:
                if avg_pos <= 3:
                    position_icon = "🥇"  # Gold medal for top 3
                elif avg_pos <= 10:
                    position_icon = "🥈"  # Silver medal for top 10
                elif avg_pos <= 30:
                    position_icon = "🥉"  # Bronze medal for top 30
                else:
                    position_icon = "📊"  # Chart for others
                
                st.metric(
                    f"{position_icon} Average Position",
                    f"#{avg_pos:.1f}",
                    help=f"Average ranking position for {domain}"
                )
            else:
                st.metric(
                    "Average Position",
                    "N/A",
                    help=f"No rankings found for {domain}"
                )
            
            # Best position metric
            if metrics['best_position'] is not None:
                st.metric(
                    "🏆 Best Position",
                    f"#{metrics['best_position']}",
                    help=f"Best ranking position for {domain}"
                )
            
            # Top positions breakdown
            st.metric(
                "🔝 Top Positions",
                f"{metrics['top_3_count']} in Top 3 | {metrics['top_10_count']} in Top 10",
                help=f"Count of keywords where {domain} ranks in top positions"
            )
            
            # Coverage metric
            st.metric(
                "📏 Keyword Coverage",
                f"{metrics['keywords_coverage_pct']:.1f}%",
                help=f"Percentage of keywords where {domain} appears in search results"
            )
    
    # Create DataFrame from results for the ranking table
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
    
    # Create detailed rankings table
    st.markdown("### 📋 Detailed Rankings")
    
    # Apply styling to highlight rankings with improved colors
    def highlight_rankings(val):
        if isinstance(val, int):
            if val <= 3:
                return 'background-color: #c8e6c9; color: #1b5e20; font-weight: bold;'  # Green for top 3
            elif val <= 10:
                return 'background-color: #fff9c4; color: #f57f17;'  # Yellow for top 10
            elif val <= 30:
                return 'background-color: #ffccbc; color: #bf360c;'  # Orange for top 30
            return 'background-color: #ffcdd2; color: #b71c1c;'  # Red for others
        return ''
    
    # Display the styled table with filtering options
    st.caption("Green = Top 3, Yellow = Top 10, Orange = Top 30, Red = Lower positions")
    st.dataframe(
        df.style.map(highlight_rankings, subset=[col for col in df.columns if col != 'Keyword']),
        use_container_width=True,
        height=400
    )
    
    # Create visualizations
    st.markdown("### 📊 Ranking Visualizations")
    
    # Tabs for different visualizations
    viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Domain Comparison", "Ranking Distribution", "Keyword Performance"])
    
    with viz_tab1:
        # Domain comparison chart
        chart_data = []
        for domain in domains:
            metrics = domain_metrics[domain]
            if metrics['avg_position'] is not None:
                chart_data.append({
                    'Domain': domain,
                    'Average Position': metrics['avg_position'],
                    'Keywords Ranked': metrics['keywords_ranked'],
                    'Top 3 Keywords': metrics['top_3_count'],
                    'Top 10 Keywords': metrics['top_10_count']
                })
        
        if chart_data:
            chart_df = pd.DataFrame(chart_data)
            
            # Create bar chart with enhanced styling
            fig1 = px.bar(
                chart_df, 
                x='Domain', 
                y='Average Position',
                color='Keywords Ranked',
                color_continuous_scale='viridis',
                text='Average Position',
                title='Average Ranking Position by Domain (Lower is Better)',
                hover_data=['Top 3 Keywords', 'Top 10 Keywords']
            )
            
            # Invert y-axis so lower (better) positions appear higher
            fig1.update_layout(
                yaxis={'autorange': 'reversed', 'title': 'Average Position (Lower is Better)'},
                coloraxis_colorbar={'title': 'Keywords Ranked'},
                height=450
            )
            
            fig1.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            
            st.plotly_chart(fig1, use_container_width=True, key="domain_comparison_chart")
            
            st.markdown("""
            💡 **How to read this chart:**
            - Lower bars represent better average ranking positions
            - Bar color intensity indicates how many keywords are ranked
            - Hover over bars to see Top 3 and Top 10 keyword counts
            """)
        else:
            st.info("No ranking data available for domain comparison visualization.")
    
    with viz_tab2:
        # Ranking distribution chart
        if domains and keywords:
            # Prepare data for distribution chart
            all_ranks = []
            for domain in domains:
                domain_ranks = []
                for keyword in keywords:
                    rank = results.get(keyword, {}).get(domain, None)
                    if rank is not None:
                        domain_ranks.append({'Domain': domain, 'Rank': rank})
                all_ranks.extend(domain_ranks)
            
            if all_ranks:
                rank_df = pd.DataFrame(all_ranks)
                
                # Create histogram of rankings
                fig2 = px.histogram(
                    rank_df,
                    x='Rank',
                    color='Domain',
                    marginal='box',  # Add box plot on the margin
                    nbins=20,
                    title='Distribution of Ranking Positions',
                    labels={'Rank': 'Ranking Position (Lower is Better)'},
                    opacity=0.7
                )
                
                fig2.update_layout(
                    xaxis_title='Ranking Position',
                    yaxis_title='Count of Keywords',
                    height=450,
                    bargap=0.1
                )
                
                st.plotly_chart(fig2, use_container_width=True, key="ranking_distribution_chart")
                
                st.markdown("""
                💡 **Distribution Analysis:**
                - The histogram shows how rankings are distributed across positions
                - More bars on the left (lower positions) indicate better overall performance
                - The box plot shows the median and range of rankings for each domain
                """)
            else:
                st.info("No ranking data available for distribution visualization.")
        else:
            st.info("No domains or keywords available for distribution visualization.")
    
    with viz_tab3:
        # Keyword performance chart
        if domains and keywords:
            # Prepare data for keyword performance chart
            keyword_data = []
            for keyword in keywords:
                keyword_results = results.get(keyword, {})
                for domain in domains:
                    rank = keyword_results.get(domain, None)
                    if rank is not None:
                        keyword_data.append({
                            'Keyword': keyword,
                            'Domain': domain,
                            'Rank': rank
                        })
            
            if keyword_data:
                keyword_df = pd.DataFrame(keyword_data)
                
                # Create a grouped bar chart
                fig3 = px.bar(
                    keyword_df,
                    x='Keyword',
                    y='Rank',
                    color='Domain',
                    barmode='group',
                    title='Keyword Rankings by Domain',
                    labels={'Rank': 'Ranking Position (Lower is Better)'}
                )
                
                # Invert y-axis so lower (better) positions appear higher
                fig3.update_layout(
                    yaxis={'autorange': 'reversed', 'title': 'Ranking Position'},
                    xaxis={'title': 'Keywords', 'tickangle': -45},
                    legend={'title': 'Domains'},
                    height=450
                )
                
                st.plotly_chart(fig3, use_container_width=True, key="keyword_performance_chart")
                
                st.markdown("""
                💡 **Keyword Analysis:**
                - Each group represents a keyword with bars for each domain
                - Lower bars indicate better ranking positions
                - Missing bars mean the domain is not ranked for that keyword
                - This view helps identify which domain performs best for each specific keyword
                """)
            else:
                st.info("No ranking data available for keyword performance visualization.")
        else:
            st.info("No domains or keywords available for keyword performance visualization.")
    
    # Provide option to export the data
    st.markdown("### 📥 Export Results")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Rankings as CSV",
            data=csv,
            file_name="seo_rankings.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with export_col2:
        # Create a summary dataframe for export
        summary_export = pd.DataFrame([domain_metrics[d] for d in domains], index=domains)
        summary_csv = summary_export.to_csv()
        st.download_button(
            label="📥 Download Summary as CSV",
            data=summary_csv,
            file_name="seo_summary_metrics.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Add recommendations
    st.markdown("### 🔍 Insights & Recommendations")
    
    # Find domains with best and worst average position
    best_domain = None
    worst_domain = None
    best_avg = float('inf')
    worst_avg = 0
    
    for domain, metrics in domain_metrics.items():
        if metrics['avg_position'] is not None:
            if metrics['avg_position'] < best_avg:
                best_avg = metrics['avg_position']
                best_domain = domain
            if metrics['avg_position'] > worst_avg:
                worst_avg = metrics['avg_position']
                worst_domain = domain
    
    if best_domain and worst_domain:
        st.markdown(f"""
        Based on the ranking data, here are some insights:
        
        - 🏆 **Best performing domain:** {best_domain} with average position {best_avg:.1f}
        - 📉 **Domain needing improvement:** {worst_domain} with average position {worst_avg:.1f}
        
        **Recommendations:**
        - 🔍 Focus on optimizing keywords where you're just outside the top 10
        - 📱 Check mobile rankings in addition to desktop results
        - 🌎 Monitor ranking changes over time to identify trends
        - 🔄 Compare with competitors to identify content gaps
        """)
    
    # Add explanation about ranking factors
    with st.expander("ℹ️ About Ranking Factors"):
        st.markdown("""
        Google uses over 200 ranking factors to determine search results. Key factors include:
        
        - **Content Quality:** Comprehensive, original, and relevant to the search query
        - **Backlinks:** Quality and quantity of other sites linking to your pages
        - **User Experience:** Page load speed, mobile-friendliness, site security (HTTPS)
        - **On-Page SEO:** Title tags, meta descriptions, headers, and content structure
        - **Engagement Metrics:** Click-through rate, time on site, bounce rate
        
        Remember that rankings can vary based on location, device type, and user search history.
        """)
