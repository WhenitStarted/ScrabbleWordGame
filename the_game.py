# MIT Word Project
# This is the code for the full game
# Made by Nick


import math
import os
import random
import string

os.system('cls')

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
VO_and_CO = "aeioubcdfghjklmnpqrstvwxyz"
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, "*": 0,
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def get_word_score(word, n):
    word = word.lower()
    wordTotal = 0
    score = 0
    part_2 = 7 * len(word) - 3 * (n-len(word))

    if "*" in word:
        for i in range(len(word)):
            wordTotal += SCRABBLE_LETTER_VALUES.setdefault(word[i])
            score = wordTotal*part_2
        return score

    for i in range(len(word)):
        wordTotal += SCRABBLE_LETTER_VALUES.setdefault(word[i])
        score = wordTotal*part_2
        if score < 1:
            return(wordTotal + 1)
    else:
        return(score)


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')      # print all on the same line
    print()


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(2):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(1):
        x = random.choice(VOWELS)
        x = "*"
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand, word):
    word = word.lower()
    handCopy = hand.copy()
    for i in range(len(word)):
        handCopy.setdefault(word[i], 0)
        handCopy[word[i]] -= 1
        if handCopy[word[i]] <= 0:
            handCopy.pop(word[i])
    return(handCopy)


def is_valid_word(word, hand, word_list):
    word = word.lower()
    this_hand = hand.copy()
    if "*" in word:
        if str("*") in this_hand.keys():
            this_hand.pop("*")
        for v in VOWELS:
            if word.replace("*", v) in word_list:
                word = word.replace("*", v)
                break
        this_hand[str(v)] = 1

    if word not in word_list:
        return False
    for i in range(len(word)):

        if word[i] in this_hand.keys():
            this_hand[word[i]] -= 1
        else:
            return False

        if this_hand[word[i]] < 0:
            return False
    return True


def calculate_handlen(hand):
    handnum = len(hand)
    return(int(handnum))


def play_hand(hand, word_list):
    word = ""
    totalscore = 0
    while word != "!!":

        hand = update_hand(hand, word)
        n = calculate_handlen(hand)
        if n == 0:
            print("out of words")
            print("This hand got you a score of: " + str(totalscore))
            print("-----------------------------")
            print("")
            break

        print("Current hand is:  ", end='')
        display_hand(hand)

        word = input("Enter word, or !! to indicate you are finished: ")

        if word == str("!!"):
            print("Your total score for this hand is: ".ljust(
                12, ".") + str(totalscore).rjust(5))
            return(totalscore)
            break

        if is_valid_word(word, hand, word_list) != True:
            print("This is not a valid word, try another word")
        else:
            is_valid_word(word, hand, word_list)
            score = get_word_score(word, n)
            print(str(word) + " earned you " + str(score)+" points")
            totalscore += score
            print("Your total score is: "+str(totalscore))
    return (totalscore)


def substitute_hand(hand, letter):
    letter = letter.lower()
    if (letter in hand.keys()) and (letter != "*"):
        while True:
            x = random.choice(VO_and_CO)
            if x in hand.keys():
                continue
            else:
                hand[x] = hand.pop(letter)
                break
    else:
        return (hand)
    return hand


def play_game(word_list):
    print('Welcome to the Word Game'.center(20, '*'))

    hand_num = int(input("Enter total number of hands:"))
    totalscore = 0

    while (hand_num > 0):
        hand = deal_hand(7)

        print("The hand is:  ", end='')
        display_hand(hand)

        while True:
            hand_rep = input(
                ("Would you like to replace a letter in the hand?: "))
            if hand_rep == "yes":
                letter = input(("Which letter do you want to replace?: "))
                substitute_hand(hand, letter)
                break
            elif hand_rep == "no":
                break
            else:
                print(end="")

        score = play_hand(hand, word_list)
        while 1:
            replay = input(
                "Would you like to replay hand? If so I will keep the highest score: ")
            if replay == "yes":
                replay_Score = play_hand(hand, word_list)
                if replay_Score > score:
                    score = replay_Score
                break
            elif replay == "no":

                break

        totalscore += score

        print("--------------------------------------------")
        hand_num -= 1

    print("The Final Score for the game is: " + str(totalscore))
    print("Thank you for playing")


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
