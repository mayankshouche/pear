from expr import Expr, Binary, Grouping, Literal, Unary
from tokens import Token, TokenType

class ASTPrinter(Expr.Visitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)
    
    def visitBinaryExpr(self, expr: 'Binary'):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: 'Grouping'):
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: 'Literal'):
        if expr.value is None: return 'nil'
        return str(expr.value)

    def visitUnaryExpr(self, expr: 'Unary'):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs):
        ret = '(' + name
        for expr in exprs:
            ret += " "
            ret += expr.accept(self)
        ret += ")"
        return ret

expression = Binary(Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)), Token(TokenType.STAR, "*", None, 1), Grouping(Literal(45.67)))
print(ASTPrinter().print(expression))