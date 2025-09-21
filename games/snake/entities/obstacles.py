import random
import pygame
import sys, os
# Настройка пути к проекту для Windows
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root + "\\..")

from settings import WIDTH, HEIGHT, CELL_SIZE, OBSTACLE_COUNT

class Obstacles:
    def __init__(self):
        self.positions = []
        self.generate()

    def generate(self):
        self.positions = []
        for _ in range(OBSTACLE_COUNT):
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            self.positions.append((x, y))

    def draw(self, screen, color):
        for pos in self.positions:
            pygame.draw.rect(screen, color, (*pos, CELL_SIZE, CELL_SIZE))
