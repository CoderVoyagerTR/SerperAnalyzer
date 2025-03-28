import pandas as pd
import streamlit as st

class DataService:
    """Service for data processing and manipulation"""
    
    def find_domain_rank(self, search_results, domain, result_size=10):
        """
        Find the rank of a domain in search results
        
        Args:
            search_results (dict): The search results from Serper API
            domain (str): The domain to find
            result_size (int): Maximum result size to check
            
        Returns:
            int or None: The rank position or None if not found
        """
        if 'organic' not in search_results:
            return None
            
        organic_results = search_results.get('organic', [])
        
        for result in organic_results[:result_size]:
            link = result.get('link', '')
            if domain in link:
                return result.get('position', 0)
        
        return None
    
    def results_to_dataframe(self, results, domains, keywords):
        """
        Convert results dictionary to pandas DataFrame
        
        Args:
            results (dict): The results dictionary (keyword -> domain -> rank)
            domains (list): List of domains
            keywords (list): List of keywords
            
        Returns:
            pandas.DataFrame: DataFrame with rankings
        """
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
        
        return pd.DataFrame(data)
    
    def calculate_domain_scores(self, results, domains, keywords):
        """
        Calculate aggregate domain scores based on rankings
        
        Args:
            results (dict): The results dictionary
            domains (list): List of domains
            keywords (list): List of keywords
            
        Returns:
            dict: Dictionary with domain scores
        """
        scores = {domain: 0 for domain in domains}
        keyword_count = len(keywords)
        
        for keyword in keywords:
            keyword_results = results.get(keyword, {})
            
            for domain in domains:
                rank = keyword_results.get(domain, None)
                
                # Calculate score: higher positions get higher scores
                if rank is not None:
                    if rank == 1:
                        scores[domain] += 10
                    elif rank <= 3:
                        scores[domain] += 8
                    elif rank <= 5:
                        scores[domain] += 5
                    elif rank <= 10:
                        scores[domain] += 3
                    else:
                        scores[domain] += 1
        
        # Calculate average score per keyword
        for domain in domains:
            scores[domain] = round(scores[domain] / keyword_count, 2)
            
        return scores
