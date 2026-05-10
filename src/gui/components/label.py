import pygame
from src.gui.colors import *
from src.gui.constants import *

class Label:
    def __init__(self, x, y, text, font_size=20, color=TEXT, bold=True):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(FONT_FAMILY,font_size, bold=bold)

    def set_text(self, text):
        self.text = text

    def draw(self, screen):
        surface = self.font.render(self.text, True, self.color)
        screen.blit(surface, (self.x, self.y))