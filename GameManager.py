"""
Manages the manager classes, including the Game manager and the InputManager. 
These are singletons to ensure the usage of only a single object.
"""

import pygame

# Constants
TIME_BETWEEN_WAVES = 30
INIT_TIME_DURING_WAVES = 20
WAVE_TIME_INCREMENT = 5
ENEMY_SPAWN_TIME = 5
GRID_SIZE = 15
STARTING_MONEY = 500

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

        # Initialisation
        self.grid = None
        self.player = None
        self.money = STARTING_MONEY # Add datasave later

        # Clock attributes
        self.clock = pygame.time.Clock()
        self.time = 0
        self._start_time = pygame.time.get_ticks() # Time of initial wave
        self.delta_time = self.clock.tick()
        self.in_game_timer = TIME_BETWEEN_WAVES
        self._last_second = 0 # For checking every second
        self.wave_counter = 0
        # self.extra_wave_time = 0 # For increasing the length of waves

        # Game state attributes
        # self.state = "None" # Can be None, Wave or Build
        self.max_enemies = 0

        # TESTING TESTING TESTING
        self.state = "Build" # TESTING DELETE WHEN ADDING A START BUTTON 
    
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
        if self.state == "None" or self.state == "Wave":
            self.add_money(100)
            self.state = "Build"
            self.in_game_timer = TIME_BETWEEN_WAVES
            self.max_enemies = 0
        elif self.state == "Build": 
            self.state = "Wave"
            self.wave_counter += 1
            self.in_game_timer = INIT_TIME_DURING_WAVES + WAVE_TIME_INCREMENT * self.wave_counter
            
    # Game over
    def game_over(self):
        self.state = "None"
    # Respawn
    def respawn(self):
        self.grid.reset()
        self.in_game_timer = TIME_BETWEEN_WAVES
        self.wave_counter = 0
        self.next_game_state()
        self.set_money(STARTING_MONEY)
    
    # Part of singleton pattern; allows the Game instance to be accessed easily
    @staticmethod 
    def get_instance():
        if Game._instance: return Game._instance
        else: 
            return Game()