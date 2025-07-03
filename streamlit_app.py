import streamlit as st
import requests

st.title("Rock Paper Scissors Lizard Spock - Best of 3")

API_URL = "http://127.0.0.1:8000/play"
choices = ["rock", "paper", "scissors", "lizard", "spock"]

# Session state for scores and round
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'computer_score' not in st.session_state:
    st.session_state.computer_score = 0
if 'round_num' not in st.session_state:
    st.session_state.round_num = 1
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

st.write(f"Round {st.session_state.round_num} (Best of 3)")

col1, col2, col3, col4, col5 = st.columns(5)
move = None
if not st.session_state.game_over:
    if col1.button("🪨 Rock"):
        move = "rock"
    elif col2.button("📄 Paper"):
        move = "paper"
    elif col3.button("✂️ Scissors"):
        move = "scissors"
    elif col4.button("🦎 Lizard"):
        move = "lizard"
    elif col5.button("🖖 Spock"):
        move = "spock"

if move and not st.session_state.game_over:
    with st.spinner("Playing..."):
        try:
            resp = requests.post(API_URL, json={"user_choice": move})
            if resp.status_code == 200:
                data = resp.json()
                st.session_state.last_result = data
                if data['result'] == "win":
                    st.session_state.user_score += 1
                elif data['result'] == "lose":
                    st.session_state.computer_score += 1
                st.session_state.round_num += 1
                # Check for best of 3
                if st.session_state.user_score == 2 or st.session_state.computer_score == 2:
                    st.session_state.game_over = True
            else:
                st.error(f"Error: {resp.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Could not connect to API: {e}")

# Show last round result
if st.session_state.last_result:
    data = st.session_state.last_result
    st.success(f"You chose: {data['user_choice']}")
    st.info(f"Computer chose: {data['computer_choice']}")
    if data['result'] == "win":
        st.success("You win this round!")
    elif data['result'] == "lose":
        st.error("Computer wins this round!")
    else:
        st.warning("It's a tie!")

st.write(f"Score: You {st.session_state.user_score} - Computer {st.session_state.computer_score}")

if st.session_state.game_over:
    if st.session_state.user_score > st.session_state.computer_score:
        st.balloons()
        st.success("Congratulations! You won best of three!")
    else:
        st.error("Computer wins best of three. Better luck next time!")

if st.button("Quit / Reset Game"):
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.round_num = 1
    st.session_state.game_over = False
    st.session_state.last_result = None
    st.experimental_rerun()

st.markdown("---")
st.caption("Make sure your FastAPI server is running at http://127.0.0.1:8000")