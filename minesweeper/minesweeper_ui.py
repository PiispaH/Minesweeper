import os
from typing import Tuple, Union
from numpy.typing import NDArray
from minesweeper.utils import Interaction, UIAction, GameState

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # Silence the stupid pygame import print...
import pygame


class MinesweeperUI:
    def __init__(self, width: int, height: int):
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        files = sorted(os.listdir(os.path.join("images")))
        self._images = {name.split(".")[0]: pygame.image.load(os.path.join("images", name)) for name in files}
        self._font_small = pygame.font.SysFont("Nunito", 30)
        self._font_big = pygame.font.SysFont("Nunito", 100)

        self._block_size = self._images[str(0)].get_height()

        self._sreen_width = (width + 2) * self._block_size
        self._screen_height = (height + 3) * self._block_size
        self._click_location = (-1, -1)
        self._grid_size_px = (width * self._block_size, height * self._block_size)

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

    def draw_frame(self, grid: NDArray, gamestate: GameState) -> Union[Interaction, None]:
        """Draws one frame with the given grid"""

        self._screen.fill((10, 0, 0))
        grid_fill = (self._block_size, 2 * self._block_size, *self._grid_size_px)
        self._screen.fill((132, 132, 132), grid_fill)
        instructions_esc = self._font_small.render("Quit the game: esc", True, (19, 120, 161))
        instructions_space = self._font_small.render("New game: space", True, (19, 120, 161))
        self._screen.blit(instructions_esc, (10, 0))
        self._screen.blit(instructions_space, (10, self._block_size))

        if gamestate == GameState.LOST:
            lost_text = self._font_big.render("GAME OVER", True, (160, 20, 20))
            self._screen.blit(lost_text, ((self._sreen_width - lost_text.get_width()) // 2, 0))
        if gamestate == GameState.WON:
            lost_text = self._font_big.render("WIN", True, (19, 161, 69))
            self._screen.blit(lost_text, ((self._sreen_width - lost_text.get_width()) // 2, 0))

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
