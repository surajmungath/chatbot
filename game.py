import random
from collections import Counter

class AlgebraGame:
    @staticmethod
    def generate_problem():
        problem_type = random.choice(["one-step", "two-step"])
        if problem_type == "one-step":
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
            answer = a + b
            problem = f"{a} + {b} = ?"
            return {"problem": problem, "answer": answer, "a": a, "b": b}
        else:
            a = random.randint(-10, 10)
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
            answer = a * b + c
            problem = f"{a} * {b} + {c} = ?"
            return {"problem": problem, "answer": answer, "a": a, "b": b, "c": c}

    @staticmethod
    def check_answer(user_answer, correct_answer):
        try:
            return int(user_answer) == correct_answer
        except ValueError:
            return False

class HangmanGame:
    WORDS = {
        'fruits': '''apple banana mango strawberry orange grape pineapple apricot lemon coconut 
            watermelon cherry papaya berry peach lychee muskmelon kiwi blueberry raspberry 
            plum pomegranate tangerine guava nectarine fig'''.split(),
        'animals': '''lion tiger elephant giraffe zebra kangaroo penguin dolphin whale shark 
            monkey chimpanzee gorilla bear wolf fox deer rabbit squirrel raccoon koala 
            panda rhinoceros hippopotamus camel leopard jaguar'''.split(),
        'vehicles': '''car truck motorcycle bicycle helicopter airplane train bus subway boat 
            ship yacht scooter ambulance firetruck taxi limousine tractor bulldozer crane 
            forklift jetski submarine'''.split(),
        'countries': '''india america china japan australia brazil canada france germany italy 
            spain russia mexico england portugal sweden norway finland denmark ireland 
            scotland netherlands belgium'''.split(),
        'sports': '''cricket football basketball baseball tennis volleyball hockey rugby golf 
            boxing wrestling swimming cycling skating skiing surfing badminton archery 
            bowling karate judo'''.split(),
        'colors': '''red blue green yellow purple orange brown black white pink 
            gray violet indigo maroon turquoise magenta crimson azure teal 
            gold silver bronze copper'''.split(),
        'professions': '''doctor teacher engineer lawyer pilot chef artist musician writer 
            programmer scientist architect nurse dentist accountant designer journalist 
            photographer firefighter policeman professor'''.split(),
        'food': '''pizza pasta burger sandwich taco sushi noodles rice curry bread 
            salad soup steak pancake waffle omelette lasagna dumpling kebab 
            sausage hotdog'''.split(),
        'weather': '''sunny rainy cloudy stormy windy snowy foggy humid dry cool 
            warm hot cold freezing mild pleasant breezy frosty thunder 
            lightning hail'''.split(),
        'instruments': '''guitar piano violin drums flute saxophone trumpet harp 
            keyboard xylophone clarinet accordion banjo cello harmonica mandolin 
            ukulele trombone bagpipe'''.split()
    }

    @staticmethod
    def new_game():
        # Choose a random category
        category = random.choice(list(HangmanGame.WORDS.keys()))
        # Choose a random word from that category
        word = random.choice(HangmanGame.WORDS[category]).strip()
        return {
            "word": word.upper(),
            "display": ["_" for _ in word],
            "guessed": [],
            "chances": len(word) + 2,
            "status": "playing",
            "category": category
        }

    @staticmethod
    def make_guess(game_state, guess):
        if not guess.isalpha() or len(guess) != 1:
            return {"success": False, "message": "Please enter a single letter"}

        guess = guess.upper()
        if guess in game_state["guessed"]:
            game_state["status"] = "lost"
            return {
                "success": False,
                "message": f"Game Over! You already guessed '{guess}'. The word was {game_state['word']}",
                "display": " ".join(game_state["display"]),
                "guessed": ", ".join(game_state["guessed"]),
                "status": game_state["status"],
                "category": game_state["category"],
                "chances": game_state["chances"],
                "game_over": True
            }

        game_state["guessed"].append(guess)
        word = game_state["word"]
        
        if guess in word:
            # Update display
            for i, letter in enumerate(word):
                if letter == guess:
                    game_state["display"][i] = guess
            message = "Good guess!"
            success = True
        else:
            game_state["chances"] -= 1
            message = f"Wrong guess! {game_state['chances']} chances left"
            success = False

        # Check win/lose conditions
        if "_" not in game_state["display"]:
            game_state["status"] = "won"
            message = f"Congratulations! You won! The word was {word}"
        elif game_state["chances"] <= 0:
            game_state["status"] = "lost"
            message = f"Game Over! The word was {word}"

        return {
            "success": success,
            "message": message,
            "display": " ".join(game_state["display"]),
            "guessed": ", ".join(game_state["guessed"]),
            "status": game_state["status"],
            "category": game_state["category"],
            "chances": game_state["chances"]
        }

