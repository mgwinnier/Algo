import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse

def scrape_ncaa_scores_to_excel(url, output_file):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
    
    # Check the status code before proceeding
    if response.status_code == 200:
        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all game containers
        games = soup.find_all(class_='gamePod-type-game')
        
        # Lists to hold team names and scores
        team_names = []
        team_scores = []
        
        # Loop through each game and get the team names and scores
        for game in games:
            teams = game.find_all(class_='gamePod-game-team-name')
            scores = game.find_all(class_='gamePod-game-team-score')
            
            for team, score in zip(teams, scores):
                team_name = team.text.strip()
                team_name = team_name.replace('St.', 'State')
                team_name = team_name.replace('U.', 'University')
                team_name = team_name.replace('Ky.', 'Kentucky')
                team_name = team_name.replace('Fla.', 'Florida')
                team_name = team_name.replace('La.', 'Louisiana')
                team_name = team_name.replace('Ill.', 'Illinois')
                team_name = team_name.replace('N.M.', 'New Mexico')
                team_name = team_name.replace('N.C.', 'North Carolina')
                team_name = team_name.replace('Ark.', 'Arkansas')
                team_name = team_name.replace('UIW', 'Incarnate Word')
                team_name = team_name.replace('Ala.', 'Alabama')
                team_name = team_name.replace('So.', 'Southern')
                team_name = team_name.replace('FIU', 'Florida International')
                team_name = team_name.replace('LSU', 'Louisiana State')
                team_name = team_name.replace('BYU', 'Brigham Young')
                team_name = team_name.replace('UNLV', 'Nevada-Las Vegas')
                team_name = team_name.replace('Seattle U', 'Seattle')
                team_name = team_name.replace('Miss.', 'Mississippi')
                team_name = team_name.replace('McNeese', 'McNeese State')
                team_name = team_name.replace('App State', 'Appalachian State')
                team_name = team_name.replace('Queens (NC)', 'Queens')
                team_name = team_name.replace('VCU', 'Virginia Commonwealth')
                team_name = team_name.replace('Alcorn', 'Alcorn State')
                team_name = team_name.replace('Col.', 'College')
                team_name = team_name.replace('Miami (FL)', 'Miami')
                team_name = team_name.replace('Ole Miss', 'Mississippi')
                team_name = team_name.replace('UCF', 'Central Florida')
                team_name = team_name.replace('Saint Francis (PA)', 'Saint Francis')
                team_name = team_name.replace('ETSU', 'East Tennessee State')
                team_name = team_name.replace('SIUE', 'SIU Edwardsville')
                team_names.append(team_name)
                team_scores.append(score.text.strip())

        # Create a DataFrame
        scores_df = pd.DataFrame({
            'Team Name': team_names,
            'Team Score': team_scores
        })

        # Save DataFrame to an Excel file
        scores_df.to_excel(output_file, index=False)
        
        # Return the path to the saved Excel file
parser = argparse.ArgumentParser(description='Scrape NCAA Scores to Excel')
parser.add_argument('dates', nargs='+', help='Dates for the scores in YYYY/MM/DD format')
args = parser.parse_args()

base_url = 'https://www.ncaa.com/scoreboard/basketball-men/d1'

for date in args.dates:
    formatted_date = date.replace('/', '/')
    url = f'{base_url}/{formatted_date}/all-conf'

    # Create a unique output file name for each date
    output_file = f'results-{date.replace("/", "-")}.xlsx'

    # Call the function and print the result
    result = scrape_ncaa_scores_to_excel(url, output_file)
    if result:
        print(f'Saved Excel file at: {result}')
    else:
        print(f'Failed to save Excel file for {date}.')