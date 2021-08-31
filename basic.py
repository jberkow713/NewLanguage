
Dict = {}
TT_INT = 'TT_INT'
TT_FLOAT = 'TT_FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
DIGITS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyz'
LETTER = 'LETTER'
WORD = 'WORD'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value 
    def __repr__(self):
        if self.value: 
            return f'{self.type}:{self.value}'
        return f'{self.type}'        
class Error:
    def __init__(self,  position_start, position_end, error_name, details):
        self.error_name = error_name
        self.position_start = position_start
        self.position_end = position_end 
        self.details = details
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'File {self.position_start.fn}, line {self.position_start.ln +1}'
        return result  

class IllegalCharError(Error):
    def __init__(self, position_start, position_end, details):
        super().__init__(position_start, position_end, 'Illegal Character', details)
class Position:

    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln =ln 
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx +=1
        self.col +=1

        if current_char == '\n':
            self.ln +=1
            self.col = 0
        return self
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

class Reader:
    def __init__(self, fn, text):
        self.fn = fn 
        self.text = text
        self.pos = Position(-1,0,-1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        
        self.pos.advance(self.current_char) 
        # self.current_char = self.text[self.pos] if self.pos <len(self.text) else None 

        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
        elif self.pos.idx >= len(self.text):
            self.current_char = None         

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            
            
            if self.current_char in ' \t.,':
                self.advance()
            elif self.current_char in LETTERS:
                tokens.append(self.make_word())
                   
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
                
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()                       
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None 
    
    def make_word(self):
        word_str = ''
        word_length = 0
        word = False

        while self.current_char != None and self.current_char in LETTERS:
            
            if self.current_char in LETTERS:
                word_str += self.current_char
                word_length +=1
            print(word_length)
            if word_length >1:
                word = True 
            self.advance()            
        if word == False:
            return Token(LETTER, word_str)
        else:
            return Token(WORD, word_str)    


    def make_number(self):
        num_str = ''
        FLOAT = False 

        while self.current_char != None and self.current_char in DIGITS or self.current_char == '.':
            
            if FLOAT == True:
                if self.current_char == '.':
                    break 

            if self.current_char in DIGITS:
                num_str +=self.current_char
            if self.current_char == '.':
                num_str +=self.current_char
                FLOAT = True
            
            self.advance()

        if FLOAT == False:
            
            return Token(TT_INT, int(num_str))
        
        else:
            
            return Token(TT_FLOAT, float(num_str))    

def run(fn, text):
    reader = Reader(fn, text)
    tokens, error = reader.make_tokens()

    return tokens, error 




