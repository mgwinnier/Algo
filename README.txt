This is a tool to strip data from an Algorithim and export it into excel.
Steps:
1) Make sure you pip install pandas, BeautifulSoup, openpyxl, argparse
2) Input Algo data into data.txt starting with first ###########
    If conch adds info like "this spread seems weird" you will need to delete that info, the command window will tell you if you missed deleting something
3) Run algo.py with python run algo.py date in format YYYY/MM/DD
4) This will create a folder with the date run and save 3 excel files: processed data, odds
5) Open all three spreadsheets and check for any "N/A" data, odds should come in 95% of the time correct, though
6) To get results you can run old.py date in format YYYY/MM/DD, this will add a scores excel file with all the scores
    If you reopen processed data, it should have a new column in scores, keep in mind you need to no change the data.txt from the day before to do this.
    Sometimes there will be N/A, this means the team name is slightly off, if this is the case you will need to find the team name in teh scores spreadsheet and manually copy the score over. Usually 1/2 of the teams will be fine so if you search the team with the score populated the the team will be one row above or below.
7) Duplicate an existing sheet in google sheets, copy the processed data excel file (without scores) to new sheet and make sure all formulas are there if not drag them down from row above.
8) Google sheet will do the rest of teh work just make sure you delete the scores from the previous day.