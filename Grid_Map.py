"""
Map code - defines functions for the map grid, walls, placement, etc.
"""

from Sprites import Sprite
from GameManager import Game

# Full representation of the map as a grid - divided into individual tiles
class Grid:
    def __init__(self, width, height):
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def build_wall(self, pos : tuple):
        # Gets a position and converts it to an empty coordinate on the grid
        x, y = pos[0] // 48, pos[1] // 48
        
        if self.grid[x][y]: # Delete the tile if the tile is taken
            self.destroy(x,y)
        else: # Creates a tile at the coordinate generated above
            tile = Sprite((x * 48, y * 48), "Assets/base_tile.png")
            if tile.rect.colliderect(Game.get_instance().player.rect): 
                # Destroy the tile if touching the player. Prevents placement of tiles over the player.
                tile.destroy()
            else:
                self.grid[x][y] = tile

    def destroy(self, x, y): # Deletes a tile from the grid
        self.grid[x][y].destroy()
        self.grid[x][y] = None


class NavigationQueue:
    def __init__(self):
        points = []