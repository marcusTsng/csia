"""
Map code - defines functions for the map grid, walls, placement, etc.
"""

from Sprites import Sprite, abs_asset_path
from Navigator import Navigator
from GameManager import Game

import random

# Full representation of the map as a grid - divided into individual tiles
class Grid:
    def __init__(self, game_manager, width, height, grid = None):
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        # Populate the grid if one has been saved
        if grid:
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    # Grid is saved as 2D array of 1s and 0s, load tiles onto 1s
                    if grid[j][i] == 1 and not (i == j == 7):  # Ignore centre tile, as that is where the player spawns
                        tile = Sprite((j * 48, i * 48), "Assets/wall_tile.png")
                        self.grid[j][i] = tile

        # other setup
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
            tile = Sprite((x * 48, y * 48), abs_asset_path("Assets/wall_tile.png"))
            if tile.rect.colliderect(Game.get_instance().player.rect) or (x == 0 or x == 14 or y == 0 or y == 14) or not self.game_manager.purchase(10): 
                # Destroy the tile if touching the player, or the player cannot afford to build a wall, or if the tile is on the edge
                tile.destroy()
            else:
                self.grid[x][y] = tile

        # Update navigators
        Navigator.update_all_navs()

    def is_empty(self): # Returns True if the grid is empty
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[j][i] != None: return False
        return True

    def destroy(self, x, y): # Deletes a tile from the grid
        if self.grid[x][y] != None:
            self.grid[x][y].destroy()
            self.grid[x][y] = None
            return True
        return False
    
    def reset(self): # Reset the grid
        for y in range(self.height):
            for x in range(self.width):
                self.destroy(x, y)