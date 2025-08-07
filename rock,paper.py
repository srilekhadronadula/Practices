import random

def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif ((user_choice == "rock" and computer_choice == "scissors") or
          (user_choice == "scissors" and computer_choice == "paper") or
          (user_choice == "paper" and computer_choice == "rock")):
        return "You Win!"
    else:
        return "You Lose!"

def rock_paper_scissors():
    user_score = 0
    computer_score = 0
    print("Welcome to Rock, Paper, Scissors!")
    
    while True:
        user_choice = input("\nChoose: rock, paper, or scissors (or type 'quit' to exit): ").strip().lower()
        
        if user_choice == "quit":
            print(f"\nFinal Score - You: {user_score} | Computer: {computer_score}")
            print("Thanks for Playing!")
            break
        
        if user_choice not in ["rock", "paper", "scissors"]:
            print("Invalid choice! Please enter rock, paper, or scissors.")
            continue
        
        computer_choice = get_computer_choice()
        print(f"Computer's choice: {computer_choice}")
        
        result = determine_winner(user_choice, computer_choice)
        print(f"Result: {result}")
        
        if result == "You Win!":
            user_score += 1
        elif result == "You Lose!":
            computer_score += 1
        
        print(f"Score - You: {user_score} | Computer: {computer_score}")
        
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            print(f"\nFinal Score - You: {user_score} | Computer: {computer_score}")
            print("Goodbye!")
            break

rock_paper_scissors()
