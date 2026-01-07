from typing import Annotated
import typer
from .minesweeper_ import Minesweeper

app = typer.Typer()

width_type = Annotated[int, typer.Argument(help="The width of the grid.", min=3, max=30, clamp=True)]
height_type = Annotated[int, typer.Argument(help="The height of the grid", min=3, max=16, clamp=True)]
n_mines_type = Annotated[int, typer.Argument(help="The amount of mines.", min=0, max=99, clamp=True)]


@app.command()
def run(width: width_type = 30, height: height_type = 16, n_mines: n_mines_type = 99):
    ms = Minesweeper(width, height, n_mines, rnd_seed=42)
    ms.run()
