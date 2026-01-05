import unittest
import numpy as np
import os
from numpy.typing import NDArray
from minesweeper.minesweeper import MinesweeperHeadless
from minesweeper.utils import Interaction, UIAction


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
                acts.append(Interaction(int(x), int(y), UIAction(int(act.strip()))))

        exp_minefield = self._get_minefield_from_file(folder_path, 0)
        game_num = 0
        with open(os.path.join(folder_path, f"states.npy"), "rb") as f:
            for i, act in enumerate(acts):

                exp_unnopened = np.load(f, allow_pickle=True)
                exp_flags = np.load(f, allow_pickle=True)

                grid, unnopened, flags = mf.make_interaction(act)

                try:
                    self.assert_arrays_equal(exp_minefield, grid)
                    self.assert_arrays_equal(exp_unnopened, unnopened)
                    self.assert_arrays_equal(exp_flags, flags)
                except AssertionError as e:
                    e.args = (*e.args, f"Action number: {i}, act = {act}")
                    raise e

                if act.action == UIAction.NEW_GAME:
                    if i + 1 == len(acts):
                        # If this was the last action
                        continue
                    game_num += 1
                    exp_minefield = self._get_minefield_from_file(folder_path, game_num)

    def test_gameplay_with_headless(self):
        test_games = os.listdir(os.path.join("tests", "resources"))
        print()
        for dir in test_games:
            if not dir.startswith("session"):
                continue
            print(f"dir: {dir}")
            path = os.path.join("tests", "resources", dir)
            self._run_test_folder(path)
