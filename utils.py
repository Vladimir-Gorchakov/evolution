import pygame
from pygame.color import THECOLORS

class Render:
    def __init__(self, thikness = 20):
        self.thikness = thikness
        self.bias = 0

    def render_text(self, txt, window):
        font = pygame.font.SysFont('couriernew', self.thikness)
        text = font.render(txt, True, THECOLORS['gray'])
        window.blit(text, (50, 50+self.bias))
        self.bias += self.thikness
    
    def clear(self):
        self.bias = 0