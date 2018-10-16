# https://www.jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1

import sys

import Dalaran.lexer.lexer
import Dalaran.lexer.tokens


def hearthstone_lex(characters,
                    tokens_exprs=Dalaran.lexer.tokens.token_exprs):
    return Dalaran.lexer.lexer.lex(characters, tokens_exprs)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]

        with open(filename) as card:
            card_text = card.read()

    else:
        card_text = sys.stdin.read()

    tokens = hearthstone_lex(card_text)

    for token in tokens:
        print(token)
