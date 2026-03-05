"""
This script manages the main game loop, importing managers from the GameManager script and utilising the manager classes. 
Handles the main logic of the game, feeding inputs into managers. 
"""

# Imports
import pygame
from GameManager import Game
from Sprites import Player, Sprite
from Grid_Map import Grid


if __name__ == "__main__":
    # Initialisation and setup
    pygame.init()
    game_manager = Game()
    grid = Grid(15,15)

    # Sprite Setup
    player = Player("Assets/base_tile.png")

    # Main Game Loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False # Closing application; breaking out of game loop
            if event.type == pygame.MOUSEBUTTONDOWN: # Click handling
                # Put a selection later
                grid.build_wall(pygame.mouse.get_pos()) # Placing down walls at the mouse position

        # Key inputs
        keys = pygame.key.get_pressed()
        # Player movement
        if keys[pygame.K_w]: player.move((0, -player.speed))
        if keys[pygame.K_s]: player.move((0, player.speed))
        if keys[pygame.K_a]: player.move((-player.speed,0))
        if keys[pygame.K_d]: player.move((player.speed,0))
        

        # Sprite handling/display
        Game.screen.fill((0,0,0))
        Sprite.display_all_sprites()

        # Other
        pygame.display.flip()
    pygame.quit()