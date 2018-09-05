from .exceptions import *
from random import randint

class GuessAttempt(object):
    
    def is_invalid(self):
        if self.hit and self.miss:
            raise InvalidGuessAttempt('Invalid Guess')
    
    def is_hit(self):
        return self.hit
            
    def is_miss(self):
        return self.miss
    
    def __init__(self, guess, hit=None, miss=None):
        self.hit = hit if hit else False
        self.miss = miss if miss else False
        self.is_invalid()

class GuessWord(object):
    #helper function for __init__
    def _mask_word(self):
        self.masked = ('*' * len(self.answer))
        
    #helper function for perform attempt
    def _uncover_word(self, character):
        
        if character in self.masked or character.lower() in self.masked:
            raise InvalidGuessedLetterException('That letter has already been guessed!')
        
        else:
            idxs = [pos for pos, char in enumerate(self.answer) if char.lower() == character.lower()]
            for i in idxs:
                self.masked = self.masked[:i] + character + self.masked[i+1:]
                
    
    #main perform guess function
    def perform_attempt(self, guess):
        if len(guess) > 1 or not guess.isalpha():
            raise InvalidGuessedLetterException('Invalid letter guess!')
        else:
            guess = guess.lower()
            self._uncover_word(guess)
            isHit = guess in self.answer
            isMiss = not isHit
                
            g_attempt = GuessAttempt(guess, hit=isHit, miss=isMiss)
            return g_attempt
    

    def __init__(self, word):
        if len(word) < 1:
            raise InvalidWordException('Invalid Word!')
        else:
            self.answer = word.lower()
        
        self.masked = ''
        self._mask_word()   
        

class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def is_finished(self):
        if self.is_lost() or self.is_won():
            return True
        else:
            return False
    
    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        else:
            return False
    
    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        else:
            return False
            
    def decrement_guesses(self):
        self.remaining_misses -= 1
        
    
    def add_guess(self, guess):
        self.previous_guesses.append(guess)
        
    
    def get_rand_int(self, range):
        rand_idx = randint(0, range)
        return rand_idx
        
    @classmethod
    def select_random_word(cls, words):

        if len(words) < 1:
            raise InvalidListOfWordsException('Invalid List of Words!')
        
        else:
            rand_idx = randint(0, len(words)-1)
            word = words[rand_idx]
            if type(word) != str:
                raise InvalidWordException('Invalid word!')
            else:
                return word
                
    def guess(self, guess):
        if self.is_finished():
            raise GameFinishedException('Game is finished!')
        
        guess = guess.lower()
        self.add_guess(guess)
        word = self.word.perform_attempt(guess)
        
        if word.is_miss():
            self.decrement_guesses()
        
        if self.is_won():
            raise GameWonException('You won the game!')
            
        if self.is_lost():
            raise GameLostException('You lost the game!')
        
        return word
        

    def __init__(self, 
                word_list=None, 
                number_of_guesses=5):
                
                self.word_list = word_list if word_list else HangmanGame.WORD_LIST
                self.remaining_misses = number_of_guesses
                wrd_list = self.word_list
                word = HangmanGame.select_random_word(wrd_list).lower()
                self.word = GuessWord(word)
                self.previous_guesses = []
                
