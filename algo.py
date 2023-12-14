import os
import pandas as pd
from datetime import datetime
from odds import scrape_odds_to_excel
import argparse

def parse_data_from_file(file_path, date):
    # Create a directory with the date as its name
    directory_name = f'./{date}'
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    # The file paths now include the directory
    odds_filename = os.path.join(directory_name, f"odds-{date}.xlsx")
    scrape_odds_to_excel(date, odds_filename)

    with open(file_path, 'r') as file:
        data = file.read()

    match_data = data.split('##############################')
    results = []
    for match in match_data:
        if not match.strip():
            continue

        lines = match.strip().split('\n')
        if len(lines) < 10:
            print("Unexpected format in segment:\n", match)
            continue

        try:
            team1 = lines[0].split('(')[0].strip()
            team2 = lines[2].split('(')[0].strip()
            efg_statement = lines[4]
            efg_start = efg_statement.find(': ') + 2
            efg_end = efg_statement.find(' by')
            efg_team = efg_statement[efg_start:efg_end].strip()

            # Parsing team scores and SRS ratings
            team1_score = float(lines[8].split(':')[1].strip())
            team2_score = float(lines[10].split(':')[1].strip())
            team1_srs = float(lines[14].split(':')[1].strip())
            team2_srs = float(lines[16].split(':')[1].strip())

            # Calculate normal and SRS spreads for each team
            normal_spread_team1 = team1_score - team2_score
            normal_spread_team2 = team2_score - team1_score
            srs_spread_team1 = team1_srs - team2_srs
            srs_spread_team2 = team2_srs - team1_srs

            matchup = f'{team1} vs {team2}'

            # Append separate entries for each team
            results.append({
                'Matchup': matchup,
                'Home/Away' : "Away",
                'Team': team1,
                'eFG Statement': efg_team,
                'Team Spread': normal_spread_team1,
                'Team SRS Spread': srs_spread_team1,
            })

            results.append({
                'Matchup': matchup,
                'Home/Away' : "Home",
                'Team': team2,
                'eFG Statement': efg_team,
                'Team Spread': normal_spread_team2,
                'Team SRS Spread': srs_spread_team2,
            })
            
        except Exception as e:
            print("Error processing segment:\n", match)
            print("Error details:", e)

    df = pd.DataFrame(results)

    # Add VLOOKUP formula to the new DataFrame
    for index, row in df.iterrows():
        excel_row = index + 2  # Excel rows start at 1 and headers take 1 row
        if row['Home/Away'] == "Away":
            df.at[index, 'Vegas Spread'] = f'=IFERROR(VLOOKUP(C{excel_row},\'[odds-{date}.xlsx]Sheet1\'!$A:$B,2,FALSE), G{excel_row+1}*-1)'
        else:
            df.at[index, 'Vegas Spread'] = f'=IFERROR(VLOOKUP(C{excel_row},\'[odds-{date}.xlsx]Sheet1\'!$A:$B,2,FALSE), G{excel_row-1}*-1)'

    processed_filename = os.path.join(directory_name, f"processed_data-{date}.xlsx")

    if not df.empty:
        # Save to Excel within the new directory
        with pd.ExcelWriter(processed_filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
            print(f"Excel file '{processed_filename}' created successfully.")
    else:
        print("No data to save to Excel.")

    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse data and scrape odds')
    parser.add_argument('date', type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(), help='Date for the odds in YYYY-MM-DD format')
    args = parser.parse_args()

    parse_data_from_file("data.txt", args.date.strftime('%Y-%m-%d'))