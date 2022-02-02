from cards import Cards


class Game:
    def __init__(self, name, created, ussr_name, usa_name, bid):
        self.name = name
        self.created = created
        self.ussr_name = ussr_name
        self.usa_name = usa_name
        self.bid = bid
        self.cards = Cards()
        self.cards.setup()

    def to_file(self, path):
        with open(path, "w") as gamefile:
            gamefile.write(f"Name: {self.name}\n")
            gamefile.write(f"Created: {self.created}\n")
            gamefile.write(f"USSR: {self.ussr_name}\n")
            gamefile.write(f"USA: {self.usa_name}\n")
            gamefile.write(f"Bid: {self.bid}\n")
            gamefile.write("-" * 80 + "\n")
            gamefile.write("Status: Open\n")
            gamefile.write("VPs: 0\n")
            gamefile.write("DEFCON: 5\n")
            gamefile.write("USSR Space Race: 0\n")
            gamefile.write("USA  Space Race: 0\n")
            gamefile.write("-" * 80 + "\n")
            gamefile.write("# Cards\n")
            gamefile.write("\n## USSR\n")
            for card in self.cards.cards_in("ussr").values():
                gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
            gamefile.write("\n## USA\n")
            for card in self.cards.cards_in("usa").values():
                gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
            gamefile.write("\n## Board\n")
            for card in self.cards.cards_in("board").values():
                gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
            gamefile.write("\n## Deck\n")
            for card in self.cards.cards_in("deck").values():
                gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
            gamefile.write("\n## Discard\n")
            for card in self.cards.cards_in("discard").values():
                gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
            gamefile.write("\n## Removed\n")
            for card in self.cards.cards_in("removed").values():
                gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
            gamefile.write("\n## Box\n")
            for card in self.cards.cards_in("box").values():
                gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
