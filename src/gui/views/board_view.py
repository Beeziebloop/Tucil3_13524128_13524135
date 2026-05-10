import pygame
from src.gui.colors import *
from src.gui.constants import *

class BoardView:
    def __init__(self, app):
        self.app = app
        self.tile_size = 50

    def get_tile_color(self, tile):
        if tile == 'X':
            return WALL

        if tile == 'L':
            return DANGER

        if tile == 'O':
            return GOAL

        if tile.isdigit():
            return CHECKPOINT

        return BOARD_EMPTY

    def draw(self, screen):
        board = self.app.board

        if board is None:
            return

        rows = board.rows
        cols = board.cols

        available_width = 900
        available_height = 440

        self.tile_size = min(available_width // cols, available_height // rows)

        board_width = cols * self.tile_size
        board_height = rows * self.tile_size

        start_x = 330 + (900 - board_width) // 2
        start_y = 110 + (420 - board_height) // 2

        player_pos = (board.start.x, board.start.y)

        if (self.app.playback.steps and self.app.playback.get_current_step()):
            _, _, player_pos, _ = (self.app.playback.get_current_step())

        for row in range(rows):
            for col in range(cols):
                tile = board.grid[row][col]
                gap = 4
                rect = pygame.Rect(
                    start_x + col * self.tile_size + gap // 2,
                    start_y + row * self.tile_size + gap // 2,
                    self.tile_size - gap,
                    self.tile_size - gap
                )
                pygame.draw.rect(screen, self.get_tile_color(tile), rect, border_radius=6)
                pygame.draw.rect(screen, BORDER, rect, width=1, border_radius=6)

                if tile.isdigit():
                    font = pygame.font.SysFont(FONT_FAMILY, self.tile_size//3 , bold=FONT_BOLD)
                    text_surface = font.render(tile, True, TEXT)
                    text_rect = text_surface.get_rect(center=rect.center)
                    screen.blit(text_surface, text_rect)

                if tile != 'X' and tile != 'L':
                    cost = str(board.costs[row][col])

                    cost_font = pygame.font.SysFont(
                        FONT_FAMILY,
                        max(12, self.tile_size // 6),
                        bold=True
                    )

                    cost_surface = cost_font.render(
                        cost,
                        True,
                        TEXT_DIM
                    )

                    cost_rect = cost_surface.get_rect(
                        bottomright=(
                            rect.right - 5,
                            rect.bottom - 3
                        )
                    )

                    screen.blit(cost_surface, cost_rect)

        player_rect = pygame.Rect(
            start_x + player_pos[1] * self.tile_size,
            start_y + player_pos[0] * self.tile_size,
            self.tile_size,
            self.tile_size
        )

        pygame.draw.circle(
            screen,
            PLAYER,
            player_rect.center,
            self.tile_size // 3
        )
