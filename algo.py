from odds import scrape_odds_to_excel
import pandas as pd

def parse_data_from_file(file_path):

    scrape_odds_to_excel('https://www.vegasinsider.com/college-basketball/odds/las-vegas/', 'Odds.xlsx')

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
    
    # Add revised VLOOKUP formula to the new DataFrame
    for index, row in df.iterrows():
        excel_row = index + 2  # Excel rows start at 1 and headers take 1 row
        if row['Home/Away'] == "Away":
            df.at[index, 'Vegas Spread'] = f'=IFERROR(VLOOKUP(C{excel_row},[odds.xlsx]Sheet1!$A:$B,2,FALSE), G{excel_row+1}*-1)'
        else:
            df.at[index, 'Vegas Spread'] = f'=IFERROR(VLOOKUP(C{excel_row},[odds.xlsx]Sheet1!$A:$B,2,FALSE), G{excel_row-1}*-1)'

    if not df.empty:
        # Save to Excel with the formula
        with pd.ExcelWriter('processed_data.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
            print("Excel file created successfully.")
    else:
        print("No data to save to Excel.")

    return df

# Assuming the 'data.txt' is in the same directory as this script
parse_data_from_file("data.txt")