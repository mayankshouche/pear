from enum import Enum, auto

TokenTypes = 'LEFT_PAREN RIGHT_PAREN LEFT_BRACE RIGHT_BRACE \
    COMMA DOT MINUS PLUS SEMICOLON SLASH STAR \
    BANG BANG_EQUAL \
    EQUAL EQUAL_EQUAL \
    GREATER GREATER_EQUAL \
    LESS LESS_EQUAL \
    IDENTIFIER STRING NUMBER \
    AND CLASS ELSE FALSE FUN FOR IF NIL OR \
    PRINT RETURN SUPER THIS TRUE VAR WHILE \
    EOF'

TokenType = Enum('TokenType', TokenTypes)

class Token:
    def __init__(self, _type: object, lexeme: str, literal: object, line: int):
        self._type = _type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self):
        lex = self.lexeme if self.lexeme else ""
        lit = self.literal if self.literal else ""
        return str(self._type) + " " + lex + " " + lit