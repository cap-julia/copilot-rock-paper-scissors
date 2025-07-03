import builtins
import pytest
import main
from unittest.mock import patch

def run_game_with_inputs(inputs):
    """Helper to run main.main() with a list of inputs, returns printed output as a string."""
    output = []
    def fake_print(*args, **kwargs):
        output.append(' '.join(str(a) for a in args))
    with patch('builtins.input', side_effect=inputs), patch('builtins.print', side_effect=fake_print):
        main.main()
    return '\n'.join(output)

def test_user_wins(monkeypatch):
    # User always picks rock, computer always picks scissors
    inputs = ['1', '1']  # win 2 rounds
    with patch('random.choice', side_effect=['scissors', 'scissors']):
        out = run_game_with_inputs(inputs)
    assert "Congratulations! You won best of three!" in out

def test_computer_wins(monkeypatch):
    # User always picks rock, computer always picks paper
    inputs = ['1', '1']  # lose 2 rounds
    with patch('random.choice', side_effect=['paper', 'paper']):
        out = run_game_with_inputs(inputs)
    assert "Computer wins best of three" in out

def test_tie_and_win(monkeypatch):
    # First round tie, then user wins 2
    inputs = ['1', '1', '1']
    with patch('random.choice', side_effect=['rock', 'scissors', 'scissors']):
        out = run_game_with_inputs(inputs)
    assert out.count("It's a tie!") == 1
    assert "Congratulations! You won best of three!" in out

def test_text_input(monkeypatch):
    # User types 'rock' instead of number
    inputs = ['rock', 'rock']
    with patch('random.choice', side_effect=['scissors', 'scissors']):
        out = run_game_with_inputs(inputs)
    assert "You chose: rock" in out
    assert "Congratulations! You won best of three!" in out

def test_spelling_correction_yes(monkeypatch):
    # User types 'roc', gets spelling correction, accepts
    inputs = ['roc', 'y', 'rock', 'rock']
    with patch('random.choice', side_effect=['scissors', 'scissors']):
        out = run_game_with_inputs(inputs)
    assert "Did you mean 'rock'?" in out
    assert "You chose: rock" in out

def test_spelling_correction_no(monkeypatch):
    # User types 'roc', gets spelling correction, rejects, then types valid
    inputs = ['roc', 'n', 'rock', 'rock']
    with patch('random.choice', side_effect=['scissors', 'scissors']):
        out = run_game_with_inputs(inputs)
    assert "Did you mean 'rock'?" in out
    assert out.count("Invalid choice. Please try again.") >= 1

def test_invalid_choice(monkeypatch):
    # User types invalid, then valid
    inputs = ['banana', 'rock', 'rock']
    with patch('random.choice', side_effect=['scissors', 'scissors']):
        out = run_game_with_inputs(inputs)
    assert out.count("Invalid choice. Please try again.") >= 1

def test_case_insensitive(monkeypatch):
    # User types 'ROCK' in uppercase
    inputs = ['ROCK', 'ROCK']
    with patch('random.choice', side_effect=['scissors', 'scissors']):
        out = run_game_with_inputs(inputs)
    assert "You chose: rock" in out

def test_lizard_spock(monkeypatch):
    # User picks lizard, computer picks spock (user wins)
    inputs = ['4', '4']
    with patch('random.choice', side_effect=['spock', 'spock']):
        out = run_game_with_inputs(inputs)
    assert "You chose: lizard" in out
    assert "Computer chose: spock" in out
    assert "You win this round!" in out
