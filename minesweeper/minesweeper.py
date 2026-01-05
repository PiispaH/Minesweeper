from typing import Callable, Set, Tuple, Union
import numpy as np
from itertools import product
from numpy.typing import NDArray
from minesweeper.minefield import MineField, CellState
from minesweeper.minesweeper_ui import MinesweeperUI, UIAction
from minesweeper.utils import GameState

type index_set = Set[Tuple[int, int]]


class Minesweeper:
    def __init__(self, width: int, height: int, n_mines: int, headless: bool = False):

        self._mf = MineField(width, height, n_mines)
        self._ui = MinesweeperUI(width, height)

        self._unopened = np.ones((height, width), dtype=bool)
        self._flagged = np.zeros((height, width), dtype=bool)

        self._gamestate = GameState.NOT_STARTED

        self.run: Callable[[], None]
        if headless:
            self._run_headless()
        else:
            self._run_with_ui()

    def _run_with_ui(self):
        """Runs the game with UI"""
        ui_grid = np.array(
            [[CellState.UNOPENED for x in range(self._mf._width)] for y in range(self._mf._height)],
            dtype=object,
        )
        minefield = None

        while True:
            act = self._ui.draw_frame(ui_grid, self._gamestate)
            if act:
                if act.action == UIAction.EXIT:
                    exit()

                if act.action == UIAction.OPEN and self._gamestate != GameState.LOST:
                    all_unnopened = not np.logical_not(self._unopened).any()

                    if self._gamestate == GameState.NOT_STARTED and all_unnopened:
                        self._gamestate = GameState.PLAYING
                        self._mf.new_minefield(act.x, act.y)
                        minefield = self._get_grid()
                    elif self._flagged[act.y][act.x]:
                        continue

                    self._reveal(act.x, act.y)
                    if self._mf._cell_at(act.x, act.y) == CellState.CELL_0:
                        _ = self._reveal_3x3(act.x, act.y)
                    self._check_win()

                elif act.action == UIAction.FLAG and self._gamestate == GameState.PLAYING:
                    if self._unopened[act.y][act.x]:
                        self._toggle_flag(act.x, act.y)

                elif act.action == UIAction.NEW_GAME:
                    self._new_game()

                ui_grid = np.where(self._unopened, CellState.UNOPENED, minefield)  # type: ignore
                ui_grid = np.where(self._flagged, CellState.FLAG, ui_grid)  # type: ignore

    def _run_headless(self):
        """Runs the game without UI"""
        raise NotImplementedError

    def _new_game(self):
        self._gamestate = GameState.NOT_STARTED
        self._unopened.fill(True)
        self._flagged.fill(False)
        ui_grid = np.array(
            [[CellState.UNOPENED for x in range(self._mf._width)] for y in range(self._mf._height)],
            dtype=object,
        )
        return ui_grid

    def _get_grid(self) -> NDArray:
        """Gives the minefield without the walls"""
        grid = self._mf.get_minefield()
        grid = grid[1:-1, 1:-1]
        return grid

    def _reveal(self, x: int, y: int):
        """Reveal single cell"""
        if not bool(self._unopened[y][x]):
            return

        self._unopened[y][x] = False
        if self._mf._cell_at(x, y) == CellState.MINE:
            self._gamestate = GameState.LOST

    def _reveal_3x3(self, x: int, y: int, checked: Union[index_set, None] = None) -> index_set:
        """Recursively blow open the empty caverns"""
        if checked is None:
            checked = set()

        for i, j in self.nbr_inds(x, y):
            self._unopened[j][i] = False

        # Hop to neighboring zero cell that hasn't been checked yet
        for i, j in self._mf._get_nbr_inds_of_types(x, y, CellState.CELL_0):
            if (i, j) not in checked:
                checked.add((i, j))
                checked |= self._reveal_3x3(i, j, checked)

        return checked

    def _toggle_flag(self, x: int, y: int):
        """Toggles the flag state of an unopened cell"""
        self._flagged[y][x] = not self._flagged[y][x]

    def nbr_inds(self, x: int, y: int):
        """Returns the indices of the non-wall neighbours of the given cell"""
        res = set()
        for dx, dy in product((-1, 0, 1), repeat=2):
            i = x + dx
            j = y + dy

            if -1 in (i, j) or i == self._mf._width or j == self._mf._height:
                continue
            else:
                res.add((i, j))
        return res

    def _check_win(self):
        if len(np.transpose((self._unopened).nonzero())) == self._mf._n_mines:
            self._gamestate = GameState.WON
            self._flagged[:] = self._unopened[:]
