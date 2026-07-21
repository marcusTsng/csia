"""
This script manages the main game loop, importing managers from the GameManager script and utilising the manager classes. 
Handles the main logic of the game, feeding inputs into managers. 
"""

# Imports
import pygame
from GameManager import Game, GRID_SIZE
from Sprites import Player, Sprite, Enemy
from UI import TextOverlay, Button
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

    # User interface
    timer_ui = TextOverlay(
        (game_manager.screen_width / 2, 80), 
        "0", 
        20, 
        (255,255,255)
    )
    ingame_ui = TextOverlay(
        (120, game_manager.screen_height - 50), 
        f"Health: {player.health}%\nMoney: $100", 
        30,
        (255,255,255)
    )
    wave_count_ui = TextOverlay(
        (game_manager.screen_width / 2, 50), 
        f"INTERMISSION", 
        50,
        (255,255,255)
    )
    
    # Game over interface
    game_over_text = TextOverlay((game_manager.screen_width / 2,250), "GAME OVER", 80, (255,0,0), appear_on_game_over=True)
    restart_button = Button((game_manager.screen_width / 2, 350), "RESTART", 50, (0,0,0), bg=(255,255,255), hover_bg=(150,150,150), appear_on_game_over=True)
    quit_button = Button((game_manager.screen_width / 2, 420), "QUIT", 60, (0,0,0), bg=(255,255,255), hover_bg=(150,150,150), appear_on_game_over=True)

    # Main Game Loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False # Closing application; breaking out of game loop
            if event.type == pygame.MOUSEBUTTONDOWN: # Click handling
                if game_manager.state == "Build":
                    grid.build_wall(pygame.mouse.get_pos()) # Placing down walls at the mouse position
                elif game_manager.state == "None":
                    # Handling game over buttons
                    if quit_button._is_clicked(event):
                        print("Quitting application...")
                        pygame.quit()
                        print("Application quit successfully\n\n")
                    if restart_button._is_clicked(event):
                        player.health = 100
                        game_manager.respawn()
        
        if game_manager.state != "None": # Only run the following while the game is active
            game_manager.tick()

            # Managing player health/death            
            if player.health <= 0:
                player.health = 0
                game_manager.game_over()
            ingame_ui.set_text(f"Health: {player.health}%\nMoney: ${game_manager.money}")

            # Managing wave ui
            if game_manager.state == "Wave":
                wave_count_ui.set_text(f"WAVE {game_manager.wave_counter}") # Displays the current wave
            else: wave_count_ui.set_text("INTERMISSION")

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
            Enemy.move_enemies()

            # In game display
            timer_ui.set_text(str(game_manager.in_game_timer))

        # Sprite handling/display
        Game.screen.fill((10,10,10))
        Sprite.display_all_sprites()
        pygame.display.flip()
    pygame.quit()