class QuizGame:
    test_questions = [
        {"question": "What is the capital of India?", "answer": "New Delhi"},
        {"question": "Who is known as the Father of the Nation in India?", "answer": "Mahatma Gandhi"},
        {"question": "What is the national animal of India?", "answer": "Tiger"},
        {"question": "In which year did India gain independence from British rule?", "answer": "1947"},
        {"question": "What is the national sport of India?", "answer": "Hockey"},
        {"question": "Who was the first Prime Minister of India?", "answer": "Jawaharlal Nehru"},
        {"question": "Which Indian city is known as the Silicon Valley of India?", "answer": "Bangalore"},
        {"question": "What is the official language of India?", "answer": "Hindi"},
        {"question": "Which river is considered the holiest in India?", "answer": "Ganges"},
        {"question": "What is the currency of India?", "answer": "Indian Rupee"},
        {"question": "Who was the first woman Prime Minister of India?", "answer": "Indira Gandhi"},
        {"question": "What is the national flower of India?", "answer": "Lotus"},
        {"question": "Who is the current President of India?", "answer": "Droupadi Murmu"},
        {"question": "What is the national bird of India?", "answer": "Peacock"},
        {"question": "Which Indian state is famous for tea plantations?", "answer": "Assam"},
        {"question": "In which city is the Taj Mahal located?", "answer": "Agra"},
        {"question": "Which is the largest state in India by area?", "answer": "Rajasthan"},
        {"question": "Who is known as the Missile Man of India?", "answer": "Dr. A.P.J. Abdul Kalam"},
        {"question": "What is the official name of India?", "answer": "Republic of India"},
        {"question": "Which Indian festival is known as the Festival of Lights?", "answer": "Diwali"},
        {"question": "Who wrote the Indian national anthem?", "answer": "Rabindranath Tagore"},
        {"question": "What is the highest civilian award in India?", "answer": "Bharat Ratna"},
        {"question": "Which city is known as the Pink City of India?", "answer": "Jaipur"},
        {"question": "What is the national tree of India?", "answer": "Banyan"},
        {"question": "Which mountain range forms the northern boundary of India?", "answer": "Himalayas"},
        {"question": "Which Indian city is famous for its film industry, often referred to as Bollywood?", "answer": "Mumbai"},
        {"question": "Who was the first Governor-General of independent India?", "answer": "Lord Mountbatten"},
        {"question": "Which city is known as the Garden City of India?", "answer": "Bangalore"},
        {"question": "What is the main language spoken in Kerala?", "answer": "Malayalam"},
        {"question": "Which Indian freedom fighter is also known as Netaji?", "answer": "Subhas Chandra Bose"},
        {"question": "Who is the father of the Indian Constitution?", "answer": "Dr. B.R. Ambedkar"},
        {"question": "Which river is considered the longest in India?", "answer": "Ganga"},
        {"question": "Which state is known as the Land of the Rising Sun in India?", "answer": "Arunachal Pradesh"},
        {"question": "What is the national game of India?", "answer": "Field Hockey"},
        {"question": "Which Indian state is known for its backwaters?", "answer": "Kerala"},
        {"question": "Which Indian city is known as the City of Joy?", "answer": "Kolkata"},
        {"question": "Who is known as the Iron Man of India?", "answer": "Sardar Vallabhbhai Patel"},
        {"question": "What is the famous dance form of Tamil Nadu?", "answer": "Bharatanatyam"},
        {"question": "Which famous Indian leader's birthday is celebrated as National Youth Day?", "answer": "Swami Vivekananda"},
        {"question": "Which state is the birthplace of Mahatma Gandhi?", "answer": "Gujarat"},
        {"question": "Which is the most popular language spoken in India?", "answer": "Hindi"},
        {"question": "Who is the founder of the Bhakshi Vidyalaya movement?", "answer": "Raja Rammohan Roy"},
        {"question": "Which is the largest lake in India?", "answer": "Vembanad Lake"},
        {"question": "Which famous Indian cricketer is known as 'Master Blaster'?", "answer": "Sachin Tendulkar"},
        {"question": "What is the national motto of India?", "answer": "Satyamev Jayate"},
        {"question": "Which state in India is famous for its 'Pukka Sahib' temples?", "answer": "Punjab"},
        {"question": "Which city is known for its famous Qutub Minar?", "answer": "Delhi"},
        {"question": "Which popular movie genre is India famous for?", "answer": "Bollywood"},
        {"question": "Who wrote '1984'?", "answer": "George Orwell"},
        {"question": "What is the capital of Canada?", "answer": "Ottawa"},
        {"question": "Who was the first person to walk on the moon?", "answer": "Neil Armstrong"},
        {"question": "What is the hardest natural substance on Earth?", "answer": "Diamond"},
        {"question": "Who discovered penicillin?", "answer": "Alexander Fleming"},
        {"question": "What is the currency of Japan?", "answer": "Yen"},
        {"question": "What is the capital of Australia?", "answer": "Canberra"},
        {"question": "Who wrote 'Pride and Prejudice'?", "answer": "Jane Austen"},
        {"question": "What is the square root of 144?", "answer": "12"},
        {"question": "What is the longest river in the world?", "answer": "Nile"},
        {"question": "Who was the first president of the United States?", "answer": "George Washington"},
        {"question": "What is the chemical symbol for water?", "answer": "H2O"},
        {"question": "What is the capital of Germany?", "answer": "Berlin"},
        {"question": "Who discovered electricity?", "answer": "Benjamin Franklin"},
        {"question": "What is the smallest country in the world?", "answer": "Vatican City"},
        {"question": "What is the tallest building in the world?", "answer": "Burj Khalifa"},
        {"question": "What is the national flower of Japan?", "answer": "Cherry Blossom"},
        {"question": "What is the primary language spoken in Brazil?", "answer": "Portuguese"},
        {"question": "What year did World War I begin?", "answer": "1914"},
        {"question": "Who invented the telephone?", "answer": "Alexander Graham Bell"},
        {"question": "Who wrote 'The Great Gatsby'?", "answer": "F. Scott Fitzgerald"},
        {"question": "What is the largest desert in the world?", "answer": "Sahara"},
        {"question": "What is the capital of Spain?", "answer": "Madrid"},
        {"question": "What is the longest-running TV show?", "answer": "The Simpsons"},
        {"question": "Who invented the light bulb?", "answer": "Thomas Edison"},
        {"question": "What is the capital of Italy?", "answer": "Rome"},
        {"question": "What is the most spoken language in the world?", "answer": "Mandarin"},
        {"question": "What year did World War II end?", "answer": "1945"},
        {"question": "Who painted the Sistine Chapel?", "answer": "Michelangelo"},
        {"question": "What is the largest island in the world?", "answer": "Greenland"},
        {"question": "What is the name of the longest mountain range in the world?", "answer": "Andes"},
        {"question": "What is the boiling point of water?", "answer": "100°C"},
        {"question": "Who invented the airplane?", "answer": "Wright Brothers"},
        {"question": "What is the official language of Egypt?", "answer": "Arabic"},
        {"question": "What is the chemical symbol for oxygen?", "answer": "O"},
        {"question": "Who wrote 'Moby Dick'?", "answer": "Herman Melville"},
        {"question": "Who is known as the 'father of modern chemistry'?", "answer": "Antoine Lavoisier"},
        {"question": "What is the capital of India?", "answer": "New Delhi"},
        {"question": "Who discovered the theory of relativity?", "answer": "Albert Einstein"},
        {"question": "What is the largest city in the United States by population?", "answer": "New York City"},
        {"question": "What is the currency of the United Kingdom?", "answer": "Pound Sterling"},
        {"question": "What is the hardest rock?", "answer": "Diamond"},
        {"question": "Who was the first woman to win a Nobel Prize?", "answer": "Marie Curie"},
        {"question": "What is the most populous country in the world?", "answer": "China"},
        {"question": "Who wrote 'The Catcher in the Rye'?", "answer": "J.D. Salinger"},
        {"question": "What is the capital of Russia?", "answer": "Moscow"},
        {"question": "Who invented the printing press?", "answer": "Johannes Gutenberg"},
        {"question": "What is the national animal of Australia?", "answer": "Kangaroo"},
        {"question": "What is the currency of the United States?", "answer": "Dollar"},
        {"question": "What is the square root of 81?", "answer": "9"},
        {"question": "Who is known as the 'father of modern economics'?", "answer": "Adam Smith"},
        {"question": "What is the capital of South Korea?", "answer": "Seoul"},
        {"question": "What is the name of the longest river in South America?", "answer": "Amazon River"},
        {"question": "What is the tallest waterfall in the world?", "answer": "Angel Falls"},
        {"question": "Who discovered the law of gravity?", "answer": "Isaac Newton"},
        {"question": "What is the largest country by area?", "answer": "Russia"},
        {"question": "Who invented the steam engine?", "answer": "James Watt"},
        {"question": "What is the largest land animal?", "answer": "African Elephant"},
        {"question": "What is the national sport of Japan?", "answer": "Sumo Wrestling"},
        {"question": "What is the largest continent?", "answer": "Asia"},
        {"question": "What is the capital of Egypt?", "answer": "Cairo"},
        {"question": "Who wrote 'Frankenstein'?", "answer": "Mary Shelley"},
        {"question": "What is the deepest ocean in the world?", "answer": "Pacific Ocean"},
        {"question": "What is the chemical symbol for carbon?", "answer": "C"},
        {"question": "Who is known as the 'father of modern chemistry'?", "answer": "Antoine Lavoisier"},
        {"question": "What is the capital of Brazil?", "answer": "Brasília"},
        {"question": "Who invented the computer?", "answer": "Charles Babbage"},
        {"question": "What is the longest mountain range in North America?", "answer": "Rocky Mountains"},
        {"question": "What is the square root of 169?", "answer": "13"},
        {"question": "What is the capital of Turkey?", "answer": "Ankara"},
        {"question": "Who was the first female prime minister of the United Kingdom?", "answer": "Margaret Thatcher"},
        {"question": "What is the largest country in Africa?", "answer": "Algeria"},
        {"question": "What is the main ingredient in sushi?", "answer": "Rice"},
        {"question": "Who wrote 'Crime and Punishment'?", "answer": "Fyodor Dostoevsky"},
        {"question": "What is the capital of China?", "answer": "Beijing"},
        {"question": "Who developed the theory of evolution?", "answer": "Charles Darwin"},
        {"question": "What is the largest lake in Africa?", "answer": "Lake Victoria"},
        {"question": "Who wrote 'War and Peace'?", "answer": "Leo Tolstoy"},
        {"question": "What is the tallest building in the United States?", "answer": "One World Trade Center"},
        {"question": "What is the currency of France?", "answer": "Euro"},
        {"question": "What is the national flower of the United States?", "answer": "Rose"},
        {"question": "Who invented the polio vaccine?", "answer": "Jonas Salk"},
        {"question": "What is the longest river in Europe?", "answer": "Volga River"},
        {"question": "What is the national animal of India?", "answer": "Tiger"},
        {"question": "What is the square root of 225?", "answer": "15"},
        {"question": "Who wrote 'Jane Eyre'?", "answer": "Charlotte Bronte"},
        {"question": "What is the capital of Mexico?", "answer": "Mexico City"},
        {"question": "What is the name of the largest volcano in the world?", "answer": "Mauna Loa"},
        {"question": "Who invented the refrigerator?", "answer": "Jacob Perkins"},
        {"question": "What is the name of the largest island in the Mediterranean Sea?", "answer": "Sicily"},
        {"question": "What is the boiling point of water in Fahrenheit?", "answer": "212°F"},
        {"question": "Who invented the radio?", "answer": "Guglielmo Marconi"},
        {"question": "What is the national dish of Spain?", "answer": "Paella"},
        {"question": "Who wrote 'The Odyssey'?", "answer": "Homer"},
        {"question": "What is the capital of Thailand?", "answer": "Bangkok"},
        {"question": "Who invented the washing machine?", "answer": "Jacob Christian Schäffer"},
        {"question": "What is the name of the highest peak in Africa?", "answer": "Mount Kilimanjaro"},
        {"question": "What is the national animal of Russia?", "answer": "Brown Bear"},
        {"question": "What is the square root of 196?", "answer": "14"},
        {"question": "Who wrote 'Les Misérables'?", "answer": "Victor Hugo"},
        {"question": "What is the capital of Argentina?", "answer": "Buenos Aires"},
        {"question": "What is the national sport of Canada?", "answer": "Ice Hockey"},
        {"question": "Who invented the safety pin?", "answer": "Walter Hunt"},
        {"question": "What is the currency of Italy?", "answer": "Euro"},
        {"question": "What is the national flower of Australia?", "answer": "Golden Wattle"},
        {"question": "Who wrote 'Wuthering Heights'?", "answer": "Emily Bronte"},
        {"question": "What is the name of the largest desert in Asia?", "answer": "Gobi Desert"},
        {"question": "What is the boiling point of water in Celsius?", "answer": "100°C"},
        {"question": "Who invented the microphone?", "answer": "Emile Berliner"},
        {"question": "What is the capital of Saudi Arabia?", "answer": "Riyadh"},
        {"question": "Who invented the telegraph?", "answer": "Samuel Morse"},
        {"question": "What is the national animal of Germany?", "answer": "Eagle"},
        {"question": "What is the square root of 256?", "answer": "16"},
        {"question": "Who wrote 'The Count of Monte Cristo'?", "answer": "Alexandre Dumas"},
        {"question": "What is the capital of Colombia?", "answer": "Bogotá"},
        {"question": "What is the national sport of Brazil?", "answer": "Football"},
        {"question": "Who invented the sewing machine?", "answer": "Elias Howe"},
        {"question": "What is the currency of Spain?", "answer": "Euro"},
        {"question": "What is the national flower of Canada?", "answer": "Maple Leaf"},
        {"question": "Who wrote 'Dracula'?", "answer": "Bram Stoker"},
        {"question": "What is the name of the largest glacier in the world?", "answer": "Lambert Glacier"},
        {"question": "What is the boiling point of water in Kelvin?", "answer": "373.15K"},
        {"question": "Who invented the typewriter?", "answer": "Christopher Sholes"},
        {"question": "What is the national dish of Italy?", "answer": "Pasta"},
        {"question": "Who wrote 'The Hobbit'?", "answer": "J.R.R. Tolkien"},
        {"question": "What is the capital of South Africa?", "answer": "Pretoria"},
        {"question": "Who invented the fax machine?", "answer": "Alexander Bain"},
        {"question": "What is the name of the largest cave in the world?", "answer": "Son Doong Cave"},
        {"question": "What is the national animal of China?", "answer": "Giant Panda"},
        {"question": "What is the square root of 324?", "answer": "18"},
        {"question": "Who wrote 'The Divine Comedy'?", "answer": "Dante Alighieri"},
        {"question": "What is the capital of Chile?", "answer": "Santiago"},
        {"question": "Which is the first state to have its own law on Right to Information?", "answer": "Tamil Nadu"},
        {"question": "What is the name of India's first space satellite?", "answer": "Aryabhata"},
        {"question": "Which is the oldest university in India?", "answer": "Nalanda University"},
        {"question": "Who founded the 'Indian National Congress'?", "answer": "Allan Octavian Hume"},
        {"question": "What is the highest rank in the Indian Army?", "answer": "Field Marshal"},
        {"question": "Who is the first Indian to win a Nobel Prize in Physics?", "answer": "C.V. Raman"},
        {"question": "What is the popular name of the National Capital Region?", "answer": "NCR"},
        {"question": "Which is the first Indian film to win an Oscar?", "answer": "Mother India"},
        {"question": "What is the state fruit of West Bengal?", "answer": "Jackfruit"},
        {"question": "Who is the famous founder of the 'Bharatiya Janata Party'?", "answer": "Atal Bihari Vajpayee"}
    ]

    @staticmethod
    def get_random_question():
        random.shuffle(QuizGame.test_questions)
        question = QuizGame.test_questions[0]
        return {
            "question": question["question"],
            "answer": question["answer"]
        }

    @staticmethod
    def check_answer(user_answer, correct_answer):
        return user_answer.strip().lower() == correct_answer.strip().lower()

    @staticmethod
    def get_questions(num_questions=5):
        random.shuffle(QuizGame.test_questions)
        return QuizGame.test_questions[:num_questions]

