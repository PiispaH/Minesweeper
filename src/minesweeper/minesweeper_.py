from itertools import product
import os
from queue import Queue
from threading import Event, Thread
from typing import Set, Tuple, Union
import numpy as np
from numpy.typing import NDArray
from .minefield import CellState, MineField
from .minesweeper_ui import MinesweeperUI
from .utils import Action, GameState, Interaction

type index_set = Set[Tuple[int, int]]


class MinesweeperBase:
    """Base class for the minesweeper game"""

    def __init__(self, width: int, height: int, n_mines: int, rnd_seed: Union[int, None] = None):
        """
        Args:
            width: The width of the minefield.
            height: The height of the minefield.
            n_mines: The amount of mines in the minefield.
            rnd_seed: An initial starting point for the seed used in random number generators.
        """

        self._mf: MineField

        self._width = width
        self._height = height
        self._n_mines = n_mines

        self._clamp_grid_specs()

        self._mines_left = self._n_mines

        self._unopened = np.ones((height, width), dtype=np.bool)
        self._flagged = np.zeros((height, width), dtype=np.bool)

        self.gamestate = GameState.NOT_STARTED

        self._rnd_seed = rnd_seed

    def _clamp_grid_specs(self):
        """Adjusts the parameters if needed to ensure a valid minefield"""

        self._n_mines = min(self._n_mines, self._width * self._height - 1)

    def _new_minefield(self, x: int, y: int):
        self._mf = MineField(self._width, self._height, self._n_mines, x, y, rnd_seed=self._rnd_seed)
        if self._rnd_seed is not None:
            self._rnd_seed += 1

    def get_grid(self) -> NDArray:
        """Gives the minefield without the walls"""
        grid = self._mf.get_minefield()
        grid = grid[1:-1, 1:-1]
        return grid

    def _new_game(self):
        self.gamestate = GameState.NOT_STARTED
        self._mines_left = self._n_mines
        self._unopened.fill(True)
        self._flagged.fill(False)

    def _open_cell(self, x: int, y: int):
        self._reveal(x, y)
        if self._mf.cell_at(x, y) == CellState.CELL_0:
            _ = self._reveal_3x3(x, y)

    def _reveal(self, x: int, y: int):
        """Reveal single cell"""
        if not bool(self._unopened[y][x]):
            return

        self._unopened[y][x] = False
        if self._mf.cell_at(x, y) == CellState.MINE:
            self.gamestate = GameState.LOST

    def _reveal_3x3(self, x: int, y: int, checked: Union[index_set, None] = None) -> index_set:
        """Recursively blow open the empty caverns"""
        if checked is None:
            checked = set()

        for i, j in self._nbr_inds(x, y):
            self._unopened[j][i] = False

        # Hop to neighbouring zero cell that hasn't been checked yet
        for i, j in self._mf.get_nbr_inds_of_types(x, y, CellState.CELL_0):
            if (i, j) not in checked:
                checked.add((i, j))
                checked |= self._reveal_3x3(i, j, checked)

        return checked

    def _toggle_flag(self, x: int, y: int):
        """Toggles the flag state of an unopened cell"""
        if not self._flagged[y][x]:
            self._flagged[y][x] = True
            self._mines_left -= 1
        else:
            self._flagged[y][x] = False
            self._mines_left += 1

    def _nbr_inds(self, x: int, y: int):
        """Returns the indices of the non-wall neighbours of the given cell"""
        res = set()
        for dx, dy in product((-1, 0, 1), repeat=2):
            i = x + dx
            j = y + dy

            if -1 in (i, j) or i == self._width or j == self._height:
                continue
            else:
                res.add((i, j))
        return res

    def _check_if_won(self):
        return len(np.transpose((self._unopened).nonzero())) == self._n_mines

    def _handle_win(self):
        self.gamestate = GameState.WON
        self._flagged[:] = self._unopened[:]
        self._mines_left = 0

    def _handle_loss(self):
        pass


