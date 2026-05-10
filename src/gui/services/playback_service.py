import pygame

class PlaybackService:
    def __init__(self):
        self.current_step = 0
        self.playing = False
        self.speed_ms = 500
        self.last_update = 0
        self.steps = []

    def load_steps(self, steps):
        self.steps = steps
        self.current_step = 0
        self.playing = False

    def toggle_play(self):
        self.playing = not self.playing
        self.last_update = pygame.time.get_ticks()

    def stop(self):
        self.playing = False

    def set_speed(self, speed_ms):
        self.speed_ms = speed_ms

    def next_step(self):
        if not self.steps:
            return

        if self.current_step < len(self.steps) - 1:
            self.current_step += 1

    def prev_step(self):
        if not self.steps:
            return

        if self.current_step > 0:
            self.current_step -= 1

    def first_step(self):
        self.current_step = 0

    def last_step(self):
        if self.steps:
            self.current_step = len(self.steps) - 1

    def jump_to(self, step):
        if not self.steps:
            return

        step = max(0, step)
        step = min(step, len(self.steps) - 1)

        self.current_step = step

    def update(self):
        if not self.playing:
            return

        if not self.steps:
            return

        now = pygame.time.get_ticks()
        if now - self.last_update >= self.speed_ms:
            self.last_update = now
            if self.current_step < len(self.steps) - 1:
                self.current_step += 1
            else:
                self.playing = False

    def get_current_step(self):
        if not self.steps:
            return None
        return self.steps[self.current_step]

    def get_progress_text(self):
        if not self.steps:
            return '0 / 0'
        
        return (f'{self.current_step}'f' / 'f'{len(self.steps)-1}')