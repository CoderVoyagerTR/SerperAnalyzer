import requests
import streamlit as st
import json

class SerperAPI:
    """Service for interacting with the Serper.dev API"""
    
    def __init__(self, api_key=""):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev"
    
    def set_api_key(self, api_key):
        """Update the API key"""
        self.api_key = api_key
    
    def get_search_results(self, query, search_type="search", location="United States", language="en", country_code="us"):
        """
        Get search results from Serper.dev API
        
        Args:
            query (str): The search query
            search_type (str): Type of search (search, images, news, etc.)
            location (str): Location for search results
            language (str): Language code (en, tr, etc.)
            country_code (str): Country code (us, tr, etc.)
            
        Returns:
            dict: The search results
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
            "type": search_type,
            "location": location
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
