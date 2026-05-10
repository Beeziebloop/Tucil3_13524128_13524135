import pygame
from src.gui.colors import *
from src.gui.constants import *

class Panel:
    def __init__(self, x, y, width, height, color=PANEL):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=CORNER_RADIUS)
        pygame.draw.rect(screen, BORDER, self.rect, width=1, border_radius=CORNER_RADIUS)