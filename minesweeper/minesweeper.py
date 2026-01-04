from minesweeper.minesweeper_ui import MinesweeperUI
from minesweeper.minefield import MineField


class Minesweeper:
    def __init__(self, width: int, height: int, n_mines: int):
        self._mf = MineField(width, height, n_mines)
        self._ui = MinesweeperUI(width, height)

    def run(self):
        self._ui.draw_frame
