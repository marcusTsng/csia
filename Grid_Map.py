"""
Map code - defines functions for the map grid, walls, placement, etc.
"""

from Sprites import Sprite
from Navigator import Navigator
from GameManager import Game

import random

# Full representation of the map as a grid - divided into individual tiles
class Grid:
    def __init__(self, game_manager, width, height):
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height

        self.game_manager = game_manager
        game_manager.grid = self 

    def get_tile_at(self, x, y):
        return self.grid[y][x]

    def get_random_tile(self):
        # Outputs a random tile on the grid, ie used for enemy placement/randomised spawning
        return self.grid[random.randint(0,self.height - 1)][random.randint(0,self.width - 1)]

    def build_wall(self, pos : tuple):
        # Gets a position and converts it to an empty coordinate on the grid
        x, y = pos[0] // 48, pos[1] // 48
        
        if self.grid[x][y]: # Delete the tile if the tile is taken
            self.game_manager.add_money(10)
            self.destroy(x,y)
        else: # Creates a tile at the coordinate generated above
            tile = Sprite((x * 48, y * 48), "Assets/wall_tile.png")
            if tile.rect.colliderect(Game.get_instance().player.rect) or not self.game_manager.purchase(10): 
                # Destroy the tile if touching the player, or the player cannot afford to build a wall
                tile.destroy()
            else:
                self.grid[x][y] = tile

        # Update navigators
        Navigator.update_all_navs()

    def destroy(self, x, y): # Deletes a tile from the grid
        self.grid[x][y].destroy()
        self.grid[x][y] = None