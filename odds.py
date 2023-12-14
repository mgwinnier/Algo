import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
from datetime import datetime

def scrape_odds_to_excel(date, output_file):
    # Format the URL to include the date parameter
    url = f'https://www.vegasinsider.com/college-basketball/odds/las-vegas/?date={date}'
    
    # Send a GET request to the page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        
        # Initialize lists to hold the extracted team names and odds
        top_team_names = []
        bottom_team_names = []
        top_team_odds = []
        bottom_team_odds = []

        # Find all 'divided' and 'footer' rows
        divided_rows = soup.find_all('tr', class_='divided')
        footer_rows = soup.find_all('tr', class_='footer')

        # Extract top team names and odds
        for row in divided_rows:
            # Extract the team name from the 'divided' row
            team_name_element = row.select_one('.team-name')
            team_name = team_name_element.get_text(strip=True) if team_name_element else 'N/A'
            top_team_names.append(team_name)
            
            # Extract the odds from the 'divided' row (adjust the index as needed)
            odds_element = row.find_all('td', class_='game-odds')[2].find('span', class_='data-value')
            odds = odds_element.get_text(strip=True) if odds_element else 'N/A'
            top_team_odds.append(odds)

        # Extract bottom team names and odds
        for row in footer_rows:
            # Extract the team name from the 'footer' row
            team_name_element = row.select_one('.team-name')
            team_name = team_name_element.get_text(strip=True) if team_name_element else 'N/A'
            bottom_team_names.append(team_name)
            
            # Extract the odds from the 'footer' row (adjust the index as needed)
            odds_element = row.find_all('td', class_='game-odds')[2].find('span', class_='data-value')
            odds = odds_element.get_text(strip=True) if odds_element else 'N/A'
            bottom_team_odds.append(odds)

        # Combine the team names and odds into a single list, alternating between top and bottom teams
        combined_data = []
        for top_name, top_odds, bottom_name, bottom_odds in zip(top_team_names, top_team_odds, bottom_team_names, bottom_team_odds):
    # Process top team odds
            if top_odds.startswith('+'):
                top_odds = top_odds.replace('+', '')
            if not (top_odds == 'N/A' or top_odds.startswith('o') or top_odds.startswith('u')):
                combined_data.append((top_name, top_odds))

            # Process bottom team odds
            if bottom_odds.startswith('+'):
                bottom_odds = bottom_odds.replace('+', '')
            if not (bottom_odds == 'N/A' or bottom_odds.startswith('o') or bottom_odds.startswith('u')):
                combined_data.append((bottom_name, bottom_odds))

        # Create a DataFrame
        df = pd.DataFrame(combined_data, columns=['Team Name', 'Odds Value'])

        # Export to Excel
        df.to_excel(output_file, index=False)
        
        print(f'Team names and odds extracted and saved to {output_file}')
    else:
        print(f'Failed to retrieve the page with status code: {response.status_code}')

