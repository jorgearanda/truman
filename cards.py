class Card:
    def __init__(self, card_line):
        card_values = card_line.split(",")
        self.short = card_values[0]
        self.full = card_values[1]
        self.stage = card_values[2]
        self.type = card_values[3]
        self.on_event = card_values[4]
        self.ops = int(card_values[5])
        self.location = "box"


class Cards:
    def __init__(self):
        self.cards = {}
        with open("cards.csv") as f:
            for line in f.readlines():
                card = Card(line)
                self.cards[card.short] = card


# -- Tests --
def test_card():
    card = Card("sogov,Socialist Governments,early,ussr,discard,3")
    assert card.short == "sogov"
    assert card.full == "Socialist Governments"
    assert card.stage == "early"
    assert card.type == "ussr"
    assert card.on_event == "discard"
    assert card.ops == 3


def test_cards():
    cards = Cards()
    assert len(cards.cards) == 110
    assert cards.cards["ussuri"].type == "usa"
