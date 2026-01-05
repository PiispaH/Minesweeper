from itertools import product
from typing import Set, Tuple
import numpy as np
from numpy.typing import NDArray
from minesweeper.utils import CellState


class MineField:
    def __init__(self, width: int, height: int, n_mines: int):
        self._width = width
        self._n_mines = n_mines
        self._height = height

        self._mf: NDArray

    def get_minefield(self) -> NDArray:
        return self._mf

    def _in_bounds_check(self, x: int, y: int):
        if x < 0 or y < 0 or y >= self._height or x >= self._width:
            raise ValueError(f"Out of bounds: x={x}, y={y}.")

    def new_minefield(self, x: int, y: int):
        self._in_bounds_check(x, y)
        self._init_grid()
        self._mine_randomizer(x, y)
        self._define_cell_values()

    def _init_grid(self):
        """Creates new minefield with walls around it"""
        self._mf = np.array([[CellState.UNOPENED for x in range(self._width)] for y in range(self._height)])
        self._mf = np.insert(self._mf, self._width, CellState.WALL, axis=1)  # type: ignore
        self._mf = np.insert(self._mf, 0, CellState.WALL, axis=1)  # type: ignore
        self._mf = np.insert(self._mf, self._height, CellState.WALL, axis=0)  # type: ignore
        self._mf = np.insert(self._mf, 0, CellState.WALL, axis=0)  # type: ignore

    def _cell_at(self, x: int, y: int) -> CellState:
        """Returns the cell at the given coordinates"""
        self._in_bounds_check(x, y)
        return self._mf[y + 1][x + 1]

    def print_mf(self):
        print()
        with np.printoptions(linewidth=200):
            print(self._mf)
        print()

    def _mine_randomizer(self, x_: int, y_: int):
        """Inserts mines randomly to the minefield."""
        self._in_bounds_check(x_, y_)

        valid_coordinates = [(x, y) for x, y in product(range(self._width), range(self._height))]

        # Keep a 3x3 clear around the start
        for dx, dy in product((-1, 0, 1), repeat=2):
            i = x_ + dx
            j = y_ + dy

            if -1 in (i, j) or i == self._width or j == self._height:
                continue
            else:
                valid_coordinates.remove((i, j))

        for ind in np.random.choice(len(valid_coordinates), self._n_mines, replace=False):
            self._mf[valid_coordinates[ind][1] + 1][valid_coordinates[ind][0] + 1] = CellState.MINE

    def _define_cell_values(self):
        """Defines the correct state for each cell"""
        for j in range(self._height):
            for i in range(self._width):
                if self._cell_at(i, j) != CellState.MINE:
                    mines_near = len(self._get_nbr_inds_of_types(i, j, CellState.MINE))
                    self._mf[j + 1][i + 1] = CellState.by_mine_amount(mines_near)

    def _get_nbr_inds_of_types(self, x: int, y: int, celltype: CellState) -> Set[Tuple[int, int]]:
        """Returns a set of the neighbouring indices with the given celltype"""
        self._in_bounds_check(x, y)
        inds: Set[Tuple[int, int]] = set()
        for dy, row in enumerate(self._neighbours(x, y), start=-1):
            for dx, nbr in enumerate(row, start=-1):
                if (dy == dx == 0) or (nbr != celltype):
                    continue
                inds.add((x + dx, y + dy))
        return inds

    def _neighbours(self, x: int, y: int) -> NDArray:
        """Returns a 3x3 matrix of the neighbours surrounding the given cell."""
        self._in_bounds_check(x, y)
        nbs = np.empty((3, 3), dtype=object)
        for dx, dy in product((-1, 0, 1), repeat=2):
            i = x + dx
            j = y + dy

            if -1 in (i, j) or i == self._width or j == self._height:
                value = CellState.WALL
            else:
                value = self._cell_at(i, j)

            nbs[dy + 1][dx + 1] = value

        return nbs
