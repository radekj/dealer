COLORS = {
    'S': 1,
    'H': 2,
    'D': 3,
    'C': 4,
}

TRUMPS = {
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

def card_image_name(card):
    color, value = card
    return '%s.png' % (color.lower() + value.lower())

def translate_to_value(card):
    try:
        value = int(card[1])
    except ValueError:
        value = TRUMPS.get(card[1])
    color = COLORS.get(card[0])
    return (value, color)

def card_values(cards):
    cards_translated = map(translate_to_value, cards)
    return [i for i in cards_translated]