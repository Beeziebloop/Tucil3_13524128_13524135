import pygame
from src.gui.components.button import Button
from src.gui.components.dropdown import Dropdown
from src.gui.components.label import Label
from src.gui.components.panel import Panel
from src.gui.constants import *
from src.gui.colors import *


class SidebarView:
    def __init__(self, app):
        self.app = app
        self.width = 300
        self.panel = Panel(0, 0, self.width, WINDOW_HEIGHT, color=SIDEBAR)
        self.components = []
        self.build()

    def build(self):
        self.components.clear()

        y = 30
        title = Label(30, y, "Ice Sliding Solver", font_size=28)
        self.components.append(title)

        y += 70
        load_button = Button(30, y, 240, 45, "LOAD MAP", self.app.load_map)
        self.components.append(load_button)

        y += 80
        algo_label = Label( 30, y, "Algorithm", font_size=18)
        self.components.append(algo_label)

        y += 30
        algo_dropdown = Dropdown(30, y, 240, 42, ['UCS', 'GBFS', 'A*'], callback=self.app.set_algorithm)
        self.components.append(algo_dropdown)
        self.algo_dropdown = algo_dropdown

        y += 80
        heuristic_label = Label(30, y, "Heuristic", font_size=18)
        self.components.append(heuristic_label)

        y += 30
        heuristic_dropdown = Dropdown( 30, y, 240, 42, ['H1', 'H2', 'H3'], callback=self.app.set_heuristic)
        self.components.append(heuristic_dropdown)
        self.heuristic_dropdown = heuristic_dropdown

        y += 90
        solve_button = Button(30, y, 240, 50, "RUN SOLVER", self.app.run_solver)
        self.components.append(solve_button)

    def handle_event(self, event):
        for component in self.components:
            if hasattr(component, 'handle_event'):
                component.handle_event(event)

    def draw(self, screen):
        self.panel.draw(screen)
        expanded_dropdown = None

        # draw semua selain dropdown expanded
        for component in self.components:
            if isinstance(component, Dropdown):
                if component.expanded:
                    expanded_dropdown = component
                    continue
            component.draw(screen)

        # draw dropdown expanded paling akhir
        if expanded_dropdown:
            expanded_dropdown.draw(screen)