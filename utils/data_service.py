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
            tuple or None: (rank position, url) or None if not found
        """
        # Check if this is an image search result
        if 'images' in search_results:
            return self.find_domain_in_image_results(search_results, domain, result_size)
        
        # Regular organic search
        if 'organic' not in search_results:
            return None
            
        organic_results = search_results.get('organic', [])
        
        for result in organic_results[:result_size]:
            link = result.get('link', '')
            if domain in link:
                return (result.get('position', 0), link)
        
        return None
    
    def find_domain_in_image_results(self, search_results, domain, result_size=10):
        """
        Find a domain in image search results
        
        Args:
            search_results (dict): The image search results from Serper API
            domain (str): The domain to find
            result_size (int): Maximum result size to check
            
        Returns:
            tuple or None: (rank position, url) or None if not found
        """
        if 'images' not in search_results:
            return None
            
        image_results = search_results.get('images', [])
        
        for result in image_results[:result_size]:
            # Both link and domain fields contain domain information in image results
            link = result.get('link', '')
            result_domain = result.get('domain', '')
            
            if domain in link or domain in result_domain:
                # Return position and link
                return (result.get('position', 0), link)
        
        return None
    
    def results_to_dataframe(self, results, domains, keywords):
        """
        Convert results dictionary to pandas DataFrame
        
        Args:
            results (dict): The results dictionary (keyword -> domain -> rank)
            domains (list): List of domains
            keywords (list): List of keywords
            
        Returns:
            pandas.DataFrame: DataFrame with rankings and URLs
        """
        data = []
        
        for keyword in keywords:
            keyword_results = results.get(keyword, {})
            row = {'Keyword': keyword}
            
            for domain in domains:
                result = keyword_results.get(domain, None)
                if result is None:
                    row[domain] = "Not found"
                    row[f"{domain}_url"] = ""
                else:
                    # Unpack the tuple (rank, url)
                    rank, url = result
                    row[domain] = rank
                    row[f"{domain}_url"] = url
            
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
                result = keyword_results.get(domain, None)
                
                # Calculate score: higher positions get higher scores
                if result is not None:
                    # Unpack the tuple (rank, url)
                    rank, _ = result
                    
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
            scores[domain] = float(scores[domain]) / keyword_count
            scores[domain] = round(scores[domain] * 100) / 100  # Round to 2 decimal places
            
        return scores
