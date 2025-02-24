import time
import requests
from bs4 import BeautifulSoup

def get_hockey_matches():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    url = "https://www.fih.hockey/schedule-fixtures-results"
    response = requests.get(url, headers=headers)
    time.sleep(2)
    soup = BeautifulSoup(response.content, "html.parser")

    matches = []

    main_div = soup.find('div', {'class': 'live-tab-container' or 'upcoming-tab-container' or 'recent-tab-container', 'id': 'tab1' or 'tab2' or 'tab3'})
    if not main_div:
        return None
    
    cards = main_div.find_all('li', class_='live hand-cursor')
    
    for card in cards:
        match = {}

        match_title = card.find_previous('h4', class_='fixtures-title')
        match['title'] = match_title.text.strip() if match_title else ""

        match_status = card.find('div', class_='fixtures-status')
        match['status'] = match_status.text.strip() if match_status else ""

        match_time = card.find('p', class_='team-time-text')
        match['time'] = match_time.text.strip() if match_time else ""

        gender_category = card.find('div', class_='fixtures-gender--womens')
        match['category'] = "Women's" if gender_category else "Men's"   

        teams = []
        all_teams = card.find_all('div', class_='team')
        
        for team in all_teams:
            team_info = {}
            team_name_tag = team.find('p', class_='team-name')
            team_name = team_name_tag.text.strip() if team_name_tag else ""
            
            team_score_tag = team.find('p', class_='score')
            team_score = team_score_tag.text.strip() if team_score_tag else ""
            
            team_info['name'] = team_name
            team_info['score'] = team_score
            teams.append(team_info)
        
        match['teams'] = teams
        
        venue_details = card.find('div', class_='fixtures-venue')
        match['venue'] = venue_details.text.strip() if venue_details else ""

        no_data = card.find('div', class_='no-data')
        match['no-data'] = no_data.text.strip() if no_data else ""

        matches.append(match)
    
    return matches if matches else None