class MinesweeperHeadless(MinesweeperBase):
    """Runs minesweeper without an user interface"""

    def make_interaction(self, act: Interaction):
        """Makes the given action"""

        if act.action == Action.OPEN and self.gamestate in {GameState.PLAYING, GameState.NOT_STARTED}:
            all_unnopened = not np.logical_not(self._unopened).any()

            if self.gamestate == GameState.NOT_STARTED and all_unnopened:
                self.gamestate = GameState.PLAYING
                self._new_minefield(act.x, act.y)

            if not self._flagged[act.y][act.x]:
                self._open_cell(act.x, act.y)

            if self.gamestate == GameState.LOST:
                return

            if self._check_if_won():
                self._handle_win()

        elif act.action == Action.FLAG and self.gamestate == GameState.PLAYING:
            if self._unopened[act.y][act.x]:
                self._toggle_flag(act.x, act.y)

        elif act.action == Action.NEW_GAME:
            self._new_game()


class Minesweeper(MinesweeperBase):
    """Runs minesweeper with an user interface"""

    def __init__(self, width: int, height: int, n_mines: int, rnd_seed: int | None = None, save_path=""):
        """
        Args:
            width: The width of the minefield.
            height: The height of the minefield.
            n_mines: The amount of mines in the minefield.
            rnd_seed: An initial starting point for the seed used in random number generators.
            save_path: Path to a folder, where gamedata will be stored. If not provided, nothing is saved.
        """
        super().__init__(width, height, n_mines, rnd_seed)
        self._ui = None  # MinesweeperUI(width, height)
        self._ui_grid = None
        self.fps = 1  # The mini

        self._save_path = save_path

        self._interactions = Queue(maxsize=100)
        self._redraw_event = Event()

    def _new_game(self):
        super()._new_game()
        self._ui_grid = self._init_ui_grid()

    def _init_ui_grid(self) -> NDArray:
        return np.array(
            [[CellState.UNOPENED for x in range(self._width)] for y in range(self._height)],
            dtype=object,
        )

    def _save(self, act: Interaction, minefield: Union[NDArray, None] = None):
        """Saves the grid state for testing reasons"""
        if not self._save_path:
            return

        if minefield is not None:
            with open(os.path.join(self._save_path, f"minefield.npy"), "ab") as f:
                np.save(f, minefield)
            return

        with open(os.path.join(self._save_path, f"acts.txt"), "a") as f:
            f.write(";".join([str(act.x), str(act.y), str(act.action.value)]) + "\n")

        with open(os.path.join(self._save_path, f"states.npy"), "ab") as f:
            np.save(f, self._unopened)
            np.save(f, self._flagged)

    def _get_interaction(self):
        """Returns the next action to take"""
        return self._ui.get_interaction()  # type: ignore

    def run(self):
        """Starts the game"""

        # Run the ui in a separate thread
        t = Thread(target=self._update_ui, daemon=False)
        t.start()

        self._run()

    def _update_ui(self):
        """Updates the ui"""
        self._ui = MinesweeperUI(self._width, self._height)
        self._ui_grid = self._init_ui_grid()

        while True:
            act = self._get_interaction()
            if act is not None:
                self._interactions.put(act)
                if act.action == Action.EXIT:
                    break
            self._ui.draw_frame(self._ui_grid, self.gamestate, self._mines_left)
            self._redraw_event.wait(timeout=1 / self.fps)
            self._redraw_event.clear()

    def _run(self):
        """The gameloop"""

        minefield = None

        while True:
            act = self._interactions.get()

            if act.action == Action.EXIT:
                break

            if self.gamestate == GameState.LOST and act.action != Action.NEW_GAME:
                continue

            if act.action == Action.OPEN and self.gamestate != GameState.LOST:
                all_unnopened = not np.logical_not(self._unopened).any()

                if self.gamestate == GameState.NOT_STARTED and all_unnopened:
                    self.gamestate = GameState.PLAYING
                    self._new_minefield(act.x, act.y)
                    minefield = self.get_grid()
                    self._save(act, minefield)

                elif self._flagged[act.y][act.x]:
                    continue

                self._open_cell(act.x, act.y)

                if self._check_if_won():
                    self._handle_win()
                elif self.gamestate == GameState.LOST:
                    self._handle_loss()

            elif act.action == Action.FLAG and self.gamestate == GameState.PLAYING:
                if self._unopened[act.y][act.x]:
                    self._toggle_flag(act.x, act.y)

            elif act.action == Action.NEW_GAME:
                self._new_game()

            else:
                continue

            self._save(act)

            self._ui_grid = np.where(self._unopened, CellState.UNOPENED, minefield)  # type: ignore
            self._ui_grid = np.where(self._flagged, CellState.FLAG, self._ui_grid)  # type: ignore

            self._redraw_event.set()
