#!/usr/bin/env python

import click

from click.testing import CliRunner
from datetime import datetime
from rich.console import Console

from cards import Cards


@click.group()
def cli():
    pass


@cli.command()
@click.argument("name")
@click.argument("ussr")
@click.argument("usa")
@click.argument("bid", type=int)
@click.option("--test/--no-test", default=False, help="Change output to ./test_output/")
def create(name, ussr, usa, bid, test):
    """Create a new game."""
    cards = Cards()
    cards.setup()
    console = Console(highlight=False)
    loc = "games" if not test else "test_output"
    path = f"{loc}/{name}.tws"
    with open(path, "w") as gamefile:
        gamefile.write(f"Name: {name}\n")
        gamefile.write(f"Created: {datetime.now()}\n")
        gamefile.write(f"USSR: {ussr}\n")
        gamefile.write(f"USA: {usa}\n")
        gamefile.write(f"Bid: {bid}\n")
        gamefile.write("-" * 80 + "\n")
        gamefile.write("Status: Open\n")
        gamefile.write("VPs: 0\n")
        gamefile.write("DEFCON: 5\n")
        gamefile.write("USSR Space Race: 0\n")
        gamefile.write("USA  Space Race: 0\n")
        gamefile.write("-" * 80 + "\n")
        gamefile.write("# Cards\n")
        gamefile.write("\n## USSR\n")
        for card in cards.cards_in("ussr").values():
            gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
        gamefile.write("\n## USA\n")
        for card in cards.cards_in("usa").values():
            gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
        gamefile.write("\n## Board\n")
        for card in cards.cards_in("board").values():
            gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
        gamefile.write("\n## Deck\n")
        for card in cards.cards_in("deck").values():
            gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
        gamefile.write("\n## Discard\n")
        for card in cards.cards_in("discard").values():
            gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
        gamefile.write("\n## Removed\n")
        for card in cards.cards_in("removed").values():
            gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")
        gamefile.write("\n## Box\n")
        for card in cards.cards_in("box").values():
            gamefile.write(f"{card.short:10} - {card.ops} {card.full}\n")

    console.print(f"✨ [bold yellow]{name}[/] created in {path} ✨")


if __name__ == "__main__":
    cli()


# -- Tests --
def test_create():
    name = "test-12345"
    runner = CliRunner()
    result = runner.invoke(cli, ["create", name, "me", "bot", "2", "--test"])
    assert result.exit_code == 0
    assert f"{name} created" in result.output
