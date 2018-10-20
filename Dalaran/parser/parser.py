from fireplace.cards.utils import *
from .utils import *

from .parse_patterns import *


def parse_tokens(type_, tokens):
    tags = {}
    attributes = {}

    tokens = bidirectional_iterator(tokens)

    while True:
        try:
            token = tokens.next()

        except StopIteration:
            break

        token_type = token[1]
        token_value = token[0]

        if token_type == 'ABILITY':
            assert type_ == CardType.MINION
                
            tags[GameTag[token_value.upper()]] = True

        elif token_type == 'ACTION':
            assert type_ == CardType.SPELL

            if attributes.get('play'):
                attributes['play'] = attributes['play'] + (parse_action(token, tokens),)

            else:
                attributes['play'] = (parse_action(token, tokens),)

        elif token_type == 'TARGET':
            assert type_ == CardType.SPELL

            target = globals().get(token_value.upper(), None)
            assert isinstance(target, SetOpSelector)

            token = tokens.next()

            token_type = token[1]
            token_value = token[0]

            assert token_type == 'ACTION'

            if token_type == 'ACTION':
                if attributes.get('play'):
                    attributes['play'] = attributes['play'] + (parse_action(token, tokens, target=target),)

                else:
                    attributes['play'] = (parse_action(token, tokens, target=target),)


    return tags, attributes


def parse_card(name, type_, cost, class_, tokens, atk=None, health=None):
    type_ = type_ if isinstance(type_, CardType) else CardType[type_.upper()]
    class_ = class_ if isinstance(
        class_, CardClass) else CardClass[class_.upper()]

    assert isinstance(cost, int)

    tags, attributes = parse_tokens(type_, tokens)

    tags[GameTag.CARDNAME] = name
    tags[GameTag.COST] = cost
    tags[GameTag.CARDTYPE] = type_
    tags[GameTag.CLASS] = class_

    if atk is not None:
        assert isinstance(atk, int)
        tags[GameTag.ATK] = atk

    if health is not None:
        assert isinstance(atk, int)
        tags[GameTag.HEALTH] = health

    values = {'tags': tags}
    values.update(attributes)

    card = type('CUSTOM_{}'.format(name), (), values)
    return card


def register_card(card):
    custom_card(card)