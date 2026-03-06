"""
Handles the classes that define sprites
"""

import pygame
from GameManager import Game

# General class for sprites
class Sprite:
    SPRITES = []
    def __init__(self, position : tuple, image_path : str, scale : float = 3):
        self._position = position
        # Loading and manipulating the image - default scale up is 3
        self._base_image = pygame.image.load(image_path)
        self._image = pygame.transform.scale_by(self._base_image, scale)

        self.rect = self._image.get_rect()
        self.rect.topleft = position

        Sprite.SPRITES.append(self)
    
    def get_pos(self): return self._position[0], self._position[1]
    def set_pos(self, position : tuple): 
        self._position = position
        self.rect.topleft = position

    def move(self, position : tuple): # Shift the sprite by a tuple position
        self._position = (self._position[0] + position[0], self._position[1] + position[1])
        self.rect.topleft = self._position

    def _display(self): # Display the sprite on the screen. Called by the display_all_sprites() static method
        Game.screen.blit(self._image, self._position)

    def destroy(self): # Deletes a sprite from existence 
        Sprite.SPRITES.remove(self)

    @staticmethod
    def display_all_sprites():
        for x in Sprite.SPRITES:
            x._display()

# Player sprite, inherits from Sprite
class Player(Sprite):
    def __init__(self, image_path):
        super().__init__((0,0), image_path)
        self.speed = 1
        self._game = Game.get_instance() # For easy reference later

    def move(self, position):
        old_pos = self._position # Stores the old position 
        
        super().move(position)

        # Clamp positions so player does not leave the map
        self._position = (pygame.math.clamp(self._position[0], 0, self._game.screen_width - 48), pygame.math.clamp(self._position[1], 0, self._game.screen_height - 48))

        for x in self._game.grid.grid:
            for tile in x: 
                if isinstance(tile, Sprite) and self.rect.colliderect(tile.rect): 
                    self._position = old_pos # Revert to old position if a collision is detected
                    return