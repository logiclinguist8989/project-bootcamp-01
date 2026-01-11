import random

def run_math_safari():
    print("--- 🐔 Welcome to Kukhuri-Ka: Math Safari! ---")
    score = 0
    total_questions = 3
    
    # 1. Ask for name (User Input)
    player_name = input("Enter your name, little explorer: ")
    print(f"Goal: Help the chick find {total_questions} bananas by solving math puzzles!\n")

    # 2. Game Loop
    for i in range(1, total_questions + 1):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 5)
        correct_answer = num1 + num2
        
        print(f"Puzzle {i}: What is {num1} + {num2}?")
        
        # 3. Error Handling 
        try:
            user_answer = int(input("Your answer: "))
        except ValueError:
            print("Oops! Please type a number (like 5 or 10).")
            continue

        # 4. Conditional Logic
        if user_answer == correct_answer:
            print("✅ Correct! You found a banana! 🍌")
            score += 1
        else:
            print(f"❌ Not quite! The answer was {correct_answer}.")

    # 5. Final Result (Scoring System)
    print(f"\n--- Game Over, {player_name}! ---")
    print(f"Total Bananas Found: {score}/{total_questions}")
    
    if score == total_questions:
        print("🏆 Perfect Score! You are a Math Hero!")
    else:
        print("Keep practicing to find more bananas!")

if __name__ == "__main__":
    run_math_safari()