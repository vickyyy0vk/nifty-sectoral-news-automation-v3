#!/usr/bin/env python3
"""
NSE Data Fetcher Script
Automated script to fetch Nifty sectoral data from NSE
"""

import requests
import json
import pandas as pd
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_nse_data():
    """
    Fetch NSE sectoral indices data
    """
    try:
        # NSE API endpoint for indices data
        url = "https://www.nseindia.com/api/allIndices"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Successfully fetched NSE data at {datetime.now()}")
        
        return data
        
    except Exception as e:
        logger.error(f"Error fetching NSE data: {e}")
        return None

def process_sectoral_data(data):
    """
    Process and filter sectoral indices data
    """
    if not data:
        return None
        
    try:
        # Filter for sectoral indices
        sectoral_indices = []
        for index in data.get('data', []):
            index_name = index.get('index', '')
            if 'NIFTY' in index_name and any(sector in index_name for sector in 
                ['BANK', 'IT', 'PHARMA', 'AUTO', 'METAL', 'ENERGY', 'FMCG', 'REALTY']):
                sectoral_indices.append({
                    'index': index_name,
                    'last': index.get('last', 0),
                    'change': index.get('change', 0),
                    'pChange': index.get('pChange', 0),
                    'timestamp': datetime.now().isoformat()
                })
        
        return sectoral_indices
        
    except Exception as e:
        logger.error(f"Error processing sectoral data: {e}")
        return None

def save_data_to_json(data, filename='nse_sectoral_data.json'):
    """
    Save processed data to JSON file
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Data saved to {filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return False

def main():
    """
    Main function to orchestrate NSE data fetching
    """
    logger.info("Starting NSE data fetch process...")
    
    # Fetch raw NSE data
    raw_data = fetch_nse_data()
    
    if raw_data:
        # Process sectoral data
        sectoral_data = process_sectoral_data(raw_data)
        
        if sectoral_data:
            # Save to file
            save_data_to_json(sectoral_data)
            logger.info(f"Successfully processed {len(sectoral_data)} sectoral indices")
        else:
            logger.error("Failed to process sectoral data")
    else:
        logger.error("Failed to fetch NSE data")

if __name__ == "__main__":
    main()
