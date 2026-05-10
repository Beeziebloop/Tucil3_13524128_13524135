import threading
import pygame
import tkinter as tk

from tkinter import filedialog

from src.parser.parser import parse_file

from src.gui.constants import *
from src.gui.colors import *

from src.gui.views.sidebar_view import SidebarView
from src.gui.views.board_view import BoardView
from src.gui.views.statistics_view import StatisticsView
from src.gui.views.playback_view import PlaybackView

from src.gui.services.playback_service import PlaybackService
from src.gui.services.solver_service import SolverService

from src.gui.utils.board_steps import generate_solution_steps


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption('Ice Sliding Puzzle Solver')

        self.clock = pygame.time.Clock()

        # ===== DATA =====
        self.board = None
        self.algorithm = 'UCS'
        self.heuristic = 'H1'
        self.result = None
        self.solving = False

        # ===== PLAYBACK =====
        self.playback = PlaybackService()

        # ===== VIEWS =====
        self.sidebar_view = SidebarView(self)
        self.board_view = BoardView(self)
        self.statistics_view = StatisticsView(self)
        self.playback_view = PlaybackView(self)

    # =========================================================
    # CONFIG
    # =========================================================

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

    # =========================================================
    # LOAD MAP
    # =========================================================

    def load_map(self):
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])

        root.destroy()

        if not filepath:
            return

        try:
            self.board = parse_file(filepath)
            self.result = None
            self.playback.load_steps([])
            print('Map loaded.')

        except Exception as error:
            print(error)

    # =========================================================
    # SOLVER
    # =========================================================

    def run_solver(self):
        if self.board is None:
            print('No board loaded.')
            return

        if self.solving:
            return

        self.solving = True

        solver_thread = threading.Thread(target=self.solve_thread, daemon=True)
        solver_thread.start()

    def solve_thread(self):
        try:
            result = SolverService.run(
                self.board,
                self.algorithm,
                self.heuristic
            )

            self.result = result

            if result['found']:
                steps = generate_solution_steps(self.board, result['solution'])
                self.playback.load_steps(steps)

            else:
                self.playback.load_steps([])

        except Exception as error:
            print(error)

        self.solving = False

    # =========================================================
    # EVENTS
    # =========================================================

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            self.sidebar_view.handle_event(event)
            self.playback_view.handle_event(event)

            # keyboard playback
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.playback.next_step()
                elif event.key == pygame.K_LEFT:
                    self.playback.prev_step()
                elif event.key == pygame.K_SPACE:
                    self.playback.toggle_play()

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self):
        self.playback.update()

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self):
        self.screen.fill(BACKGROUND)
        self.sidebar_view.draw(self.screen)
        self.board_view.draw(self.screen)
        self.statistics_view.draw(self.screen)
        self.playback_view.draw(self.screen)

        if self.solving:
            font = pygame.font.SysFont(FONT_FAMILY, 26, bold=FONT_BOLD)
            text_surface = font.render('Solving...', True, TEXT)
            self.screen.blit(text_surface, (520, 250))

        pygame.display.flip()

    # =========================================================
    # MAIN LOOP
    # =========================================================

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)