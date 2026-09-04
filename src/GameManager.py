"""
Manages the manager classes, including the Game manager and the InputManager. 
These are singletons to ensure the usage of only a single object.
"""

import pygame
from Datasave import get_user_data

# Constants
TIME_BETWEEN_WAVES = 30
INIT_TIME_DURING_WAVES = 20
WAVE_TIME_INCREMENT = 5
ENEMY_SPAWN_TIME = 5
GRID_SIZE = 15

# Game Manager Singleton
class Game:
    _instance = None # For singleton
    _initialized = False

    # Screen setup
    screen_width, screen_height = 720,720
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Singleton pattern 
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    # Constructor
    def __init__(self):
        if self._initialized: return # Ensures initialisation happens only once, for singleton
        self._initialized = True

        # Getting saved data
        data = get_user_data()

        # Initialisation
        self.grid = None
        self.player = None
        self.money = data["money"]
        self.high_score = data["highscore"]
        self.new_high = False # For checking whether the player has achieved a new highscore or not

        # Clock attributes
        self.clock = pygame.time.Clock()
        self.time = 0
        self._start_time = pygame.time.get_ticks() # Time of initial wave
        self.delta_time = self.clock.tick()
        self.in_game_timer = TIME_BETWEEN_WAVES
        self._last_second = 0 # For checking every second
        self.wave_counter = data["wave_no"]
        # self.extra_wave_time = 0 # For increasing the length of waves

        # Game state attributes
        self.max_enemies = 0

        self.state = "Menu"  # Can be Menu, Build, Wave, or GameOver
        self.menu = True
    
    # Accessors/Mutators
    def get_player(self): return self.player
    def get_grid(self): return self.grid
    def get_money(self): return self.money
    
    def purchase(self, amount): 
        if self.money < amount: return False
        self.money -= amount
        return True
    def add_money(self, money): self.money += money
    def set_money(self, money): self.money = money

    # Runs every frame
    def tick(self):
        
        self.time = (pygame.time.get_ticks() - self._start_time) / 1000
        # Delta time is time between frames, makes sure movement stays the same even in lag
        self.delta_time = self.clock.tick(60) / 100 # 60 fps cap, divide by 100 to convert to seconds

        # Calls the every_second() function whenever a second has passed
        if self.time - self._last_second >= 1:
            self._last_second = self.time
            self.every_second()

    # Runs every second, called by tick()
    def every_second(self): 
        # Handling the in-game timer
        self.in_game_timer -= 1
        if self.in_game_timer <= 0:
            self._start_time = self.time
            self.next_game_state()

        # Enemy spawning 
        if self.state != "Wave": 
            self.max_enemies = 0
        elif self.in_game_timer % ENEMY_SPAWN_TIME == 0: # Enemies spawn at certain time intervals
            self.max_enemies += 1

    # Switching game states between None, Build and Game
    def next_game_state(self): 
        if self.state == "Wave":
            self.add_money(100)
            self.state = "Build"
            self.in_game_timer = TIME_BETWEEN_WAVES
            self.max_enemies = 0
        elif self.state == "Menu" or self.state == "GameOver":
            self.state = "Build"
            self.in_game_timer = TIME_BETWEEN_WAVES
            self.max_enemies = 0
        elif self.state == "Build": # When switching from build to wave, increment the wave
            self.state = "Wave"
            self.wave_counter += 1
            if self.wave_counter > self.high_score: # Update highscore 
                self.high_score = self.wave_counter
                self.new_high = True
            self.in_game_timer = INIT_TIME_DURING_WAVES + WAVE_TIME_INCREMENT * self.wave_counter
            
    # Reset game
    def reset_game(self):
        self.grid.reset()
        self.in_game_timer = TIME_BETWEEN_WAVES
        self.wave_counter = 0
        self.new_high = False
        self.player.health = 100
        self.player._position = (336, 336)
        self.set_money(500)
    # Game over
    def game_over(self):
        self.reset_game()
        self.state = "GameOver"
    # Respawn/Spawn the player into a new game
    def new_game(self):
        self.reset_game()
        self.set_money(500)
        self.next_game_state()
    
    # Part of singleton pattern; allows the Game instance to be accessed easily
    @staticmethod 
    def get_instance():
        if Game._instance: return Game._instance
        else: 
            return Game()