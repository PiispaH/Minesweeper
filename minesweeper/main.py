import typer
from minesweeper.minesweeper import run

app = typer.Typer()


@app.command()
def mono():
    run()
