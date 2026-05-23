# Cricket ETL Pipeline

A Python data pipeline that fetches live cricket match data, 
cleans it, and saves to CSV with proper logging.

## What it does
- Fetches live match data from CricAPI
- Cleans and flattens nested JSON
- Handles missing data gracefully  
- Saves to CSV with headers
- Logs all pipeline activity to error.txt

## Tech used
- Python 3
- requests
- csv
- logging
