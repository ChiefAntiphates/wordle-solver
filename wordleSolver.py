from audioop import reverse
import re
import random

def initPotential(dictionary):
    words = []
    file = open(dictionary, 'r')
    for word in file:
        word = word.strip()
        if len(word) == 5:
            words.append(word)
    return words

def getMostCommonChars(potentials, exclude=[]):
    chars = {}
    for word in potentials:
        for char in word:
            if char not in exclude:
                if char in chars:
                    chars[char] += 1
                else:
                    chars[char] = 1
    #Return the most common characters in the remaining words
    return(sorted(chars, key=chars.get, reverse=True)[:5])


def getDifferentCharWords(potentials, allowed_repeats=0):#
    suggested = []
    for word in potentials:
        repeats = 0
        chars = []
        for char in word:
            if char in chars:
                repeats += 1
            chars.append(char)
        if repeats <= allowed_repeats:
            suggested.append(word)
    if len(suggested)==0 and allowed_repeats <= 5:#
        suggested = getDifferentCharWords(potentials, allowed_repeats+1)
    return suggested

def getMostOfCertain(potentials, certain=['a','e','i','o','u']):
    most_certain = 0
    suggested = []

    for word in potentials:
        certain_no = 0
        for char in word:
            if char in certain:
                certain_no += 1
        if certain_no > most_certain:
            most_certain = certain_no
            suggested = [word]
        elif certain_no == most_certain:
            suggested.append(word)
    return suggested

def checkRegex(maybes, search_string):
    #Take string as "..rry" where dot is missing char
    potentials = []
    for word in maybes:
        if re.search(search_string, word):
            potentials.append(word)
    return potentials

def checkContains(maybes, required_chars):
    potentials = []
    for word in maybes:
        valid = True
        for char in required_chars:
                if char not in word:
                    valid = False
        if valid:
            potentials.append(word)
    return potentials

def checkNotContains(maybes, bad_chars):
    potentials = []
    for word in maybes:
        valid = True
        for char in bad_chars:
                if char in word:
                    valid = False
        if valid:
            potentials.append(word)
    return potentials

def printSuggestedWords(suggested):
    print("\nHere are some other words I think it could be...")
    print(suggested)


def solve(helping):
    potential_words = initPotential('wordle-dictionary.txt')
    close_chars = []
    removed_chars = []
    found_chars = []
    regex = ['.','.','.','.','.']
    found = False
    guesses = 0
    suggested_words = getMostOfCertain(getDifferentCharWords(potential_words), getMostCommonChars(potential_words))
  
    while not found:
        guesses += 1
        print(f"\n\n\nGuess {guesses}\n\nThere are currently {len(potential_words)} potential answers.\n")
        computer_guess = random.choice(suggested_words)
        print(f"I guess the word is... {computer_guess}!")
        if helping:
            if len(suggested_words) > 1:
                printSuggestedWords(suggested_words[:5].remove(computer_guess))
            if suggested_words[:5] != potential_words:
                if input("\nWould you like to see all potential words? (y/n): ").lower().strip() == 'y':
                    print(potential_words)
                    printSuggestedWords(suggested_words[:5])
        
            valid_guess = False
            while not valid_guess:
                guess = input("\nPlease enter your guess: ").lower().strip()
                if (len(guess) == 5):
                    valid_guess = True
                else:
                    print("Please make sure your guess is 5 letters.")

        
            if input("\nWas your guess correct? (y/n): ").lower().strip() == 'y':
                found = True
                print(f"\n\nYou got the right answer '{guess}' after {guesses} guesses!")
                break
        else:
            if input("\nIs my guess correct? (y/n): ").lower().strip() == 'y':
                found = True
                print(f"\n\nI got the right answer of '{computer_guess}'! After {guesses} guesses!")
                break
        
        known = input("\nPlease enter which (if any) characters were in the correct place: ").lower().strip()
        close = input("\nPlease enter which (if any) characters were correct but in the wrong place: ").lower().strip()

        word = computer_guess
        if helping:
            word = guess

        for char in known:
            if char in close_chars:
                close_chars.remove(char)
            if char not in found_chars:
                found_chars.append(char)
            indexes = []
            for i in range(len(word)):
                if word[i] == char:
                    indexes.append(i)
            for i in indexes:
                regex[i] = char
        
        for char in close:
            if char not in close_chars:
                close_chars.append(char)
            for i in range(len(word)):
                if word[i] == char:
                    if "^" in regex[i]:
                        regex[i] = regex[i][:-1]+char+"]"
                    else:
                        regex[i] = f"[^{char}]"
        for char in word:
            if char not in found_chars and char not in close_chars:
                removed_chars.append(char)
        
        potential_words = checkNotContains(potential_words, removed_chars)
        potential_words = checkRegex(potential_words, ''.join(regex))
        potential_words = checkContains(potential_words, close_chars)
        suggested_words = getMostOfCertain(getDifferentCharWords(potential_words), getMostCommonChars(potential_words, found_chars+close_chars))



if __name__ == "__main__":
    game_mode = input("Do you want to play against the solver or use the solver as a tool? (play/tool): ").lower().strip()
    valid = False
    while not valid:
        if game_mode == "play":
            input("Think of a 5 letter word, then hit 'Enter' and see if the solver can guess it...")
            solve(helping=False)
            valid=True
        elif game_mode == "tool":
            solve(helping=True)
            valid=True
        else:
            game_mode = input("Invalid input. Try again: (play/tool)").lower().strip()