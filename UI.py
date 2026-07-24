"""
Handles all the user interface and overlays, including health bars, countdowns, etc. 
"""

#Imports
import pygame
from Sprites import Sprite, abs_asset_path
from GameManager import Game

# Constants
DEFAULT_FONT_NAME = abs_asset_path("Assets/Fonts/determination/determination.ttf")
TITLE_FONT_NAME = abs_asset_path("Assets/Fonts/alagard.ttf")


class TextOverlay(Sprite): #Any text overlays onto the screen, like the countdown
    def __init__(self, position : tuple, text : str,  size : int, color : tuple, font_name : str = DEFAULT_FONT_NAME, appear_on_game_over=False):
        super().__init__(position, overlay=True, appear_on_game_over=appear_on_game_over)

        self._game = Game.get_instance()

        self._text = text
        self._size = size
        self._color = color
        self._font = pygame.font.Font(font_name, size)
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

class Button(TextOverlay):
    def __init__(self, position, text, size, color, font_name = DEFAULT_FONT_NAME, bg = None, hover_bg = None, hover_color = None, appear_on_game_over=False):

        # Set defaults for hover colors
        if hover_bg == None: hover_bg = bg
        if hover_color == None: hover_color = color

        self._bg_color = bg
        self._hover_bg_color = hover_bg
        self._hover_color = hover_color

        super().__init__(position, text, size, color, font_name, appear_on_game_over=appear_on_game_over)
        self._update_surface()
    
    def _update_surface(self): 
        self._surface = self._font.render(self._text, True, self._color, self._bg_color)
        self._rect = self._surface.get_rect()
        self._rect.center = self._position

        if self._is_hovering(): # Override visuals for hovering
            self._surface = self._font.render(self._text, True, self._hover_color, self._hover_bg_color)
            self._rect = self._surface.get_rect()
            self._rect.center = self._position

    def _is_hovering(self): # Check whether the mouse is hovering over the button
        return self._rect.collidepoint(pygame.mouse.get_pos())
    
    def _is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                return True
        return False
    
    def _display(self): 
        self._update_surface()
        super()._display()