from typing import Callable, Set
import numpy as np
from enum import Enum
from itertools import product
from numpy.typing import NDArray
from minesweeper.minefield import MineField, CellState
from minesweeper.minesweeper_ui import MinesweeperUI, UIAction


class GameState(Enum):
    NOT_STARTED = 0
    PLAYING = 1
    LOST = 2
    WON = 3


class Minesweeper:
    def __init__(self, width: int, height: int, n_mines: int, headless: bool = False):
        self._mf = MineField(width, height, n_mines)
        self._ui = MinesweeperUI(width, height)

        self._unopened = np.ones((height, width), dtype=bool)

        self.run: Callable[[], None]
        if headless:
            self._run_headless()
        else:
            self._run_head()

    def _run_head(self):
        """Runs the game with UI"""
        ui_grid = np.array(
            [[CellState.UNOPENED for x in range(self._mf._width)] for y in range(self._mf._height)], dtype=object
        )
        gamestate = GameState.NOT_STARTED
        while gamestate != GameState.LOST:
            act = self._ui.draw_frame(ui_grid)
            if act:

                if act.action == UIAction.EXIT:
                    exit()

                if act.action == UIAction.OPEN:
                    all_unnopened = not np.logical_not(self._unopened).any()
                    if gamestate == GameState.NOT_STARTED and all_unnopened:
                        gamestate = GameState.PLAYING
                        self._mf.new_minefield(act.x, act.y)
                    if not self._reveal(act.x, act.y):
                        gamestate = GameState.LOST

                if act.action == UIAction.FLAG:
                    pass

                ui_grid = np.where(self._unopened, CellState.UNOPENED, self.get_grid())  # type: ignore
        print("End")

    def _run_headless(self):
        """Runs the game without UI"""
        pass

    def get_grid(self) -> NDArray:
        """Gives the current minefield without the walls"""
        grid = self._mf.get_minefield()
        grid = grid[1:-1, 1:-1]
        return grid

    def _reveal(self, x: int, y: int):
        """Reveal single cell, returns True if the show goes on, False otherwise"""
        if not bool(self._unopened[y][x]):
            return True

        self._unopened[y][x] = False
        if self._mf._cell_at(x, y) == CellState.MINE:
            return False

        if self._mf._cell_at(x, y) == CellState.CELL_0:
            self._reveal_3x3(x, y)
            return True

    def _reveal_3x3(self, x: int, y: int, checked: Set = set()):
        """Recursively blow open the empty caverns"""

        if (x, y) in checked:
            return

        checked.add((x, y))

        for i, j in self.nbr_inds(x, y):
            self._unopened[j][i] = False

        # Hop to neigbor 0 that hasnt been checked yet
        for i, j in self._mf._get_nbr_inds_of_types(x, y, CellState.CELL_0):
            print(i, j)
            return self._reveal_3x3(i, j, checked)

    def nbr_inds(self, x: int, y: int):
        """Returns the indices of the valid neighbours of the given cell"""
        res = set()
        for dx, dy in product((-1, 0, 1), repeat=2):
            i = x + dx
            j = y + dy

            if -1 in (i, j) or i == self._mf._width or j == self._mf._height:
                continue
            else:
                res.add((i, j))

        return res
