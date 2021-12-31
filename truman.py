#!/usr/bin/env python

import click

from click.testing import CliRunner
from datetime import datetime
from rich.console import Console


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
    console = Console(highlight=False)
    loc = "games" if not test else "test_output"
    path = f"{loc}/{name}.tws"
    with open(path, "w") as gamefile:
        gamefile.write(f"Name: {name}\n")
        gamefile.write(f"Created: {datetime.now()}\n")
        gamefile.write("Status: Open\n")
        gamefile.write(f"USSR: {ussr}\n")
        gamefile.write(f"USA: {usa}\n")
        gamefile.write(f"Bid: {bid}\n")
        gamefile.write("-" * 80 + "\n")
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
