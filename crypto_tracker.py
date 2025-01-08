"""
Cryptocurrency Live Data Tracker (Google Sheets Version)
-----------------------------------------------------
This script fetches real-time data for the top 50 cryptocurrencies using the CoinGecko API,
performs analysis, and updates a Google Sheet continuously.

Author: Shreyash Naik (modified for Google Sheets)
Date: January 8, 2025
"""

import requests
import pandas as pd
import time
from datetime import datetime
import os
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class CryptoTrackerGSheets:
    def __init__(self, credentials_path, spreadsheet_id):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.spreadsheet_id = spreadsheet_id
        self.service = self._initialize_sheets_service(credentials_path)
        
    def _initialize_sheets_service(self, credentials_path):
        """Initialize Google Sheets service with credentials"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            return build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            print(f"Error initializing Google Sheets service: {e}")
            return None

    def fetch_top_50_data(self):
        """Fetch top 50 cryptocurrencies data from CoinGecko API"""
        try:
            endpoint = f"{self.base_url}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 50,
                'page': 1,
                'sparkline': False
            }
            
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def process_crypto_data(self, data):
        """Process raw API data into a structured format"""
        if not data:
            return None
            
        processed_data = []
        for coin in data:
            processed_data.append([
                coin['name'],
                coin['symbol'].upper(),
                coin['current_price'],
                coin['market_cap'],
                coin['total_volume'],
                coin['price_change_percentage_24h'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ])
            
        return processed_data

    def analyze_data(self, data):
        """Perform analysis on cryptocurrency data"""
        if not data:
            return None
            
        df = pd.DataFrame(data, columns=[
            'Name', 'Symbol', 'Current Price (USD)', 'Market Cap', 
            '24h Volume', '24h Change %', 'Last Updated'
        ])
            
        analysis = [
            ["Market Analysis"],
            ["Top 5 by Market Cap:"],
        ]
        
        # Add top 5 by market cap
        top_5 = df.nlargest(5, 'Market Cap')
        for _, row in top_5.iterrows():
            analysis.append([f"{row['Name']}: ${row['Market Cap']:,.2f}"])
        
        analysis.extend([
            [""],
            [f"Total Market Cap: ${df['Market Cap'].sum():,.2f}"],
            [f"Average Price: ${df['Current Price (USD)'].mean():,.2f}"],
            [f"Average 24h Volume: ${df['24h Volume'].mean():,.2f}"],
            [f"Market Volatility Index: {df['24h Change %'].std():.2f}%"],
            [""],
            [f"Highest 24h Change: {df.nlargest(1, '24h Change %').iloc[0]['Name']} ({df.nlargest(1, '24h Change %').iloc[0]['24h Change %']:.2f}%)"],
            [f"Lowest 24h Change: {df.nsmallest(1, '24h Change %').iloc[0]['Name']} ({df.nsmallest(1, '24h Change %').iloc[0]['24h Change %']:.2f}%)"],
        ])
        
        return analysis

    def initialize_sheet(self):
        """Initialize Google Sheet with headers and formatting"""
        try:
            # Clear the sheet
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range='Sheet1'
            ).execute()

            # Set up headers
            headers = [
                ['Cryptocurrency Live Data Tracker'],
                [''],
                ['Name', 'Symbol', 'Current Price (USD)', 'Market Cap', 
                 '24h Volume', '24h Change %', 'Last Updated']
            ]

            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='A1',
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()

            # Apply formatting (bold headers)
            requests = [{
                'repeatCell': {
                    'range': {
                        'sheetId': 0,
                        'startRowIndex': 0,
                        'endRowIndex': 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': 7
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'textFormat': {'bold': True}
                        }
                    },
                    'fields': 'userEnteredFormat.textFormat.bold'
                }
            }]

            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={'requests': requests}
            ).execute()

            return True

        except HttpError as e:
            print(f"Error initializing Google Sheet: {e}")
            return False

    def update_sheet(self, data, analysis):
        """Update Google Sheet with latest data and analysis"""
        try:
            # Update main data
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='A4',
                valueInputOption='RAW',
                body={'values': data}
            ).execute()

            # Update analysis
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='I1',
                valueInputOption='RAW',
                body={'values': analysis}
            ).execute()

        except HttpError as e:
            print(f"Error updating Google Sheet: {e}")

    def run_tracker(self, update_interval=300):
        """Run the crypto tracker with specified update interval (in seconds)"""
        if not self.initialize_sheet():
            return

        print(f"Cryptocurrency tracker started. Data will be updated every {update_interval} seconds.")
        print("Press Ctrl+C to stop.")

        while True:
            try:
                # Fetch and process data
                raw_data = self.fetch_top_50_data()
                data = self.process_crypto_data(raw_data)
                analysis = self.analyze_data(data)

                # Update Google Sheet
                self.update_sheet(data, analysis)

                print(f"Data updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                time.sleep(update_interval)

            except KeyboardInterrupt:
                print("\nCryptocurrency tracker stopped.")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(10)  # Wait before retrying


    @staticmethod
    def verify_setup(credentials_path):
        """Verify that the credentials file exists and is accessible"""
        if not os.path.exists(credentials_path):
            print(f"ERROR: Credentials file not found at: {credentials_path}")
            print("Please ensure you have:")
            print("1. Downloaded the credentials JSON file from Google Cloud Console")
            print("2. Moved it to the correct location")
            print("3. Updated credentials_path to point to the correct file")
            return False
        return True       

if __name__ == "__main__":
    # Replace these with your actual values
    CREDENTIALS_PATH = "credentials.json"
    SPREADSHEET_ID = "1xVh43WdQ_1TiE5aBx4Ecx9MsXh_se9tPsKTF6HdTmqg"
    
    # Use the static method for verification
    if CryptoTrackerGSheets.verify_setup(CREDENTIALS_PATH):
        tracker = CryptoTrackerGSheets(CREDENTIALS_PATH, SPREADSHEET_ID)
        tracker.run_tracker()
    else:
        print("Setup verification failed. Please fix the issues above and try again.")