# Legacy support for command-line interface
def algebra_practice_game():
    game = AlgebraGame()
    score = 0
    num_problems = 5
    
    print(f"\nWelcome to Algebra Practice! You'll get {num_problems} problems to solve.")
    for i in range(num_problems):
        problem_data = game.generate_problem()
        problem = problem_data["problem"]
        correct_answer = problem_data["answer"]
        
        user_answer = input(f"\nProblem {i+1}: {problem}\nYour answer: ")
        
        if game.check_answer(user_answer, correct_answer):
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect. The correct answer was {correct_answer}")
    
    print(f"\nFinal score: {score}/{num_problems}")

def hangman_game():
    game_state = HangmanGame.new_game()
    print("\nWelcome to Hangman!")
    print(f"Category: {game_state['category'].upper()}")
    print(f"The word has {len(game_state['word'])} letters.")
    
    while game_state["status"] == "playing":
        print(f"\nWord: {' '.join(game_state['display'])}")
        print(f"Guessed letters: {', '.join(game_state['guessed'])}")
        print(f"Chances left: {game_state['chances']}")
        
        guess = input("Enter a letter: ").upper()
        result = HangmanGame.make_guess(game_state, guess)
        print(result["message"])
    
    if game_state["status"] == "won":
        print("\nCongratulations! You won!")
    else:
        print("\nGame Over! Better luck next time!")

def question_game():
    game = QuizGame()
    score = 0
    num_questions = int(input("How many questions would you like to answer? "))
    questions = game.get_questions(num_questions)
    
    for question_data in questions:
        question = question_data["question"]
        correct_answer = question_data["answer"]
        
        user_answer = input(f"Question: {question}\nYour answer: ")
        
        if game.check_answer(user_answer, correct_answer):
            score += 1
            print("Correct!")
        else:
            print(f"Incorrect. The correct answer was {correct_answer}")
    
    print(f"\nFinal score: {score}/{num_questions}")

if __name__ == "__main__":
    print("Choose a game:")
    print("1. Algebra Practice")
    print("2. Hangman")
    print("3. Quiz")
    choice = input("Enter your choice (1-3): ")
    
    if choice == "1":
        algebra_practice_game()
    elif choice == "2":
        hangman_game()
    elif choice == "3":
        question_game()
    else:
        print("Invalid choice!")
