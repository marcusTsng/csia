import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 800,800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Sprite:
    SPRITES = []
    def __init__(self, position : tuple, image_path : str):
        self._position = position
        self.image = pygame.image.load(image_path)

        Sprite.SPRITES.append(self)
    
    def get_pos(self): return self._position[0], self._position[1]
    def set_pos(self, position : tuple): self._position = position

    def display(self): SCREEN.blit(self.image, self._position)

    def destroy(self): Sprite.SPRITES.remove(self) 

    @staticmethod
    def display_all_sprites():
        for x in Sprite.SPRITES:
            x.display()

class Player(Sprite):
    def __init__(self, image_path):
        super().__init__((0,0), image_path)