"""
This script manages the main game loop, importing managers from the GameManager script and utilising the manager classes. 
Handles the main logic of the game, feeding inputs into managers. 
"""

GRID_SIZE = 15

# Imports
import pygame
from GameManager import Game
from Sprites import Player, Sprite, Enemy
from UI import TextOverlay
from Grid_Map import Grid

if __name__ == "__main__":
    # Initialisation and setup
    pygame.init()
    pygame.display.set_caption("Computer Science IA: Pathfinding Game")

    game_manager = Game()
    grid = Grid(game_manager, GRID_SIZE,GRID_SIZE)
    player = Player(game_manager)

    game_manager.grid = grid
    game_manager.player = player

    timer_ui = TextOverlay(
        (game_manager.screen_width / 2, 50), 
        "0", 
        50, 
        (255,255,255)
    )

    # Main Game Loop
    running = True
    while running:
        # Event handling
        game_manager.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False # Closing application; breaking out of game loop
            if event.type == pygame.MOUSEBUTTONDOWN: # Click handling
                if game_manager.state == "Build":
                    grid.build_wall(pygame.mouse.get_pos()) # Placing down walls at the mouse position

        # Key inputs
        keys = pygame.key.get_pressed()
        # Player movement
        if keys[pygame.K_w]: player.move((0, -player.speed))
        if keys[pygame.K_s]: player.move((0, player.speed))
        if keys[pygame.K_a]: player.move((-player.speed,0))
        if keys[pygame.K_d]: player.move((player.speed,0))

        # Spawning enemies
        if game_manager.state == "Wave" and Enemy.count_enemies() < game_manager.max_enemies:
            Enemy.spawn_enemy()

        # Sprite handling/display
        Game.screen.fill((0,0,0))
        Enemy.move_enemies()
        timer_ui.set_text(str(game_manager.in_game_timer))
        Sprite.display_all_sprites()

        # Other
        pygame.display.flip()
    pygame.quit()