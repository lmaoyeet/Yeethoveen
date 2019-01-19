from evaluate import Lexer, Evaluator, Parse

def main():
    filename = 'main.yeet'
    file     = open(filename, 'r')
    lexer    = Lexer(file)
    parse    = Parse(lexer.tokens)

    lexer.tokenizer()
    # print("Tokens: ")
    # print(lexer.tokens, "\n")

    parse.build_AST()
    # print("AST:")
    # print (parse.AST, "\n")

    evaluator = Evaluator(parse.AST)
    print("the fucking output:")
    evaluator.run(parse.AST)

if __name__ == '__main__':
   main() 