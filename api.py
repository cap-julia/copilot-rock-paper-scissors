# FastAPI REST API for Rock, Paper, Scissors, Lizard, Spock
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import difflib

app = FastAPI(title="Rock Paper Scissors Lizard Spock API")

choices = ["rock", "paper", "scissors", "lizard", "spock"]
win_map = {
    "rock":     ["scissors", "lizard"],
    "paper":    ["rock", "spock"],
    "scissors": ["paper", "lizard"],
    "lizard":   ["spock", "paper"],
    "spock":    ["scissors", "rock"]
}

class PlayRequest(BaseModel):
    user_choice: str

def correct_choice(user_choice: str):
    user_choice = user_choice.lower()
    if user_choice in choices:
        return user_choice
    close_matches = difflib.get_close_matches(user_choice, choices, n=1, cutoff=0.6)
    if close_matches:
        return close_matches[0]
    return None

def get_result(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "tie"
    elif computer_choice in win_map[user_choice]:
        return "win"
    else:
        return "lose"

@app.post("/play")
def play_game(req: PlayRequest):
    user_choice = correct_choice(req.user_choice)
    if not user_choice:
        raise HTTPException(status_code=400, detail="Invalid choice. Valid options: rock, paper, scissors, lizard, spock.")
    computer_choice = random.choice(choices)
    result = get_result(user_choice, computer_choice)
    return {
        "user_choice": user_choice,
        "computer_choice": computer_choice,
        "result": result
    }

# For convenience, allow POST to /{move} (e.g., /rock, /spock)
from fastapi import Path
@app.post("/{move}")
def play_move(move: str = Path(..., description="Your move: rock, paper, scissors, lizard, or spock")):
    user_choice = correct_choice(move)
    if not user_choice:
        raise HTTPException(status_code=400, detail="Invalid choice. Valid options: rock, paper, scissors, lizard, spock.")
    computer_choice = random.choice(choices)
    result = get_result(user_choice, computer_choice)
    return {
        "user_choice": user_choice,
        "computer_choice": computer_choice,
        "result": result
    }
