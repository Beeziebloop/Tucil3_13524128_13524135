from src.gui.components.label import Label
from src.gui.components.panel import Panel
from src.gui.constants import *
from src.gui.colors import *


class StatisticsView:
    def __init__(self, app):
        self.app = app
        self.panel = Panel(20, 500, 260, 170)

    def draw(self, screen):
        self.panel.draw(screen)
        result = self.app.result

        Label(40, 510, 'STATISTICS', 24).draw(screen)

        if result is None:
            Label(40, 550, "No solution loaded.", 16, TEXT_DIM).draw(screen)
            return

        Label(40, 550, f'Path: {result["solution"]}', 16, bold=False).draw(screen)
        Label(40, 575, f'Cost: {result["cost"]}', 16, bold=False).draw(screen)
        Label(40, 600, f'Iterations: {result["iterations"]}', 16, bold=False).draw(screen)
        Label(40, 625, f'Time: {result["time_ms"]:.2f} ms', 16, bold=False).draw(screen)