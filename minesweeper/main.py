import typer
from minesweeper.minesweeper import Minesweeper

app = typer.Typer()


@app.command()
def run():
    ms = Minesweeper(30, 16, 99)
    ms.run()
