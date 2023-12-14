import requests
from bs4 import BeautifulSoup
import pandas as pd

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
        return output_file
    else:
        # Print the error and return None
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

# Example usage:
# Replace 'url_to_ncaa_scoreboard' with the actual URL you wish to scrape
# Replace 'path_to_output_excel_file' with the desired path for your Excel file
url_to_ncaa_scoreboard = 'https://www.ncaa.com/scoreboard/basketball-men/d1/2023/12/12'
path_to_output_excel_file = 'scores.xlsx'

# Call the function and print the result
result = scrape_ncaa_scores_to_excel(url_to_ncaa_scoreboard, path_to_output_excel_file)
if result:
    print(f'Saved Excel file at: {result}')
else:
    print('Failed to save Excel file.')
