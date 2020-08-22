from typing import List
from tokens import TokenType, Token
from pear import err

class Scanner:
    reservedWords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }

    def __init__(self, src: str):
        self.src = src
        self.tokens = []
        self.start = 0
        self.cur = 0
        self.line = 1

    def hasNext(self) -> bool:
        return self.cur < len(self.src)

    def advance(self) -> str:
        self.cur += 1
        return self.src[self.cur - 1]

    def addToken(self, _type, literal=None) -> None:
        textInToken = self.src[self.start:self.cur]
        self.tokens.append(Token(_type, textInToken, literal, self.line)) 
        
    def match(self, expect: str) -> bool:
        if not self.hasNext: return False
        if not self.src[self.cur] == expect: return False

        self.cur += 1
        return True

    def peek(self) -> str:
        if not self.hasNext(): return '\0'
        return self.src[self.cur]

    def peekTwo(self) -> str:
        if self.cur + 1 >= len(self.src): return '\0'
        return self.src[self.cur + 1]

    # need a custom function because Python's isdigit takes 
    # things we can't necessarily parse (exponent unicodes, etc.)
    def isDigit(self, char: str) -> bool:
        return '0' <= char <= '9'

    def isAlpha(self, char: str) -> bool:
        return 'a' <= char <= 'z' or 'A' <= char <= Z or char == '_'

    def isAlphaNumeric(self, char: str) -> bool:
        return self.isDigit(char) or self.isAlpha(char)    

    def scanToken(self):
        c = self.advance()
        if c == '(': self.addToken(TokenType.LEFT_PAREN)
        elif c == ')': self.addToken(TokenType.RIGHT_PAREN)
        elif c == '{': self.addToken(TokenType.LEFT_BRACE)
        elif c == '}': self.addToken(TokenType.RIGHT_BRACE)
        elif c == ',': self.addToken(TokenType.COMMA)
        elif c == '.': self.addToken(TokenType.DOT)
        elif c == '-': self.addToken(TokenType.MINUS)
        elif c == '+': self.addToken(TokenType.PLUS)
        elif c == ';': self.addToken(TokenType.SEMICOLON)
        elif c == '*': self.addToken(TokenType.STAR)
        elif c == '!': self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=': self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<': self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>': self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '"': 
            # consume the string until the closing quote 
            while not self.peek() == '"' and self.hasNext():
                if self.peek() == '\n': self.line += 1
                self.advance()

            if not self.hasNext():
                err(self.line, "Unterminated string.")
            else:
                self.advance()
                # skip first and last chars of range to avoid quotes
                self.addToken(TokenType.STRING, self.src[self.start+1:self.cur-1])

        elif self.isDigit(c):
            while(self.isDigit(self.peek())): self.advance()

            if self.peek() == '.' and self.isDigit(self.peekTwo()):
                self.advance()

            while(self.isDigit(self.peek())): self.advance()
            self.addToken(TokenType.NUMBER, float(self.src[self.start:self.cur]))

        elif self.isAlpha(c):
            while(self.isAlphaNumeric(self.peek())): self.advance()
            text = self.src[self.start:self.cur]
            _type = self.reservedWords.get(text, TokenType.IDENTIFIER)
            self.addToken(_type)

        elif c == '/': 
            if self.match('/'): # handle comments
                while not self.peek() == '\n' and self.hasNext(): self.advance()
            elif self.match('*'):
                # consume multiline comment until end
                while not (self.peek() == '*' and self.peekTwo() == '/') and self.hasNext():
                    if self.peek() == '\n': self.line += 1
                    self.advance()
                if not self.hasNext():
                    err(self.line, "Unterminated multiline comment.")
                else: # skip over the '*' and '/'
                    self.advance()
                    self.advance()

            else: self.addToken(TokenType.SLASH)

        elif c == ' ' or c == '\r' or c == '\t': pass
        elif c == '\n': self.line += 1
        else:
            err(self.line, "Invalid character encountered.")


    def getTokens(self) -> List[Token]:
        while(self.hasNext()):
            self.start = self.cur
            self.scanToken()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

