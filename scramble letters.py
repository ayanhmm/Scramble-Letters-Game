import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
wildcard = '*'
HAND_SIZE = 7
def getrandomletter():
    mystr = 'bcdfghjklmnpqrstvwxyzaeiou'
    mylist = list(mystr)
    letter = random.choice(mylist)
    return letter
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
WORDLIST_FILENAME = "words.txt"

def load_words(): #recieving words from word list
    """ Returns a list of valid words. Words are strings of lowercase letters. """
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
    and the values are integer counts, for the number of times that an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
# -----------------------------------
def get_word_score(word, n): #gives score... Assumes the word is avalid word.	
    #The first component is the sum of the points for letters in the word.
    wordguessedlist = list(word)
    pointstype1 = 0; pointstype2 = 0
    for letter in wordguessedlist:
        curletterpoints = SCRABBLE_LETTER_VALUES[letter]
        pointstype1 = pointstype1 + curletterpoints
    #print(pointstype1)
	
    # The second component is the larger of:
    #1 or 7*wordlen - 3*(n-wordlen), where wordlen is the length of the word and n is the hand length when the word was played
    lengthscore = (7*len(word)) - (3*n)
    if lengthscore<1:
        pointstype2 = 1
    else :
        pointstype2 = lengthscore
    #print(pointstype2)
    
    #The score for a word is the product of two components:
    return pointstype1*pointstype2
