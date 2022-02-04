import filecmp

from cards import Cards


class Game:
    def new(self, name, created, ussr_name, usa_name, bid):
        self.name = name
        self.created = created
        self.ussr_name = ussr_name
        self.usa_name = usa_name
        self.bid = bid
        self.status = "Open"
        self.score = 0
        self.defcon = 5
        self.ussr_space_race = 0
        self.usa_space_race = 0
        self.cards = Cards()
        self.cards.setup()
        return self

    def from_file(self, path):
        self.cards = Cards()
        with open(path) as gamefile:
            lines = [line.strip() for line in gamefile.readlines()]

        for idx, line in enumerate(lines):
            match line:
                case "# Meta":
                    self.load_meta(idx + 1, lines)
                case "# General":
                    self.load_state(idx + 1, lines)
                case "# Cards":
                    self.load_cards(idx + 1, lines)
        return self

    def load_meta(self, idx, lines):
        for line in lines[idx:]:
            if line.startswith("---"):
                break
            label, value = line.split(": ", 1)
            match label:
                case "Name":
                    self.name = value
                case "Created":
                    self.created = value
                case "USSR":
                    self.ussr_name = value
                case "USA":
                    self.usa_name = value
                case "Bid":
                    self.bid = value

    def load_state(self, idx, lines):
        for line in lines[idx:]:
            if line.startswith("---"):
                break
            label, value = line.split(": ", 1)
            match label:
                case "Status":
                    self.status = value
                case "VPs":
                    self.score = value
                case "DEFCON":
                    self.defcon = value
                case "USSR Space Race":
                    self.ussr_space_race = value
                case "USA Space Race":
                    self.usa_space_race = value

    def load_cards(self, idx, lines):
        location = None
        for line in lines[idx:]:
            if line.startswith("---"):
                break
            if len(line) == 0:
                continue
            if line == "## USSR":
                location = "ussr"
            elif line == "## USA":
                location = "usa"
            elif line == "## Board":
                location = "board"
            elif line == "## Deck":
                location = "deck"
            elif line == "## Discard":
                location = "discard"
            elif line == "## Removed":
                location = "removed"
            elif line == "## Box":
                location = "box"
            else:
                short = line[:10].strip()
                self.cards.move(short, location)

    def to_file(self, path):
        with open(path, "w") as gamefile:
            gamefile.write("# Meta\n")
            gamefile.write(f"Name: {self.name}\n")
            gamefile.write(f"Created: {self.created}\n")
            gamefile.write(f"USSR: {self.ussr_name}\n")
            gamefile.write(f"USA: {self.usa_name}\n")
            gamefile.write(f"Bid: {self.bid}\n")
            gamefile.write("-" * 80 + "\n")
            gamefile.write("# General\n")
            gamefile.write(f"Status: {self.status}\n")
            gamefile.write(f"VPs: {self.score}\n")
            gamefile.write(f"DEFCON: {self.defcon}\n")
            gamefile.write(f"USSR Space Race: {self.ussr_space_race}\n")
            gamefile.write(f"USA Space Race: {self.usa_space_race}\n")
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


# -- Tests --
def test_no_changes():
    name = "game_test"
    game = Game().new(name, "a timestamp", "me", "bot", 2)
    path = f"test_output/{name}.tws"
    game.to_file(path)
    game.from_file(path)
    path2 = f"test_output/{name}_2.tws"
    game.to_file(path2)
    assert game.name == name
    assert filecmp.cmp(path, path2)
