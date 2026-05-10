import pygame
from src.gui.colors import *
from src.gui.constants import *

class Button:
    def __init__(self, x, y, width, height, text, callback, font_size=20, enabled=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.enabled = enabled
        self.hovered = False
        self.font = pygame.font.SysFont(FONT_FAMILY,font_size, bold=FONT_BOLD)

    def handle_event(self, event):
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.callback()

    def draw(self, screen):
        if not self.enabled:
            color = PANEL_LIGHT
        elif self.hovered:
            color = ACCENT_HOVER
        else:
            color = ACCENT

        pygame.draw.rect(screen, color, self.rect, border_radius=CORNER_RADIUS)
        text_surface = self.font.render(self.text, True, TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)