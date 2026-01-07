import os
import unittest
import numpy as np
from numpy.typing import NDArray
from src.minesweeper.minesweeper_ import MinesweeperHeadless
from src.minesweeper.utils import Action, GameState, Interaction


class TestMinesweeperHeadlessGameplay(unittest.TestCase):
    """Tests that the headless mode gameplay is consistent with minesweeper rules"""

    def assert_arrays_equal(self, expected: NDArray, result: NDArray):
        self.assertEqual(expected.shape, result.shape)
        for j, row in enumerate(expected):
            for i, value in enumerate(row):
                self.assertEqual(value, result[j][i])

    def _get_minefield_from_file(self, folder_path: str, i: int):
        with open(os.path.join(folder_path, "minefield.npy"), "rb") as f:
            for _ in range(i):
                _ = np.load(f, allow_pickle=True)
            return np.load(f, allow_pickle=True)

    def _run_test_folder(self, folder_path: str):
        mf = MinesweeperHeadless(30, 16, 99, rnd_seed=42)

        acts = []
        with open(os.path.join(folder_path, "acts.txt"), "r") as f:
            for row in f:
                x, y, act = row.split(";")
                acts.append(Interaction(int(x), int(y), Action(int(act.strip()))))

        exp_minefield = self._get_minefield_from_file(folder_path, 0)
        game_num = 0
        with open(os.path.join(folder_path, f"states.npy"), "rb") as f:
            for i, act in enumerate(acts):

                exp_unnopened = np.load(f, allow_pickle=True)
                exp_flags = np.load(f, allow_pickle=True)

                mf.make_interaction(act)

                try:
                    self.assert_arrays_equal(exp_minefield, mf.get_grid())
                    self.assert_arrays_equal(exp_unnopened, mf._unopened)
                    self.assert_arrays_equal(exp_flags, mf._flagged)
                except AssertionError as e:
                    e.args = (*e.args, f"Action number: {i}, act = {act}")
                    raise e

                if act.action == Action.NEW_GAME:
                    if i + 1 == len(acts):
                        # If this was the last action
                        continue
                    game_num += 1
                    exp_minefield = self._get_minefield_from_file(folder_path, game_num)

    def test_gameplay_with_headless(self):
        """Replays games that atleast looked to follow all of the proper rules when they were played..."""
        # self._run_test_folder(os.path.join("tests", "resources", "session_0"))
        test_games = os.listdir(os.path.join("tests", "resources"))
        print()
        for dir in test_games:
            if not dir.startswith("session"):
                continue
            print(f"dir: {dir}")
            path = os.path.join("tests", "resources", dir)
            self._run_test_folder(path)

    def test_loss_condition(self):
        """Test that game is lost correctly"""
        mf = MinesweeperHeadless(3, 3, 7, rnd_seed=42)
        self.assertEqual(mf.gamestate, GameState.NOT_STARTED)

        mf.make_interaction(Interaction(0, 0, Action.OPEN))
        self.assertEqual(mf.gamestate, GameState.PLAYING)

        mf.make_interaction(Interaction(1, 1, Action.OPEN))
        self.assertEqual(mf.gamestate, GameState.LOST)

    def test_win_condition(self):
        """Test that game is won correctly"""
        mf = MinesweeperHeadless(3, 3, 7, rnd_seed=42)
        self.assertEqual(mf.gamestate, GameState.NOT_STARTED)

        mf.make_interaction(Interaction(0, 0, Action.OPEN))
        self.assertEqual(mf.gamestate, GameState.PLAYING)

        mf.make_interaction(Interaction(1, 0, Action.OPEN))
        self.assertEqual(mf.gamestate, GameState.WON)


class TestMinesweeperHeadless(unittest.TestCase):
    """Tests for the MinesweeperHeadless class"""

    def test_clamp_grid_specs(self):
        width = height = 9

        ms = MinesweeperHeadless(width, height, width * height)
        self.assertEqual(ms._width, width)
        self.assertEqual(ms._height, height)
        self.assertEqual(ms._n_mines, width * height - 1)

        ms = MinesweeperHeadless(width, height, 0)
        self.assertEqual(ms._width, width)
        self.assertEqual(ms._height, height)
        self.assertEqual(ms._n_mines, 0)

        ms = MinesweeperHeadless(width, height, 10)
        self.assertEqual(ms._width, width)
        self.assertEqual(ms._height, height)
        self.assertEqual(ms._n_mines, 10)
