
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

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value 
    def __repr__(self):
        if self.value: 
            return f'{self.type}:{self.value}'
        return f'{self.type}'        
class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result 

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)

class Reader:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        
        self.pos +=1
        # self.current_char = self.text[self.pos] if self.pos <len(self.text) else None 

        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        elif self.pos >= len(self.text):
            self.current_char = None         

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            
            
            if self.current_char in ' \t':
                self.advance()
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
                char = self.current_char
                self.advance()
                return [], IllegalCharError("'" + char + "'")

        return tokens, None 

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

def run(text):
    reader = Reader(text)
    tokens, error = reader.make_tokens()

    return tokens, error 




