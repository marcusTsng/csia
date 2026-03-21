"""
This script manages the main game loop, importing managers from the GameManager script and utilising the manager classes. 
Handles the main logic of the game, feeding inputs into managers. 
"""

# Imports
import pygame
from GameManager import Game
from Sprites import Player, Sprite, Enemy
from UI import TextOverlay
from Grid_Map import Grid

# Constants
GRID_SIZE = 15

if __name__ == "__main__":
    # Initialisation and setup
    pygame.init()
    pygame.display.set_caption("Computer Science IA: Pathfinding Game")

    grid = Grid(GRID_SIZE,GRID_SIZE)
    game_manager = Game(grid)

    # Sprite Setup
    player = Player()
    timer_ui = TextOverlay(
        (game_manager.screen_width / 2, 50), 
        "0", 
        50, 
        (255,255,255)
    )

    # TESTING, REMOVE LATER!!!
    for _ in range(5): Enemy.spawn_enemy()

    # Main Game Loop
    running = True
    while running:
        # Event handling
        game_manager.tick()
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
        Enemy.move_enemies()
        timer_ui.set_text(str(game_manager.in_game_timer))
        Sprite.display_all_sprites()

        # Other
        pygame.display.flip()
    pygame.quit()