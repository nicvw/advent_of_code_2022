import typer
from rich import print

from advent.calories import total
from advent.camp_cleanup import overlapping_pairs
from advent.rock_paper_scissors import rounds_from_datafile, convert_game, tally_scores
from advent.rucksack import auth_stickers, reorder_rucksacks

app = typer.Typer()

@app.command()
def calories(number: int):
    print(total(number))

@app.command()
def rock_paper_scissors(convert: bool = typer.Option(default=False)):
    game_data = rounds_from_datafile()
    if convert:
        game_data = convert_game(game_data)
    p1, p2 = tally_scores(game_data)
    print(f"player one: {p1}, player two: {p2}")

@app.command()
def rucksack():
    print(reorder_rucksacks())

@app.command()
def stickers():
    print(auth_stickers())

@app.command()
def overlapping_sections():
    print(overlapping_pairs())
