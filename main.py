# Write a rock, paper, scissors game
# import random and difflib modules
import random
import difflib

# define main function that handles all the logic

def main():
    choices = ["rock", "paper", "scissors", "lizard", "spock"]
    # Rules for who beats whom
    win_map = {
        "rock":     ["scissors", "lizard"],
        "paper":    ["rock", "spock"],
        "scissors": ["paper", "lizard"],
        "lizard":   ["spock", "paper"],
        "spock":    ["scissors", "rock"]
    }
    user_score = 0
    computer_score = 0
    round_num = 1
    while user_score < 2 and computer_score < 2:
        print(f"\nRound {round_num} (Best of 3)")
        # Display numbered options
        print("Choose your option (or type 'quit' to exit early):")
        for idx, option in enumerate(choices, 1):
            print(f"  {idx}. {option}")
        print("  q. quit")
        while True:
            user_input = input("Enter the number of your choice: ").strip()
            if user_input.lower() in ('q', 'quit'):
                print("You chose to quit early. Thanks for playing!")
                return
            if user_input.isdigit():
                num = int(user_input)
                if 1 <= num <= len(choices):
                    user_choice = choices[num - 1]
                    break
            # fallback to text input with spelling correction
            user_choice = user_input.lower()
            if user_choice in choices:
                break
            close_matches = difflib.get_close_matches(user_choice, choices, n=1, cutoff=0.6)
            if close_matches:
                corrected = close_matches[0]
                print(f"Did you mean '{corrected}'?")
                confirm = input("Type 'y' to accept, or 'n' to try again: ").lower()
                if confirm == 'y':
                    user_choice = corrected
                    break
            print("Invalid choice. Please try again.")
        computer_choice = random.choice(choices)
        print(f"You chose: {user_choice}")
        print(f"Computer chose: {computer_choice}")
        if user_choice == computer_choice:
            print("It's a tie!")
        elif computer_choice in win_map[user_choice]:
            print("You win this round!")
            user_score += 1
        else:
            print("Computer wins this round!")
            computer_score += 1
        print(f"Score: You {user_score} - Computer {computer_score}")
        round_num += 1
    if user_score > computer_score:
        print("\nCongratulations! You won best of three!")
    else:
        print("\nComputer wins best of three. Better luck next time!")

# call main function
if __name__ == "__main__":
    main()


