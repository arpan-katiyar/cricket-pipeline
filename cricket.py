import requests
import logging
import csv
import json
from datetime import datetime

logging.basicConfig(filename="error.txt",level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("ELT pipeline started")

API_KEY = "96eb8b16-c231-4bca-b820-93e5919e0c7e"
URL = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"

def fetch_matches():
    try:
        logging.info("trying api calling...")
        response = requests.get(URL)
        data = response.json()
        logging.info("api called successfully...")
        # print(data["data"])
        return data["data"]
    except Exception as e:
        logging.exception("api calling failed")
        return []

def clean_match(match):
    cleaned = {
        "name": match["name"],
        "status": match["status"],
        "venue": match["venue"],
        "date": match["date"],
        "team1":match["teams"][0],
        "team2":match["teams"][1],
        "team1_score": None,
        "team2_score": None
    }
    if "score" in match:
        scores = match.get("score", [])
        first = scores[0] if len(scores) > 0 else None
        second = scores[1] if len(scores) > 1 else None
        if first:
            cleaned["team1_score"]= f"{first.get('inning')}: {first.get('r')}/{first.get('w')} in {first.get('o')} overs"
        if second:
            cleaned["team2_score"]= f"{second.get('inning')}: {second.get('r')}/{second.get('w')} in {second.get('o')} overs"
        
        
    print(cleaned)       
    return cleaned

def save_to_file(matches, filename="matches.csv"):
    if len(matches) == 0:
        logging.warning("no matches found for save")
        return
    with open(filename, "w") as f:
        fieldnames= matches[0].keys()
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(matches)

    logging.info(f"Saved {len(matches)} matches to {filename}")


# Main pipeline
matches_raw = fetch_matches()
matches_clean = [clean_match(m) for m in matches_raw]
save_to_file(matches_clean)
