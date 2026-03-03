# Imports
import pygame
from Classes import Sprite, Player

# Game Manager Singleton
class Game:
    _instance = None
    def __new__(cls): # Singleton pattern 
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    @staticmethod 
    def get_instance():
        if Game._instance: return Game._instance
        else: return Game()

# Input Manager Singleton
class InputManager:
    _instance = None
    def __new__(cls): # Singleton pattern 
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Initialisation 
            cls._instance._mouse_down = False
        return cls._instance
    
    def set_mouse_down(self, input):
        pass



if __name__ == "__main__":
    # Initialisation and setup
    pygame.init()
    game_manager = Game()
    input_manager = InputManager()

    # Sprite Setup
    player = Player("Assets/placeholder.png")


    # Main Game Loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False # Closing application; breaking out of game loop

        # Key inputs
            if event.type == pygame.KEYDOWN:
                # Movement
                x, y = player.get_pos()
                if event.key == pygame.K_w: player.set_pos((x, y + 10))

        
        # Logic handling

        # Sprite handling/display
        # screen.fill((0,0,0))
        Sprite.display_all_sprites()

        # Other
        pygame.display.flip()
    pygame.quit()