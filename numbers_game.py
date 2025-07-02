import random
import json

def generate_numbers(min_value, max_value):
    """Generate one random number between min_value and max_value"""
    return random.randint(min_value, max_value)

def get_guess(min_value, max_value):
    """Get a guess from the user or return 'hint' if requested"""
    while True:
        guess = input(f"\nEnter your guess ({min_value}-{max_value}): ").strip().lower()

        # Check if the user wants a hint
        if guess == "hint":
            return "hint"

        try:
            guess = int(guess)
            if min_value <= guess <= max_value:
                return guess
            else:
                print(f"\nPlease enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("\nInvalid input. Please enter a valid number or 'hint'.")


def check_guess(guess, number):
    """Check the user's guess to see if they won or not"""
    if guess == number:
        print("\nCongratulations! You've guessed the number!")
    elif guess < number:
        print("\nToo low! Try again.")
    else:
        print("\nToo high! Try again.")

def choose_difficulty():
    choice = input("\nChoose your difficulty level: ").lower()
    if choice == "easy":
        return "easy", 1, 50
    elif choice == "medium":
        return "medium", 1, 100
    elif choice == "hard":
        return "hard", 1, 500
    elif choice == "insane":
        return "insane", 1, 1000
    else:
        print("\nInvalid choice. Defaulting to medium difficulty.")
        return "medium", 1, 100

def show_rules():
    print("\nWelcome to the Number Guessing Game!")
    print("\nHere are the rules:")
    print("\n1. Choose your difficulty level. You can choose from easy, medium, hard, or insane.")
    print("2. Try to guess the number I'm thinking of.")
    print("3. You have 10 attempts.")
    print("4. If you want a hint, type 'hint' to see the range of the number. If you use your hint, you will lose one attempt.")
    print("5. You can enter your name to save your score to the leaderboard when you've finished playing.")
    print ("\nLet's start!")

def play_game():
    """Main game loop"""
    show_rules()
    difficulty, min_val, max_val = choose_difficulty()
    number = generate_numbers(min_val, max_val)
    attempts = 0
    max_attempts = 10
    print(f"\nI'm thinking of a number between {min_val} and {max_val}.")

    while True:
        guess = get_guess(min_val, max_val)
        
        if guess == "hint":

            hint_low = max(min_val, number - 10)
            hint_high = min(max_val, number + 10)
            print(f"\nHere's your hint, use it well: The number is between {hint_low} and {hint_high}")
            attempts += 1

            print(f"\nHint used! You now have {10 - attempts} attempts left.")

            if attempts >= max_attempts:
                print("\nYou've used all 10 attempts. Game over!")
                break

            continue

        attempts += 1
        check_guess(guess, number)

        if guess == number:
            print(f"\nYou guessed the number in {attempts} attempts!")
            if attempts <= 3:
                name = input("\nYou are a genius! Enter your name for the leaderboard: ")
                save_score(name, attempts, difficulty)
                display_leaderboard(difficulty)
            elif attempts > 3:
                leader = input("\nDo you want to save your score? (yes/no): ").strip().lower()
                if leader == "yes":
                    name = input("\nEnter your name for the leaderboard: ")
                    save_score(name, attempts, difficulty)
                    display_leaderboard(difficulty)
                else:
                    print("\nThanks for playing! Better luck next time!")
            break

        if attempts >= max_attempts:
            print(f"\nYou've used all {max_attempts} attempts. Game over!")
            print(f"The number was: {number}")
            leader = input("\nDo you want to save your score? (yes/no): ").strip().lower()
            if leader == "yes":
                name = input("\nEnter your name for the leaderboard: ")
                save_score(name, attempts, difficulty)
                display_leaderboard(difficulty)
            else:
                print("\nThanks for playing! Better luck next time!")
            break


def load_leaderboard():
    """Load the leaderboard from a JSON file"""
    try:
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"easy": {}, "medium": {}, "hard": {}, "insane": {}}

def save_score(name, attempts, difficulty):
    """Save the score and name to leaderboard"""
    leaderboard = load_leaderboard()

    # Create category if it doesn't exist
    if difficulty not in leaderboard:
        leaderboard[difficulty] = {}

    # Only update if new or better score
    if name not in leaderboard[difficulty] or attempts < leaderboard[difficulty][name]:
        leaderboard[difficulty][name] = attempts

    # Keep only top 5 scores
    sorted_scores = sorted(leaderboard[difficulty].items(), key=lambda x: x[1])
    leaderboard[difficulty] = dict(sorted_scores[:5])

    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file, indent=4)

def display_leaderboard(difficulty):
    """Display the leaderboard for a given difficulty"""

    leaderboard = load_leaderboard()
    scores = leaderboard.get(difficulty, {})

    if not scores:
        print(f"\nNo leaderboard entries yet for {difficulty.title()}.")
        return

    print(f"\n🌟 Top 5 Leaderboard — {difficulty.title()} 🌟")
    sorted_scores = sorted(scores.items(), key=lambda x: x[1])
    for i, (name, score) in enumerate(sorted_scores, 1):
        print(f"{i}. {name} — {score} attempts")


def _clear_leaderboard():
    """Clear the leaderboard"""
    with open('leaderboard.json', 'w') as file:
        json.dump({}, file)
    print("Leaderboard cleared!")

if __name__ == "__main__":
   reset = input("\nPress Enter to play: ").lower()
   if reset == "reset":
       _clear_leaderboard()
   play_game()
