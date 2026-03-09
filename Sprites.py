"""
Handles the classes that define sprites
"""

import pygame
import time
from GameManager import Game

# General class for sprites
class Sprite:
    SPRITES = []
    def __init__(self, position : tuple, image_path : str):
        self._game = Game.get_instance() # For easy reference later

        self._position = position
        self._image = Sprite.load_image(image_path)

        self.rect = self._image.get_rect()
        self.rect.topleft = position

        Sprite.SPRITES.append(self)
    
    def get_pos(self): return self._position[0], self._position[1]
    def set_pos(self, position : tuple): 
        self._position = position
        self.rect.topleft = position

    def move(self, position : tuple): # Shift the sprite by a tuple position
        self._position = (self._position[0] + position[0] * self._game.delta_time, self._position[1] + position[1] * self._game.delta_time)
        self.rect.topleft = self._position

    def _display(self): # Display the sprite on the screen. Called by the display_all_sprites() static method
        Game.screen.blit(self._image, self._position)

    def destroy(self): # Deletes a sprite from existence 
        Sprite.SPRITES.remove(self)

    @staticmethod
    def display_all_sprites():
        for x in Sprite.SPRITES:
            x._display()

    @staticmethod 
    def load_image(image_path):
        # For loading images. Loads image from the relative path and scales to fit the screen
        base = pygame.image.load(image_path)
        return pygame.transform.scale_by(base, 3)

# Player sprite, inherits from Sprite
class Player(Sprite):
    def __init__(self):
        super().__init__((0,0), "Assets/Player/player_Idle.png")
        self.speed = 20

        # For walk animations
        self._walking = False
        self._last_frame = 0 
        self._current_frame_i = 1

        # Animation loading
        self._walk1 = Sprite.load_image("Assets/Player/player_Walk1.png")
        self._walk2 = Sprite.load_image("Assets/Player/player_Walk2.png")

    def move(self, position): # For player movement
        self._walking = True
        old_pos = self._position # Stores the old position 
        
        super().move(position)

        # Clamp positions so player does not leave the map
        self._position = (pygame.math.clamp(self._position[0], 0, self._game.screen_width - 48), pygame.math.clamp(self._position[1], 0, self._game.screen_height - 48))

        for x in self._game.grid.grid:
            for tile in x: 
                if isinstance(tile, Sprite) and self.rect.colliderect(tile.rect): 
                    self._position = old_pos # Revert to old position if a collision is detected
                    return
                
    def _display(self): # Overrides display to allow walk animations
        if self._walking: # Walk animation
            self._walking = False
            if self._game.time - self._last_frame >= 0.1: # Every 0.1 secs
                self._last_frame = self._game.time
                self._current_frame_i = 1 if self._current_frame_i == 2 else 2
            if self._current_frame_i == 1: Game.screen.blit(self._walk1, self._position)
            else: Game.screen.blit(self._walk2, self._position)
        else:
            Game.screen.blit(self._image, self._position)


class Enemy(Sprite):
    def __init__(self, position):
        super().__init__(position, "Assets/placeholder.png")

        