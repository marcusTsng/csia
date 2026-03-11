"""
Handles all the user interface and overlays, including health bars, countdowns, etc. 
"""

#Imports
import pygame
from Sprites import Sprite
from GameManager import Game

# Constants
DEFAULT_FONT_NAME = "Arial"


class TextOverlay(Sprite): #Any text overlays onto the screen, like the countdown
    def __init__(self, position : tuple, text : str,  size : int, color : tuple, font_name : str = DEFAULT_FONT_NAME):
        super().__init__(position, overlay=True)

        self._game = Game.get_instance()

        self._text = text
        self._size = size
        self._color = color
        self._font = pygame.font.SysFont(font_name, size)
        self._update_surface()

    def _update_surface(self): 
        # Updates the surface attribute and centres the text
        self._surface = self._font.render(self._text, True, self._color)
        self._rect = self._surface.get_rect()
        self._rect.center = self._position

    def set_text(self, text : str): 
        self._text = text
        self._update_surface()
    def set_size(self, size : int): 
        self._size = size
        self._update_surface()
    def get_text(self): return self._text
    def get_size(self): return self._size

    def set_pos(self, pos : tuple): self.pos = pos
    def get_pos(self): return self.pos

    def _display(self): 
        Game.screen.blit(self._surface, self._rect)