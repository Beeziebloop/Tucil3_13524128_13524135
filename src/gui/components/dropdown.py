import pygame
from src.gui.colors import *
from src.gui.constants import *

class Dropdown:
    def __init__(self, x, y, width, height, options, default_index=0, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_index = default_index
        self.callback = callback
        self.expanded = False
        self.hovered_index = -1
        self.enabled = True
        self.font = pygame.font.SysFont(FONT_FAMILY, 18, bold=FONT_BOLD)

    @property
    def selected(self):
        return self.options[self.selected_index]

    def set_enabled(self, enabled):
        self.enabled = enabled

    def handle_event(self, event):
        if not self.enabled:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                return

            # klik main box
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                return

            # klik option
            if self.expanded:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y + (i + 1) * self.rect.height,
                        self.rect.width,
                        self.rect.height
                    )

                    if option_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.expanded = False
                        if self.callback:
                            self.callback(option)
                        return

                self.expanded = False

        elif event.type == pygame.MOUSEMOTION:
            self.hovered_index = -1
            if self.expanded:
                for i in range(len(self.options)):
                    option_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y + (i + 1) * self.rect.height,
                        self.rect.width,
                        self.rect.height
                    )

                    if option_rect.collidepoint(event.pos):
                        self.hovered_index = i
                        break

    def draw(self, screen):
        base_color = PANEL_LIGHT if self.enabled else PANEL
        pygame.draw.rect(screen, base_color, self.rect, border_radius=CORNER_RADIUS)
        pygame.draw.rect(screen, BORDER, self.rect, width=1, border_radius=CORNER_RADIUS)

        text_surface = self.font.render(self.selected, True, TEXT)
        screen.blit(text_surface,(self.rect.x + 12, self.rect.y + 10))

        # arrow
        arrow = '▼' if not self.expanded else '▲'
        arrow_surface = self.font.render(arrow, True, TEXT)
        arrow_rect = arrow_surface.get_rect(
            center=(
                self.rect.right - 16,
                self.rect.centery
            )
        )
        screen.blit(arrow_surface, arrow_rect)

        # expanded options
        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y + (i + 1) * self.rect.height,
                    self.rect.width,
                    self.rect.height
                )

                color = PANEL_LIGHT

                if i == self.hovered_index:
                    color = ACCENT

                pygame.draw.rect(screen, color, option_rect, border_radius=CORNER_RADIUS)
                pygame.draw.rect(screen, BORDER, option_rect, width=1, border_radius=CORNER_RADIUS)

                option_surface = self.font.render(option, True, TEXT)
                screen.blit(option_surface, (option_rect.x + 12, option_rect.y + 10))