"""
Manages the manager classes, including the Game manager and the InputManager. 
These are singletons to ensure the usage of only a single object.
"""

import pygame

# Game Manager Singleton
class Game:
    _instance = None # For singleton
    # Screen setup
    screen_width, screen_height = 720,720
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Singleton pattern 
    def __new__(cls, grid):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.grid = grid
        return cls._instance
    @staticmethod 
    def get_instance():
        if Game._instance: return Game._instance
        else: return Game()