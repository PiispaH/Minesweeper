import unittest
import numpy as np
from numpy.typing import NDArray
from src.minesweeper.minefield import CellState, MineField

_W = CellState.WALL
_M = CellState.MINE
_0 = CellState.CELL_0
_1 = CellState.CELL_1
_2 = CellState.CELL_2
_3 = CellState.CELL_3
_4 = CellState.CELL_4
_5 = CellState.CELL_5
_6 = CellState.CELL_6
_7 = CellState.CELL_7
_8 = CellState.CELL_8


class TestCellState(unittest.TestCase):
    """Tests for the CellState class"""

    def test_cellstate(self):
        self.assertEqual(_0, CellState.by_mine_amount(0))
        self.assertEqual(_1, CellState.by_mine_amount(1))
        self.assertEqual(_2, CellState.by_mine_amount(2))
        self.assertEqual(_3, CellState.by_mine_amount(3))
        self.assertEqual(_4, CellState.by_mine_amount(4))
        self.assertEqual(_5, CellState.by_mine_amount(5))
        self.assertEqual(_6, CellState.by_mine_amount(6))
        self.assertEqual(_7, CellState.by_mine_amount(7))
        self.assertEqual(_8, CellState.by_mine_amount(8))
        self.assertRaises(ValueError, lambda: CellState.by_mine_amount(9))


class TestMinesField(unittest.TestCase):
    """Tests for the MineField class"""

    def assert_arrays_equal(self, expected: NDArray, result: NDArray):
        self.assertEqual(expected.shape, result.shape)
        for j, row in enumerate(expected):
            for i, value in enumerate(row):
                self.assertEqual(value, result[j][i])

    def test_neighbours(self):
        np.random.seed(41)
        mf = MineField(6, 4, 4, 0, 0)

        nbs = mf._neighbours(0, 0)
        res = np.array(
            [
                [_W, _W, _W],
                [_W, _0, _0],
                [_W, _0, _1],
            ]
        )
        self.assert_arrays_equal(nbs, res)

        nbs = mf._neighbours(5, 3)
        res = np.array(
            [
                [_M, _1, _W],
                [_3, _1, _W],
                [_W, _W, _W],
            ]
        )
        self.assert_arrays_equal(nbs, res)

    def test_define_cell_values(self):
        np.random.seed(41)
        mf = MineField(6, 4, 4, 0, 0)

        expected = np.array(
            [
                [_W, _W, _W, _W, _W, _W, _W, _W],
                [_W, _0, _0, _0, _0, _0, _0, _W],
                [_W, _0, _1, _2, _3, _2, _1, _W],
                [_W, _0, _1, _M, _M, _M, _1, _W],
                [_W, _0, _1, _3, _M, _3, _1, _W],
                [_W, _W, _W, _W, _W, _W, _W, _W],
            ]
        )
        self.assert_arrays_equal(expected, mf._mf)

    def test_new_minefield_many_mines(self):
        """Tests that the minefield is generated correctly when there are a bit too many mines"""
        np.random.seed(42)
        mf = MineField(5, 5, 5 * 5, 2, 2)
        expected = np.array(
            [
                [_W, _W, _W, _W, _W, _W, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _M, _M, _8, _M, _M, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _W, _W, _W, _W, _W, _W],
            ]
        )
        self.assert_arrays_equal(expected, mf.get_minefield())

        np.random.seed(42)
        mf = MineField(5, 5, 5 * 5, 0, 0)
        expected = np.array(
            [
                [_W, _W, _W, _W, _W, _W, _W],
                [_W, _3, _M, _M, _M, _M, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _W, _W, _W, _W, _W, _W],
            ]
        )
        self.assert_arrays_equal(expected, mf.get_minefield())

        np.random.seed(42)
        mf = MineField(5, 5, 5 * 5 - 9, 2, 2)
        expected = np.array(
            [
                [_W, _W, _W, _W, _W, _W, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _M, _5, _3, _5, _M, _W],
                [_W, _M, _3, _0, _3, _M, _W],
                [_W, _M, _5, _3, _5, _M, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _W, _W, _W, _W, _W, _W],
            ]
        )
        self.assert_arrays_equal(expected, mf.get_minefield())

        np.random.seed(42)
        mf = MineField(5, 5, 5 * 5 - 8, 2, 2)
        expected = np.array(
            [
                [_W, _W, _W, _W, _W, _W, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _M, _5, _3, _5, _M, _W],
                [_W, _M, _4, _1, _3, _M, _W],
                [_W, _M, _M, _4, _5, _M, _W],
                [_W, _M, _M, _M, _M, _M, _W],
                [_W, _W, _W, _W, _W, _W, _W],
            ]
        )
        self.assert_arrays_equal(expected, mf.get_minefield())
