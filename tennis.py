import requests
from datetime import datetime

API_KEY = "663ac1f53dd92f10e22dc9b30324cba9f9135ccf64bbc7caa548420e6690d3f4"

# Automatically get today's date
today_date = datetime.today().strftime("%Y-%m-%d")

url = "https://api.api-tennis.com/tennis/"
params = {
    "method": "get_fixtures",
    "APIkey": API_KEY,
    "date_start": today_date,
    "date_stop": today_date
}

def get_tennis_cards():
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        matches_list = []

        if data.get("success") == 1:
            matches = data["result"]
            for match in matches:
                set_scores = []
                if "scores" in match and isinstance(match["scores"], list):
                    for set_data in match["scores"]:
                        set_scores.append(f"{set_data.get('score_first', 'N/A')} - {set_data.get('score_second', 'N/A')} (Set {set_data.get('score_set', 'N/A')})")
                
                match_info = {
                    "tournament": match.get("tournament_name", "N/A"),
                    "match_type": match.get("event_type_type", "N/A"),
                    "status": match.get("event_status", "N/A"),
                    "time": f"{match.get('event_date', 'N/A')} {match.get('event_time', '')}",
                    "winner": match.get("event_winner", "N/A"),
                    "teams": [
                        {"name": match.get("event_first_player", "N/A"), "score": match.get("event_final_result", "N/A")},
                        {"name": match.get("event_second_player", "N/A"), "score": match.get("event_final_result", "N/A")}
                    ]
                }
                matches_list.append(match_info)
        
        return matches_list

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {str(e)}")
        print(f"Response content: {response.text}")
    except KeyError as e:
        print(f"Data parsing error: Missing key {e}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

    return []