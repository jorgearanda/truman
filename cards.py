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

    def move(self, name, dest):
        if name in self.cards.keys():
            self.cards[name].location = dest
        elif name in {"ussr", "usa", "deck", "discard", "board", "removed", "box"}:
            for card in self.cards_in(name).keys():
                self.move(card, dest)
        elif name in {"early", "mid", "late"}:
            for card in self.cards.values():
                if card.stage == name:
                    self.move(card.short, dest)

    def cards_in(self, location):
        return {
            card.short: card
            for card in self.cards.values()
            if card.location == location
        }

    def setup(self):
        for short, card in self.cards.items():
            if card.stage == "early":
                self.move(short, "deck")
            self.move("china", "ussr")


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


def test_card_move():
    cards = Cards()
    cards.move("nasser", "ussr")
    assert cards.cards["nasser"].location == "ussr"


def test_card_move_from_location():
    cards = Cards()
    cards.setup()
    cards.move("deck", "discard")
    assert cards.cards["truman"].location == "discard"


def test_card_move_stage():
    cards = Cards()
    cards.move("mid", "deck")
    assert cards.cards["ussuri"].location == "deck"


def test_cards_in():
    cards = Cards()
    assert len(cards.cards_in("box")) == 110
    cards.move("nasser", "ussr")
    assert len(cards.cards_in("box")) == 109
    assert len(cards.cards_in("ussr")) == 1


def test_setup():
    cards = Cards()
    cards.setup()
    assert len(cards.cards_in("deck")) == 38
