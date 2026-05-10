import pygame
from src.gui.colors import *
from src.gui.constants import *

class Slider:
    def __init__(self, x, y, width, min_value, max_value, initial_value, callback=None):
        self.x = x
        self.y = y
        self.width = width
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.callback = callback
        self.dragging = False
        self.track_rect = pygame.Rect(x, y, width, 6)
        self.knob_radius = 10
        self.font = pygame.font.SysFont(FONT_FAMILY, 16, bold=FONT_BOLD)

    def get_ratio(self):
        return ((self.value - self.min_value)/(self.max_value - self.min_value))

    def get_knob_x(self):
        return self.x + int(self.get_ratio() * self.width)
    
    def handle_event(self, event):
        knob_x = self.get_knob_x()
        knob_rect = pygame.Rect(
            knob_x - self.knob_radius,
            self.y - self.knob_radius,
            self.knob_radius * 2,
            self.knob_radius * 2
        )

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if knob_rect.collidepoint(event.pos):
                    self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x = event.pos[0]
                mouse_x = max(self.x, mouse_x)
                mouse_x = min(self.x + self.width, mouse_x)

                ratio = (mouse_x - self.x) / self.width

                self.value = (
                    self.min_value
                    + ratio * (self.max_value - self.min_value)
                )

                if self.callback:
                    self.callback(self.value)

    def draw(self, screen):
        pygame.draw.rect(screen, PANEL_LIGHT, self.track_rect, border_radius=4)
        filled_rect = pygame.Rect(self.x, self.y, self.get_knob_x() - self.x, 6)
        pygame.draw.rect(screen, ACCENT, filled_rect, border_radius=4)
        pygame.draw.circle(screen, ACCENT_HOVER, (self.get_knob_x(), self.y + 3), self.knob_radius)
        value_surface = self.font.render(f'{int(self.value)} ms', True, TEXT)
        screen.blit(value_surface, (self.x, self.y - 20))