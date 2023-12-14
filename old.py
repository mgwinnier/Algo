# main_script.py

import os
import argparse
import pandas as pd
from datetime import datetime
from odds import scrape_odds_to_excel  # Assuming this is in scrape_odds.py
from results import scrape_ncaa_scores_to_excel  # Assuming this is in scrape_ncaa_scores.py
from algo import parse_data_from_file  # Assuming this is in algo.py

def run_scraping_tasks(date):
    # Create a directory for the date
    directory_name = f'./{date.replace("/", "-")}'
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    # File paths for the odds, NCAA scores, and processed results
    odds_filename = os.path.join(directory_name, f"odds-{date.replace('/', '-')}.xlsx")
    scores_filename = os.path.join(directory_name, f"results-{date.replace('/', '-')}.xlsx")
    processed_results_filename = os.path.join(directory_name, f"processed_data-{date.replace('/', '-')}.xlsx")

    # Scrape odds and save to Excel
    scrape_odds_to_excel(date, odds_filename)

    # Scrape NCAA scores and save to Excel
    ncaa_url = f'https://www.ncaa.com/scoreboard/basketball-men/d1/{date.replace("/", "/")}/all-conf'
    scrape_ncaa_scores_to_excel(ncaa_url, scores_filename)

    # Process data and save to Excel
    df = parse_data_from_file('data.txt', date)

    for i in range(len(df)):
        row_num = i + 2  # Excel rows start at 1 and header row is the first row
        df.at[i, 'Actual Score'] = f'=VLOOKUP(C{row_num},\'[results-{date.replace("/", "-")}.xlsx]Sheet1\'!$A:$B,2,FALSE)'


    if not df.empty:
        with pd.ExcelWriter(processed_results_filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
            print(f"Excel file '{processed_results_filename}' created successfully.")
    else:
        print("No data to save to Excel.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run NCAA Data Scraping Tasks')
    parser.add_argument('date', type=lambda s: datetime.strptime(s, '%Y/%m/%d').date(), help='Date for the tasks in YYYY/MM/DD format')
    args = parser.parse_args()

    run_scraping_tasks(args.date.strftime('%Y-%m-%d'))
