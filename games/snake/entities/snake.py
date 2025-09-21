import pygame
import sys, os

# Настройка пути к проекту для ОС Windows
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, ".."))

from settings import CELL_SIZE

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        """Начальное тело змейки и направление"""
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL_SIZE, 0)  # по умолчанию вправо

    @property
    def head(self):
        """Голова змейки — первый сегмент"""
        return self.body[0]

    def move(self, grow=False):
        """
        Движение змейки.
        grow=True — если съели еду, тогда хвост не убирается
        """
        new_head = (self.head[0] + self.direction[0], self.head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()

    def change_direction(self, new_dir):
        """Запрет движения в противоположную сторону"""
        if (self.direction[0] + new_dir[0], self.direction[1] + new_dir[1]) != (0, 0):
            self.direction = new_dir

    def check_collision_self(self):
        """Проверка столкновения с собственным телом"""
        return self.head in self.body[1:]

    def draw(self, surface, color):
        """Рисуем все сегменты змейки"""
        for segment in self.body:
            pygame.draw.rect(surface, color, (*segment, CELL_SIZE, CELL_SIZE))
