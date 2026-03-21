"""
Manages the manager classes, including the Game manager and the InputManager. 
These are singletons to ensure the usage of only a single object.
"""

import pygame

# Constants
TIME_BETWEEN_WAVES = 5

# Game Manager Singleton
class Game:
    _instance = None # For singleton
    _initialized = False

    # Screen setup
    screen_width, screen_height = 720,720
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Singleton pattern 
    def __new__(cls, grid):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, grid):
        if self._initialized: return # Ensures initialisation happens only once, for singleton
        self._initialized = True

        # Initialisation
        self.time = 0
        self.grid = grid
        self.player = None

        self.clock = pygame.time.Clock()
        self._start_time = pygame.time.get_ticks() # Time of initial wave
        self.delta_time = self.clock.tick()
        self.in_game_timer = TIME_BETWEEN_WAVES
        self._last_second = 0 # For checking every second
    
    def tick(self):
        self.time = (pygame.time.get_ticks() - self._start_time) / 1000
        # Delta time is time between frames, makes sure movement stays the same even in lag
        self.delta_time = self.clock.tick(60) / 100 # 60 fps cap, divide by 100 to convert to seconds

        # Calls the every_second() function whenever a second has passed
        if self.time - self._last_second >= 1:
            self._last_second = self.time
            self.every_second()

    def every_second(self): # Runs every second, called by tick()
        # Handling the in-game timer
        self.in_game_timer = TIME_BETWEEN_WAVES - int(self.time)
        if self.in_game_timer <= 0:
            self.in_game_timer = TIME_BETWEEN_WAVES
            self._start_time = self.time

    @staticmethod 
    def get_instance():
        if Game._instance: return Game._instance
        else: return Game()