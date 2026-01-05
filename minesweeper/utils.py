from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class CellState(Enum):
    CELL_0 = "square open0"
    CELL_1 = "square open1"
    CELL_2 = "square open2"
    CELL_3 = "square open3"
    CELL_4 = "square open4"
    CELL_5 = "square open5"
    CELL_6 = "square open6"
    CELL_7 = "square open7"
    CELL_8 = "square open8"
    UNOPENED = "square blank"
    MINE = "square bombrevealed"
    FLAG = "square bombflagged"
    MINEDEATH = "square bombdeath"
    MISFLAG_MINE = "square bombmisflagged"
    WALL = "wall"

    def __repr__(self) -> str:
        """"""
        if self == CellState.MINE:
            s = "B"
        elif self == CellState.FLAG:
            s = "F"
        else:
            s = str(self.num())
        return s

    def __str__(self) -> str:
        return f"{self.name}"

    def num(self) -> int:
        return [i.value for i in CellState].index(self.value)

    @classmethod
    def by_mine_amount(cls, value: int) -> CellState:
        return CellState(f"square open{value}")


class UIAction(Enum):
    OPEN = 0
    FLAG = 1
    EXIT = 2
    NEW_GAME = 3


@dataclass
class Interaction:
    x: int
    y: int
    action: UIAction


class GameState(Enum):
    NOT_STARTED = 0
    PLAYING = 1
    LOST = 2
    WON = 3
