import time
import requests
from bs4 import BeautifulSoup
import streamlit as st
from streamlit_autorefresh import st_autorefresh

def get_match_cards():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    url = "https://www.espncricinfo.com/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    matches = []
    
    cards = soup.find_all('div', {'class' : 'slick-slide' or 'slick-slide slick-active'}, {'style' : 'outline:none'})  
    if cards:
        for card in cards:
            match = {}
            match_status = card.find('span', class_='ds-text-tight-xs ds-font-bold ds-uppercase ds-leading-5')
            match['status'] = match_status.text.strip() if match_status else ""

            details = card.find('span', class_='ds-text-tight-xs ds-text-typo-mid2')
            match['details'] = details.text.strip() if details else ""

            teams = []
            all_teams = card.find_all('div', class_=('ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo', 'ci-team-score ds-flex ds-justify-between ds-items-center ds-text-typo ds-opacity-50'))
            for team in all_teams:
                team_name = team.find('p', class_=('ds-text-tight-s ds-font-bold ds-capitalize ds-truncate', 'ds-text-tight-s ds-font-bold ds-capitalize ds-truncate !ds-text-typo-mid3'))
                team_name = team_name.text.strip() if team_name else ""
                
                team_score_tag = team.find('div', class_='ds-text-compact-s ds-text-typo ds-text-right ds-whitespace-nowrap')
                team_score = team_score_tag.text.strip() if team_score_tag else ""
                
                teams.append({'name': team_name, 'score': team_score})
            
            match['teams'] = teams
            
            today_details = card.find('div', class_='ds-text-tight-xs ds-text-right')
            match['other_details'] = today_details.text if today_details else ""

            result_details = card.find('div', class_='ds-h-3')
            match['result'] = result_details.text.strip() if result_details else ""

            matches.append(match)

    return matches if matches else None

st.image("logo.png")
st.title('Today Matches - ESPN CRIC INFO')
st.markdown('Live updates every five minutes.')

match_data = get_match_cards()

if match_data:
    count = st_autorefresh(interval=300000, key="autorefresh_key")
    time.sleep(2)
    
    cols = st.columns(3)
    
    for i, match in enumerate(match_data):
        col = cols[i % 3]
        with col:
            if match.get('status') or match.get('details'):
                st.subheader(f"{match.get('status', '')} {match.get('details', '')}")
            
            if match.get('teams'):
                for team in match['teams']:
                    st.write(f"{team.get('name', '')} \t {team.get('score', '')}")
            
            if match.get('result'):
                st.caption(match['result'])
                if match.get('other_details'):
                    st.write(f"**{match['other_details']}**")
                    st.markdown('---')
                else:
                    st.markdown('---')
