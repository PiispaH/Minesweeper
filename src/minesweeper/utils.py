from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class CellState(Enum):
    """Enumeration for the cell states of the minefield"""

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
        match self:
            case CellState.UNOPENED:
                s = "_U"
            case CellState.MINE:
                s = "_M"
            case CellState.FLAG:
                s = "_F"
            case CellState.MINEDEATH:
                s = "MD"
            case CellState.MISFLAG_MINE:
                s = "OH"
            case CellState.WALL:
                s = "_W"
            case _:
                s = f"_{self.num()}"
        return s

    def __str__(self) -> str:
        return f"{self.name}"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, CellState):
            return self.num() == value.num()
        return self.num() == value

    def num(self) -> int:
        return [i.value for i in CellState].index(self.value)

    @classmethod
    def by_mine_amount(cls, value: int) -> CellState:
        return CellState(f"square open{value}")


class Action(Enum):
    """Enumeration for the possible actions to make in the game"""

    OPEN = 0
    EXIT = 1
    FLAG = 2
    NEW_GAME = 3
    SAVE = 4


@dataclass
class Interaction:
    """Represents an interaction with the game"""

    x: int
    y: int
    action: Action


class GameState(Enum):
    """Enumeration fo the possible states of the game"""

    NOT_STARTED = 0
    PLAYING = 1
    LOST = 2
    WON = 3
