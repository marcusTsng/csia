"""
Map code - defines functions for the map grid, walls, placement, etc.
"""

from Sprites import Sprite

# Full representation of the map as a grid - divided into individual tiles
class Grid:
    def __init__(self, width, height):
        self.grid = [[[] for _ in range(width)] for _ in range(height)]

    def build_wall(self, pos : tuple):
        # Gets a position and converts it to an empty coordinate on the grid
        x, y = pos[0] // 48, pos[1] // 48

        
        # Creates a tile at the coordinate generated above
        tile = Sprite((x * 48, y * 48), "Assets/base_tile.png")
        self.grid[x][y] = tile