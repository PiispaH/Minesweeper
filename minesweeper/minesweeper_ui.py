import os
from typing import Tuple, Union
from numpy.typing import NDArray
from minesweeper.utils import Interaction, UIAction

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # Silence the stupid pygame import print...
import pygame


class MinesweeperUI:
    def __init__(self, width: int, height: int):
        pygame.init()

        files = sorted(os.listdir(os.path.join("images")))
        self._images = {name.split(".")[0]: pygame.image.load(os.path.join("images", name)) for name in files}
        self._font_small = pygame.font.SysFont("Nunito", 30)

        self._block_size = self._images[str(0)].get_height()

        self._sreen_width = (width + 2) * self._block_size
        self._screen_height = (height + 3) * self._block_size
        self._click_location = (-1, -1)

        self._screen = pygame.display.set_mode((self._sreen_width, self._screen_height))

    def _map_pos_to_gridpoint(self, x: int, y: int) -> Tuple[int, int]:
        """Returns the cell coordinates from pixel coordinates"""
        i = j = -1
        if (self._block_size < x < self._sreen_width - self._block_size) and (
            2 * self._block_size < y < self._screen_height - self._block_size
        ):
            i = int((x - self._block_size) / self._block_size)
            j = int((y - 2 * self._block_size) / self._block_size)

        return i, j

    def draw_frame(self, grid: NDArray) -> Union[Interaction, None]:
        """Draws one frame with the given grid"""

        self._screen.fill((10, 0, 0))
        directions_esc = self._font_small.render("Quit the game: esc", True, (160, 20, 20))
        self._screen.blit(directions_esc, (10, 0))

        for j, row in enumerate(grid):
            for i, value in enumerate(row):
                key = value.num()
                if key >= 9:
                    key = value
                self._screen.blit(self._images[str(key)], ((1 + i) * self._block_size, (2 + j) * self._block_size))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = self._map_pos_to_gridpoint(*event.pos)
                if -1 in {x, y}:
                    continue
                if event.button == 1:
                    return Interaction(x, y, UIAction.OPEN)
                elif event.button == 3:
                    return Interaction(x, y, UIAction.FLAG)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return Interaction(-1, -1, UIAction.EXIT)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return Interaction(-1, -1, UIAction.NEW_GAME)

        pygame.display.flip()
