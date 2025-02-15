import sys

from TokensLexer import TokensLexer
from TokensNode import TokensNode
from Token import Token
from Node import Node


class Parser:
    def __init__(self, tokens, lang):
        self.tokens = tokens
        self.lang = lang

        # Базовые параметры
        self.pos = 0
        self.len = len(self.tokens)

    def parse(self):
        node = Node(type=TokensNode.BOF, other=self.statement())
        return node

    def statement(self):
        token = self.peek(0)
        if token.type == TokensNode.EOF:
            return None
        if token.type == TokensLexer.CODE and self.lang.basis[TokensNode.EVENT] == token.value:
            event = token.value
            self.eat(TokensLexer.CODE)
            self.eat(TokensLexer.OPEN_BRACE)
            token = self.peek(0)
            if token.type == TokensLexer.CODE:
                event_name = self.lang.getType(event, token.value)
                if event_name is not False:
                    self.eat(TokensLexer.CODE)
                    self.eat(TokensLexer.CLOSE_BRACE)
                    self.eat(TokensLexer.OPEN_BRACKET)
                    node = Node(type=event_name, value1=self.expression())
                    self.eat(TokensLexer.CLOSE_BRACKET)
                    node.other = self.statement()
                    return node
        if token.type != TokensNode.EOF:
            sys.exit("ERROR IN STATEMENT")

    def expression(self):
        token = self.peek(0)
        if token.assign(TokensLexer.VARIABLE):
            self.eat(TokensLexer.VARIABLE)
            self.eat(TokensLexer.ASSIGN)
            node = Node(type="SET_VARIABLE", value1=Node(type=TokensLexer.VARIABLE,
                                                         id=TokensNode.VALUE,
                                                         value1=token),
                        value2=self.additive())
            self.eat(TokensLexer.SEMICOLON)
            node.other = self.expression()
            return node
        if token.assign(TokensLexer.CODE) and token.value in self.lang.type.keys():
            key1 = token.value
            self.eat(TokensLexer.CODE)
            token = self.eat(TokensLexer.DOT)
            if token.assign(TokensLexer.CODE) and token.value in self.lang.type[key1].keys():
                pass
                self.eat(TokensLexer.CODE)
                self.eat(TokensLexer.OPEN_PARENT)
                node = Node(type=self.lang.type[key1][token.value])
                values = list()
                while not self.peek(0).assign(TokensLexer.CLOSE_PARENT, TokensLexer.EOF):
                    if values:
                        self.eat(TokensLexer.COMMA)
                    value = self.additive().value1
                    if isinstance(value, list):
                        values += value
                    else:
                        values.append(value)
                node.values = values
                self.eat(TokensLexer.CLOSE_PARENT)
                self.eat(TokensLexer.SEMICOLON)
                node.other = self.expression()
                return node
            else:
                sys.exit("ERROR IN EACH ACTION")

    def additive(self):
        value = self.multiplicative()
        while self.peek(0).assign(TokensLexer.PLUS, TokensLexer.MINUS):
            if self.peek(0).assign(TokensLexer.PLUS):
                self.eat(TokensLexer.PLUS)
                value = Node(type="SUM", value1=value, value2=self.multiplicative())
            else:
                self.eat(TokensLexer.MINUS)
                value = Node(type="DIFFERENCE", value1=value, value2=self.multiplicative())
        return value

    def multiplicative(self):
        value = self.primary()
        while self.peek(0).assign(TokensLexer.MULTIPLY, TokensLexer.DIVISION):
            if self.peek(0).assign(TokensLexer.MULTIPLY):
                self.eat(TokensLexer.MULTIPLY)
                value = Node(type="MULTIPLY", value1=value, value2=self.primary())
            else:
                self.eat(TokensLexer.DIVISION)
                value = Node(type="QUOTIENT", value1=value, value2=self.primary())
        return value

    def primary(self):
        token = self.peek(0)
        if token.assign(TokensLexer.VARIABLE):
            self.eat(TokensLexer.VARIABLE)
            return Node(type=TokensLexer.VARIABLE, value1=token, id=TokensNode.VALUE)
        elif token.assign(TokensLexer.NUMBER):
            self.eat(TokensLexer.NUMBER)
            return Node(type=TokensLexer.NUMBER, value1=token, id=TokensNode.VALUE)
        elif token.assign(TokensLexer.STRING):
            self.eat(TokensLexer.STRING)
            return Node(type=TokensLexer.STRING, value1=token, id=TokensNode.VALUE)
        elif token.assign(TokensLexer.OPEN_PARENT):
            self.eat(TokensLexer.OPEN_PARENT)
            value = Node(type=TokensLexer.PARENT, value1=self.additive(), id=TokensNode.VALUE)
            self.eat(TokensLexer.CLOSE_PARENT)
            return value
        elif token.assign(TokensLexer.CODE):
            value = self.peek(0).value
            if value in self.lang.objects.keys():
                return self.createObject()
            else:
                sys.exit("ERROR IN CREATE OBJECT! WRONG NAME")

    def createObject(self):
        value = self.lang.objects[self.peek(0).value]
        values = list()
        self.eat(TokensLexer.CODE)
        self.eat(TokensLexer.OPEN_PARENT)
        while not self.peek(0).assign(TokensLexer.CLOSE_PARENT, TokensLexer.EOF):
            if values:
                self.eat(TokensLexer.COMMA)
            values.append(self.additive().value1.value)
        self.eat(TokensLexer.CLOSE_PARENT)
        return Node(value, Token(value, values), id=TokensNode.VALUE)

    def peek(self, relative_position):
        position = self.pos + relative_position
        if position >= self.len:
            EOF = TokensNode.EOF
            return Token(EOF, EOF)
        return self.tokens[position]

    def next(self):
        self.pos += 1
        return self.peek(0)

    def eat(self, *types):
        value = self.peek(0)
        for type in types:
            if value.type == type:
                return self.next()
        sys.exit("ERROR! Ожидался другой тип данных из " + ' '.join([i for i in types]) + " " + str(self.peek(0)))
