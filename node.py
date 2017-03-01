# Node class represent every key in the dictionary. It contains a String 
# representing the token, a number representing the frequency, and a pointer
# to the posting in disk

class Node:
    def __init__(self, term, frequency):
        self.term = term
        self.frequency = frequency

    def get_term(self):
        return self.term
    
    def get_frequency(self):
        return self.frequency
    
    def set_frequency(self, frequency):
        self.frequency = frequency