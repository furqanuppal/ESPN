import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh
from cricket import get_cricket_cards
from hockey import get_hockey_matches
from tennis import get_tennis_cards

st.image("sports.png", width=300)
st.title("Sports Dashboard")
st.markdown("Select a sport to view live updates.")

sport = st.sidebar.radio("Select a Sport", ("Home", "Cricket", "Tennis", "Hockey"))

if sport == "Home":
    st.header("Welcome to the Sports Dashboard!")
    st.write("Click on a sport from the sidebar to view live match updates.")

elif sport == "Cricket":
    st.image("cricket.png", width=300)
    st.title("Today Matches - ESPN CRIC INFO")
    st.markdown("Live updates every five minutes.")
    
    match_data = get_cricket_cards()
    
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

elif sport == "Hockey":
    st.image("hockey.png", width=300)
    st.title("Today Matches - FIH HOCKEY")
    st.markdown("Live updates every two minutes.")

    match_data = get_hockey_matches()

    if match_data:
        count = st_autorefresh(interval=120000, key="autorefresh_key")
        time.sleep(2)
        
        cols = st.columns(3)
        
        for i, match in enumerate(match_data):
            col = cols[i % 3]
            with col:
                st.subheader(f"{match.get('title', '')}")
                
                if match.get('status') or match.get('time'):
                    st.write(f"{match.get('category', '')} - {match.get('status', '')} - {match.get('time', '')}")
                
                if match.get('teams'):
                    for team in match['teams']:
                        st.write(f"{team.get('name', '')} \t {team.get('score', '')}")
                
                if match.get('venue'):
                    st.caption(f"{match.get('venue', '')}")
                    
                st.markdown('---')
    else:
        st.caption("NO MATCH IN PROGRESS")

elif sport == "Tennis":
    st.image("tennis.png", width=300)
    st.title("Today Matches - TENNIS.COM")
    st.markdown("Live updates every two minutes.")

    match_data = get_tennis_cards()

    if match_data:
        count = st_autorefresh(interval=120000, key="autorefresh_key")
        time.sleep(2)
        
        cols = st.columns(3)
        
        for i, match in enumerate(match_data):
            col = cols[i % 3]
            with col:
                st.subheader(f"{match.get('tournament', '')} ({match.get('match_type', '')})")
                
                if match.get('status'):
                    st.write(f"**Status:** {match.get('status')} - {match.get('time')}")
                
                if 'teams' in match and isinstance(match['teams'], list):
                    for competitor in match['teams']:
                        st.write(f"**{competitor.get('name', '')}** - {competitor.get('score', '')}")

                if match.get('winner'):
                    st.success(f"🏆 Winner: {match.get('winner')}")

                st.markdown('---')
