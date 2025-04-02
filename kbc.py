import random
import time
import os

def clear_screen():
    """Clear the terminal screen based on operating system"""
    os.system('cls' if os.name == 'nt' else 'clear')

class QuizGame:
    def __init__(self):
        # Prize money levels
        self.levels = [1000, 2000, 3000, 5000, 10000, 20000, 40000, 80000, 160000, 320000, 640000, 1280000, 2500000, 5000000, 10000000]
        
        # Questions bank - format: [question, option_a, option_b, option_c, option_d, correct_answer_index]
        self.questions_bank = [
            # Easy questions
            ["In which programming language was Facebook initially created?", "Python", "Java", "JavaScript", "PHP", 4],
            ["Who is the founder of Microsoft?", "Steve Jobs", "Bill Gates", "Elon Musk", "Mark Zuckerberg", 2],
            ["HTML stands for?", "Hyper Text Markup Language", "High Tech Machine Learning", "Hyper Transfer Mode Language", "Hybrid Text Management Logic", 1],
            ["Which of these is not a programming language?", "Java", "Python", "Photoshop", "Ruby", 3],
            ["What does CPU stand for?", "Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Control Processing Unit", 1],
            
            # Medium questions
            ["Which data structure follows the LIFO principle?", "Queue", "Stack", "Linked List", "Array", 2],
            ["What does API stand for?", "Application Programming Interface", "Application Protocol Integration", "Advanced Programming Interface", "Automated Program Instruction", 1],
            ["Which of these is a NoSQL database?", "MySQL", "PostgreSQL", "MongoDB", "Oracle", 3],
            ["What is the time complexity of binary search?", "O(n)", "O(n²)", "O(log n)", "O(n log n)", 3],
            ["Which of these is not a cloud computing service model?", "SaaS", "PaaS", "IaaS", "DaaS", 4],
            
            # Hard questions
            ["Which sorting algorithm has the best average-case performance?", "Quick Sort", "Bubble Sort", "Selection Sort", "Insertion Sort", 1],
            ["In Python, what is the difference between deep copy and shallow copy?", "No difference", "Deep copy creates a new object, shallow copy creates a reference", "Shallow copy copies all nested objects, deep copy doesn't", "Deep copy copies all nested objects, shallow copy doesn't", 4],
            ["Which design pattern is used when you need a single instance of a class?", "Factory", "Observer", "Singleton", "Decorator", 3],
            ["What is the purpose of the ACID properties in database systems?", "Data encryption", "Ensuring transaction reliability", "Performance optimization", "User authentication", 2],
            ["Which protocol is used for secure communication over the Internet?", "HTTP", "FTP", "SMTP", "HTTPS", 4]
        ]
        
        # Lifelines
        self.lifelines = {
            "50:50": True,
            "Ask the Audience": True,
            "Phone a Friend": True
        }
        
        self.money = 0
        self.safe_levels = [4, 9, 14]  # Questions 5, 10, 15 are safe levels (indices 4, 9, 14)
        self.current_questions = []
        
    def select_questions(self):
        """Select 15 random questions from the bank, ensuring a mix of difficulties"""
        easy = self.questions_bank[:5]
        medium = self.questions_bank[5:10]
        hard = self.questions_bank[10:]
        
        # Shuffle each difficulty group
        random.shuffle(easy)
        random.shuffle(medium)
        random.shuffle(hard)
        
        # Take 5 from each difficulty level
        self.current_questions = easy[:5] + medium[:5] + hard[:5]
    
    def use_fifty_fifty(self, question):
        """Implement the 50:50 lifeline by removing two incorrect options"""
        if not self.lifelines["50:50"]:
            print("You've already used the 50:50 lifeline!")
            return question
        
        # Get correct answer index
        correct_index = question[-1]
        
        # Get indices of incorrect answers
        incorrect_indices = [i for i in range(1, 5) if i != correct_index]
        
        # Randomly select two incorrect options to eliminate
        to_eliminate = random.sample(incorrect_indices, 2)
        
        # Create a new question with eliminated options
        new_question = question.copy()
        for idx in to_eliminate:
            new_question[idx] = ""
        
        self.lifelines["50:50"] = False
        return new_question
    
    def ask_the_audience(self, question):
        """Implement the Ask the Audience lifeline"""
        if not self.lifelines["Ask the Audience"]:
            print("You've already used the Ask the Audience lifeline!")
            return
        
        correct_index = question[-1]
        
        # Simulate audience voting with bias toward correct answer
        votes = {
            1: random.randint(10, 30),
            2: random.randint(10, 30),
            3: random.randint(10, 30),
            4: random.randint(10, 30)
        }
        
        # Boost the correct answer
        votes[correct_index] += random.randint(30, 60)
        
        # Normalize to 100%
        total = sum(votes.values())
        for k in votes:
            votes[k] = round((votes[k] / total) * 100)
        
        # Adjust to make sure total is 100%
        diff = 100 - sum(votes.values())
        votes[correct_index] += diff
        
        print("\nAudience Results:")
        print(f"A: {votes[1]}%   B: {votes[2]}%")
        print(f"C: {votes[3]}%   D: {votes[4]}%")
        
        self.lifelines["Ask the Audience"] = False
    
    def phone_a_friend(self, question):
        """Implement the Phone a Friend lifeline"""
        if not self.lifelines["Phone a Friend"]:
            print("You've already used the Phone a Friend lifeline!")
            return
        
        correct_index = question[-1]
        
        # Friend has 80% chance of being correct
        if random.random() < 0.8:
            friend_guess = correct_index
            certainty = random.choice(["I'm pretty sure", "I'm certain", "I think", "I believe"])
        else:
            # Wrong guess
            options = [1, 2, 3, 4]
            options.remove(correct_index)
            friend_guess = random.choice(options)
            certainty = random.choice(["I'm not entirely sure, but", "I think", "Maybe", "If I had to guess"])
        
        option_letters = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
        
        print("\nCalling your friend...")
        time.sleep(2)
        print(f"Friend: {certainty} the answer is {option_letters[friend_guess]}. Good luck!")
        
        self.lifelines["Phone a Friend"] = False
    
    def get_safe_money(self, question_index):
        """Determine how much money the player takes home if they quit"""
        for safe_level in reversed(self.safe_levels):
            if question_index > safe_level:
                return self.levels[safe_level]
        return 0
    
    def display_lifelines(self):
        """Display available lifelines"""
        print("\nLifelines:")
        for lifeline, available in self.lifelines.items():
            status = "Available" if available else "Used"
            print(f"{lifeline}: {status}")
    
    def play(self):
        """Main game loop"""
        self.select_questions()
        
        print("Welcome to WHO WANTS TO BE A MILLIONAIRE!")
        print("Answer 15 questions correctly to win ₹10,000,000")
        print("You have 3 lifelines: 50:50, Ask the Audience, and Phone a Friend")
        input("Press Enter to begin...")
        
        for i in range(len(self.current_questions)):
            clear_screen()
            
            # Show current progress
            print(f"Question {i+1} of 15 for ₹{self.levels[i]:,}")
            if i > 0:
                print(f"Current winnings: ₹{self.levels[i-1]:,}")
            
            # Display lifelines
            self.display_lifelines()
            
            # Display question
            question = self.current_questions[i]
            print(f"\n{question[0]}")
            print(f"A. {question[1]}       B. {question[2]}")
            print(f"C. {question[3]}       D. {question[4]}")
            
            # Get player's action
            while True:
                action = input("\nEnter your choice (A/B/C/D), use a lifeline (1=50:50, 2=Audience, 3=Phone), or walk away (W): ").upper()
                
                if action in ['A', 'B', 'C', 'D']:
                    answer_index = {'A': 1, 'B': 2, 'C': 3, 'D': 4}[action]
                    break
                elif action == '1':
                    if self.lifelines["50:50"]:
                        question = self.use_fifty_fifty(question)
                        print("\nAfter 50:50:")
                        print(f"A. {question[1]}       B. {question[2]}")
                        print(f"C. {question[3]}       D. {question[4]}")
                    else:
                        print("You've already used this lifeline!")
                elif action == '2':
                    self.ask_the_audience(question)
                elif action == '3':
                    self.phone_a_friend(question)
                elif action == 'W':
                    if i == 0:
                        print("You're walking away with nothing!")
                    else:
                        print(f"You're walking away with ₹{self.levels[i-1]:,}!")
                    return
                else:
                    print("Invalid choice. Try again.")
            
            # Check answer
            if answer_index == question[-1]:
                print(f"Correct answer! You've won ₹{self.levels[i]:,}")
                self.money = self.levels[i]
                
                if i == len(self.levels) - 1:
                    print("\nCONGRATULATIONS! You've won the grand prize of ₹10,000,000!")
                    break
                
                # Ask if they want to continue after safe levels
                if i in self.safe_levels:
                    print(f"You've reached a safe level! You'll take home at least ₹{self.levels[i]:,}")
                
                continue_game = input("Do you want to continue to the next question? (Y/N): ").upper()
                if continue_game != 'Y':
                    print(f"Thanks for playing! You're taking home ₹{self.money:,}")
                    break
            else:
                print(f"I'm sorry, that's incorrect. The correct answer was option {['A', 'B', 'C', 'D'][question[-1]-1]}.")
                
                # Calculate money to take home based on safe levels
                self.money = self.get_safe_money(i)
                print(f"You're going home with ₹{self.money:,}")
                break
            
            input("\nPress Enter to continue to the next question...")
        
        print("\nThanks for playing Who Wants to be a Millionaire!")

if __name__ == "__main__":
    game = QuizGame()
    game.play()
