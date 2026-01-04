import unittest
import numpy as np
from numpy.typing import NDArray
from minesweeper.minesweeper import Minesweeper
from minesweeper.minesweeper import CellState


class TestCellState(unittest.TestCase):
    def test_cellstate(self):
        self.assertEqual(CellState.CELL_0, CellState.by_mine_amount(0))
        self.assertEqual(CellState.CELL_1, CellState.by_mine_amount(1))
        self.assertEqual(CellState.CELL_2, CellState.by_mine_amount(2))
        self.assertEqual(CellState.CELL_3, CellState.by_mine_amount(3))
        self.assertEqual(CellState.CELL_4, CellState.by_mine_amount(4))
        self.assertEqual(CellState.CELL_5, CellState.by_mine_amount(5))
        self.assertEqual(CellState.CELL_6, CellState.by_mine_amount(6))
        self.assertEqual(CellState.CELL_7, CellState.by_mine_amount(7))
        self.assertEqual(CellState.CELL_8, CellState.by_mine_amount(8))
        self.assertRaises(ValueError, lambda: CellState.by_mine_amount(9))


class TestMinesweeper(unittest.TestCase):

    def assert_arrays_equal(self, expected: NDArray, result: NDArray):
        self.assertEqual(expected.shape, result.shape)
        for j, row in enumerate(expected):
            for i, value in enumerate(row):
                self.assertEqual(value, result[j][i])

    def test_init_mf(self):
        mf = Minesweeper(4, 5, 8)

        W = CellState.WALL
        U = CellState.UNOPENED

        expected = np.array(
            [
                [W, W, W, W, W, W],
                [W, U, U, U, U, W],
                [W, U, U, U, U, W],
                [W, U, U, U, U, W],
                [W, U, U, U, U, W],
                [W, U, U, U, U, W],
                [W, W, W, W, W, W],
            ]
        )
        self.assert_arrays_equal(expected, mf._mf)

    def test_minesweeper_mine_randomizer(self):
        np.random.seed(42)
        mf = Minesweeper(4, 5, 8)
        mf._mine_randomizer(0, 0)

        W = CellState.WALL
        U = CellState.UNOPENED
        M = CellState.MINE

        expected = np.array(
            [
                [W, W, W, W, W, W],
                [W, U, U, U, U, W],
                [W, M, M, U, U, W],
                [W, M, U, M, M, W],
                [W, U, U, U, U, W],
                [W, M, M, M, U, W],
                [W, W, W, W, W, W],
            ]
        )
        self.assert_arrays_equal(expected, mf._mf)

    def test_neighbours(self):
        np.random.seed(41)
        mf = Minesweeper(6, 4, 4)
        mf._mine_randomizer(0, 0)

        nbs = mf._neighbours(0, 0)
        res = np.array(
            [
                [CellState.WALL, CellState.WALL, CellState.WALL],
                [CellState.WALL, CellState.UNOPENED, CellState.UNOPENED],
                [CellState.WALL, CellState.UNOPENED, CellState.UNOPENED],
            ]
        )
        self.assert_arrays_equal(nbs, res)

        nbs = mf._neighbours(5, 3)
        res = np.array(
            [
                [CellState.UNOPENED, CellState.UNOPENED, CellState.WALL],
                [CellState.UNOPENED, CellState.UNOPENED, CellState.WALL],
                [CellState.WALL, CellState.WALL, CellState.WALL],
            ]
        )
        self.assert_arrays_equal(nbs, res)

    def test_define_cell_values(self):
        print()
        np.random.seed(41)
        mf = Minesweeper(6, 4, 4)
        mf._mine_randomizer(0, 0)
        mf._define_cell_values()

        _W = CellState.WALL
        _M = CellState.MINE
        _0 = CellState.CELL_0
        _1 = CellState.CELL_1
        _2 = CellState.CELL_2
        _3 = CellState.CELL_3

        expected = np.array(
            [
                [_W, _W, _W, _W, _W, _W, _W, _W],
                [_W, _0, _1, _M, _M, _1, _0, _W],
                [_W, _0, _2, _3, _3, _1, _0, _W],
                [_W, _0, _1, _M, _2, _1, _0, _W],
                [_W, _0, _1, _2, _M, _1, _0, _W],
                [_W, _W, _W, _W, _W, _W, _W, _W],
            ]
        )
        self.assert_arrays_equal(expected, mf._mf)
