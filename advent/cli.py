from io import StringIO
import typer
from rich import print

from advent.calories import total
from advent.camp_cleanup import containing_pairs, overlapping_pairs
from advent.comm_device import SignalDecoder
from advent.rock_paper_scissors import rounds_from_datafile, convert_game, tally_scores
from advent.rucksack import auth_stickers, reorder_rucksacks
from advent.stacks import SupplyStacks
from advent.utils import iterate_over_data

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
def containing_sections():
    print(containing_pairs())

@app.command()
def overlapping_sections():
    print(overlapping_pairs())

@app.command()
def stacks(multi: bool = typer.Option(default=False)):
    stacks = [
        ["Z", "J", "N", "W", "P", "S"],
        ["G", "S", "T"],
        ["V", "Q", "R", "L", "H"],
        ["V", "S", "T", "D"],
        ["Q", "Z", "T", "D", "B", "M", "J"],
        ["M", "W", "T", "J", "D", "C", "Z", "L"],
        ["L", "P", "M", "W", "G", "T", "J"],
        ["N", "G", "M", "T", "B", "F", "Q", "H"],
        ["R", "D", "G", "C", "P", "B", "Q", "W"]
    ]
    var = SupplyStacks(moves=iterate_over_data("stack_moves.txt"), stacks=stacks)
    var.move(multi=multi)
    print("".join([x[-1] for x in var.stacks]))

@app.command()
def communicator():
    stream = StringIO(next(iterate_over_data("signal.txt")))
    decoder = SignalDecoder(stream)
    decoder.process_data()
    print(f"start of packet: {decoder.start_of_packet}, start of message: {decoder.start_of_message}")
