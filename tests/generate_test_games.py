import os
from minesweeper.minesweeper import Minesweeper


def main():
    num = None
    for i in range(10):
        try:
            os.mkdir(os.path.join("tests", "resources", f"session_{i}"))
            num = i
            break
        except FileExistsError:
            continue

    ms = Minesweeper(30, 16, 99, rnd_seed=42, save_path=os.path.join("tests", "resources", f"session_{num}"))
    ms.run()


if __name__ == "__main__":
    main()
