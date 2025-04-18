import requests
import streamlit as st
import json
import os

class SerperAPI:
    """Service for interacting with the Serper.dev API"""
    
    def __init__(self, api_key=None):
        # Try to get API key from Streamlit secrets, then fallback to parameter
        try:
            self.api_key = api_key or st.secrets["api_keys"]["serper"]
        except:
            # Fallback to environment variable if secrets not available
            self.api_key = api_key or os.getenv("SERPER_API_KEY")
        self.base_url = "https://google.serper.dev"
    
    def set_api_key(self, api_key):
        """Update the API key"""
        self.api_key = api_key
    
    def get_search_results(self, query, search_type="search", location="United States", language="en", country_code="us", result_size=10):
        """
        Get search results from Serper.dev API
        
        Args:
            query (str): The search query
            search_type (str): Type of search (search, images, news, etc.)
            location (str): Location for search results
            language (str): Language code (en, tr, etc.)
            country_code (str): Country code (us, tr, etc.)
            result_size (int): Number of results to return (10, 20, 50 or 100)
            
        Returns:
            dict: The search results
        """
        if not self.api_key:
            raise ValueError("API key is required")
        
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Use different endpoint and payload structure for image search
        if search_type == "images":
            return self.get_image_search_results(query, location, language, country_code, result_size)
        
        payload = {
            "q": query,
            "gl": country_code,
            "hl": language,
            "type": search_type,
            "location": location,
            "num": result_size  # Add the number of results to return
        }
        
        endpoint = f"{self.base_url}/search"
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            if hasattr(e, 'response') and e.response:
                try:
                    error_details = e.response.json()
                    st.error(f"Error details: {json.dumps(error_details, indent=2)}")
                except:
                    st.error(f"Status code: {e.response.status_code}")
                    st.error(f"Response text: {e.response.text}")
            raise e
    
    def get_image_search_results(self, query, location="United States", language="en", country_code="us", result_size=10):
        """
        Get image search results from Serper.dev API
        
        Args:
            query (str): The search query
            location (str): Location for search results
            language (str): Language code (en, tr, etc.)
            country_code (str): Country code (us, tr, etc.)
            result_size (int): Number of results to return (10, 20, 50 or 100)
            
        Returns:
            dict: The image search results
        """
        if not self.api_key:
            raise ValueError("API key is required")
        
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": query,
            "gl": country_code,
            "hl": language,
            "location": location,
            "num": result_size
        }
        
        # Images need a specific endpoint
        endpoint = f"{self.base_url}/images"
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            if hasattr(e, 'response') and e.response:
                try:
                    error_details = e.response.json()
                    st.error(f"Error details: {json.dumps(error_details, indent=2)}")
                except:
                    st.error(f"Status code: {e.response.status_code}")
                    st.error(f"Response text: {e.response.text}")
            raise e