def display_hand(hand):#displays letters in hand # You will need to modify this for Problem #4.
    """  For example:         display_hand({'a':1, 'x':2, 'l':3, 'e':1})
         Should print out something like: a x x l l l e the order of the letters is unimportant.    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):     # print all on the same line
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line
def deal_hand(n):    # Returns a random hand containing n lowercase letters.
    """
    ceil(n/3) letters in the hand should be VOWELS (note, ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are letters and the values are the number of times the particular letter is repeated in that hand.

    n: int >= 0  returns: dictionary (string -> int)
    """ 
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1 #adding to dictionary
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    hand[wildcard] = hand.get(wildcard, 0) + 1

    return hand #print (deal_hand(6))

# Problem #2: Update a hand by removing letters
def update_hand(hand, word):  # Updates the hand: uses up the letters in the given word and returns the new hand, without those letters in it.
    # Does NOT assume that hand contains every letter in word at least as many times as the letter appears in word.
    # punishes if the above happens by removing common letters from hand

    handy = hand.copy() #duplicating
    for letter in word:
        state = letter in handy
        if state == False and letter != '*':
            # Letters that appear in word more times than in hand should never result in a negative count;
            print("out of bounds hogaya");
            for let in word:  # removing common letters
                state2 = let in handy
                if (state2 == True) and (handy[let] > 0):
                    handy[let] = handy[let] - 1
            return handy
    starcount = 0
    starsinhand = 0
    if '*' in hand :
      starsinhand = hand['*']
    for letter in word:
       if letter == '*' and starsinhand>0:
          starcount = starcount + 1
       if starcount > starsinhand:
           print("itne * toh haath mein hain hee nahn")
           for let in word:  # removing common letters
               handy[let] -= 1
           return handy


    for letter in handy:
        lettercount = 0
        for letter2 in word:
            if letter == letter2:
                lettercount += 1
        if lettercount > handy[letter]:
            print("itne ", letter, " toh haath mein hain hee nahn")
            for let in word:  # removing common letters
                handy[let] -= 1
            return handy

    for letter in word:
        state3 = letter in handy
        if (state3 == True):
            if handy[letter] > 0:
                handy[letter] = handy[letter] - 1
    return handy
# Problem #3: Test word validity
def is_valid_word(word, hand, word_list):  # Returns True if word is in the word_list and is entirely composed of letters in the hand.
    for letter in word: #see if only required letters are present
        state = letter in hand
        if state == False:
            # Letters that appear in word more times than in hand should never result in a negative count;
            return False
    for letter in hand: # see if quantity of a letter is same
        lettercount = 0
        for letter2 in word:
            if letter == letter2:
                lettercount += 1
        if lettercount > hand[letter]:
            return False
    starcount = 0
    starsinhand = 0
    if '*' in hand :
      starsinhand = hand['*']
    for letter in word:
       if letter == '*' and starsinhand>0:
          starcount = starcount + 1
       if starcount > starsinhand:
         return starcount == starsinhand
    for validword in word_list:
        if len(validword) == len(word):
            for i in range(0,len(word),1):
                if word[i] != "*":
                    if word[i] != validword[i]:
                        break
                if word[i] == "*":
                    vovela = "a"
                    vovele = "e"
                    voveli= "i"
                    vovelo = "o"
                    vovelu = "u"
                    currletter = validword[i]
                    if (currletter != vovela) and (currletter != vovele) and (currletter != voveli) and (currletter != vovelo) and (currletter != vovelu):
                         break

                if i == len(word) - 1:
                    print(validword)
                    return True

    return word in word_list
# Problem #5: Playing a hand
def calculate_handlen(hand): #Returns the length (number of letters) in the current hand
    currhand = []
    hand_touple = hand.values()
    handlen = 0
    for number in hand_touple:
        handlen += number
    return handlen

def play_hand(hand, word_list, turnscore):
    display_hand(hand) #The hand is displayed.
    n = calculate_handlen(hand)
    #print(n)
    if n == 0: # The hand finishes when there are no more unused letters or string '!!'
        print("total score for this turn: ",turnscore) # The sum of the word scores is displayed when the hand finishes.
        return turnscore
    word = input("enter a valid word...(!! to end turn )")  # The user may input a word.
    if word == "!!": # The hand finishes when there are no more unused letters or string '!!'
        print("total score for this turn: ",turnscore) # The sum of the word scores is displayed when the hand finishes.
        return turnscore
    newhand = update_hand(hand, word) # When any word is entered (valid or invalid), it uses up letters from the hand.
    # An invalid word is rejected, and a message is displayed asking the user to choose another word.
    state = is_valid_word(word, hand, word_list)
    if state == True:
        curscore = get_word_score(word, n)
        turnscore += curscore
        print("score for this word is: ",curscore)
    else:
        print("invalidword so no points")

    turnscore = play_hand(newhand, word_list, turnscore)
    return turnscore



    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is two exclamation points:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function
# Problem #6: Playing a game
def substitute_hand(hand):
    hanny = hand.copy()
    letter = input("type letter to be replaced")
    if letter not in hanny: #If user provide a letter not in the hand, the hand should be the same.
        print("yeh toh hai hee nahn")
        return hanny
    newletter = getrandomletter()
    if newletter in hanny : #The new letter hould be different from hand
        newletter = getrandomletter()
    value = hanny[letter]
    del(hanny[letter])  # delete entry
    hanny[newletter] = value

    return hanny

def play_game(word_list,subcount,totalscore,recount):
    hand = deal_hand(6)
    display_hand(hand)

    #For each hand, before playing, ask the user if they want to substitute one letter for another.
    #This can only be done once during the game. Once the substitue option is used, the user should not be asked
    if subcount == 0:
       subschoice = input("do you want to subs a choice yes/no")
       if subschoice == "yes":
           hand = substitute_hand(hand)
           subcount += 1

    turnscore = 0
    turnscore = play_hand(hand, word_list, turnscore)
    #Accumulates the score for each hand into a total score for the entire series

    #For each hand, ask the user if they would like to replay the hand. and keep the better of the two scores for that hand.
    #This can only be done once during the game.
    if recount == 0:
       rechoice = input("do you want to redo yes/no")
       if rechoice == "yes":
           newscore = 0
           newscore = play_hand(hand, word_list, newscore)
           recount += 1
           if newscore > turnscore:
               turnscore = newscore

    #Returns the total score for the series of hands
    totalscore += turnscore
    print("round ends at total points ",totalscore)
    return (subcount,totalscore,recount)
def play_more(word_list,subcount,totalscore,recount):
    more = input("do you want to play more? yes/no")
    if more == "yes":
        (subcount, totalscore, recount) = play_game(word_list, subcount, totalscore, recount)
        play_more(word_list,subcount,totalscore,recount)
    else:
        print("game over with points",totalscore)
        return (subcount, totalscore, recount)

word_list = load_words()
subcount= 0
recount = 0
totalscore = 0
(subcount,totalscore,recount) = play_game(word_list,subcount,totalscore,recount)
play_more(word_list,subcount,totalscore,recount)



"""
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
"""

#word = "*pple"
#hand = {'a': 1, 'p': 2, 'l': 2, 'e': 1 , '*': 1}
#n=6
#turnscore = 0
#subcount= 0
#print(play_hand(hand, word_list, turnscore))
#print(deal_hand(6))