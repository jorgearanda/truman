#!/usr/bin/env python

import click

from click.testing import CliRunner
from datetime import datetime
from rich.console import Console

from cards import Cards
from game import Game


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
    loc = "games" if not test else "test_output"
    game = Game().new(name, datetime.now(), ussr, usa, bid)
    path = f"{loc}/{name}.tws"
    game.to_file(path)
    console = Console(highlight=False)
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
