from Lang import Lang
from Lexer import Lexer
from Parser import Parser
from Builder import Builder


filename = "../code.txt"
lang = Lang("TokensML.json")

lexer = Lexer(filename)
tokens = lexer.tokenize()

parser = Parser(tokens, lang)
node = parser.parse()
# print(node)

filename = filename.split("/")[-1].split(".")[0]
builder = Builder(node, filename, lang)
reduced = builder.generation()
for pos in reduced:
    print(pos)
print("\nHappy end! :)")
