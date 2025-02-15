import sys

from TokensLexer import TokensLexer as Tokens
from Token import Token


class Lexer:
    def __init__(self, path):
        self.code = open(path, "r", encoding="UTF-8").read()

        # Базовые параметры
        self.pos = 0
        self.len = len(self.code)
        self.tokens = list()

    def tokenize(self):
        token = self.get(0)
        while token != Tokens.EOF:
            if token.isalpha() or token == "_":
                self.tokenizeCode()
            elif token.isdigit() or token in (".", "-"):
                self.tokenizeNumber()
            elif token in ("'", '"'):
                self.tokenizeString()
            elif token == "`":
                self.tokenizeVariable()
            elif token in ("\n", "\t", " "):
                self.next()
            else:
                self.tokenizeChar()
            token = self.get(0)
        return self.tokens

    def tokenizeVariable(self):
        char = self.next()
        value = ""
        while char not in ("`", Tokens.EOF):
            value += char
            char = self.next()
        if char == "`":
            self.addToken(Tokens.VARIABLE, value)
            self.next()
        else:
            sys.exit("ERROR IN VARIABLE")

    def tokenizeString(self):
        key = self.get(0)
        skip = False

        char = self.next()
        value = ""
        while (char != key or skip is True) and char != Tokens.EOF:
            if char == "\\" and skip is False:
                skip = True
            else:
                if skip is True:
                    skip = False
                value += char
            char = self.next()
        if self.get(0) == key:
            self.addToken(Tokens.STRING, value)
            self.next()
        else:
            sys.exit("ERROR IN STRING")

    # Обработка символов
    def tokenizeChar(self):
        char = self.get(0)
        if char == "+":
            self.addToken(Tokens.PLUS, char)
        elif char == "-":
            self.addToken(Tokens.MINUS, char)
        elif char == "*":
            self.addToken(Tokens.MULTIPLY, char)
        elif char == "/":
            self.addToken(Tokens.DIVISION, char)
        elif char == "^":
            self.addToken(Tokens.POWER, char)
        elif char == "<":
            self.addToken(Tokens.OPEN_BRACE, char)
        elif char == ">":
            self.addToken(Tokens.CLOSE_BRACE, char)
        elif char == "(":
            self.addToken(Tokens.OPEN_PARENT, char)
        elif char == ")":
            self.addToken(Tokens.CLOSE_PARENT, char)
        elif char == "{":
            self.addToken(Tokens.OPEN_BRACKET, char)
        elif char == "}":
            self.addToken(Tokens.CLOSE_BRACKET, char)
        elif char == ".":
            self.addToken(Tokens.DOT, char)
        elif char == ",":
            self.addToken(Tokens.COMMA, char)
        elif char == ";":
            self.addToken(Tokens.SEMICOLON, char)
        elif char == ":":
            self.addToken(Tokens.COLON, char)
        elif char == "=":
            self.addToken(Tokens.ASSIGN, char)
        else:
            sys.exit("ERROR IN SYMBOL")
        self.next()

    # Обработка чисел
    def tokenizeNumber(self):
        char = self.get(0)
        value = ""
        while (char.isdigit() or char in ("-", ".")) and char != Tokens.EOF:
            value += char
            char = self.next()
        try:
            self.addToken(Tokens.NUMBER, float(value))
        except ValueError:
            if value in ("-", "."):
                self.pos -= 1
                self.tokenizeChar()
            else:
                sys.exit("ERROR IN NUMBER")

    # Обработка команд
    def tokenizeCode(self):
        char = self.get(0)
        value = ""
        while (char.isalnum() or char == "_") and char != Tokens.EOF:
            value += char
            char = self.next()
        self.addToken(Tokens.CODE, value)

    def get(self, relative_position):
        position = self.pos + relative_position
        if position >= self.len:
            return Tokens.EOF
        return self.code[position]

    def next(self):
        self.pos += 1
        return self.get(0)

    def addToken(self, token_type, token_value):
        self.tokens.append(Token(token_type, token_value))
