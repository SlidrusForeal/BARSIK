import pygame


class Dreamis:
    sprite = pygame.image.load('data/gfx/dream.png')

    def __init__(self, x_pos: float = 0, y_pos: float = 0):
        self.sprite = pygame.image.load('data/gfx/dream.png')
        self.position = pygame.Vector2()
        self.position.xy = x_pos, y_pos