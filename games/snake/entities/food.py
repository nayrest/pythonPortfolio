import random
import pygame
from settings import WIDTH, HEIGHT, CELL_SIZE

class Food:
    def __init__(self, bonus=False):
        self.bonus = bonus        # флаг бонусной еды
        self.visible = True       # для мерцания
        self.timer = 0            # таймер мерцания
        self.pos = (-CELL_SIZE, -CELL_SIZE)
        self.bonus_timer = 0      # таймер жизни бонуса
        self.active = False       # активна бонусная еда

    def reset(self, bonus=False):
        """Перемещает еду в случайное место"""
        self.pos = (
            random.randrange(0, WIDTH, CELL_SIZE),
            random.randrange(0, HEIGHT, CELL_SIZE)
        )
        self.visible = True
        self.timer = 0
        self.bonus = bonus
        if bonus:
            self.active = True
            self.bonus_timer = 0
        else:
            self.active = False

    def draw(self, surface, color):
        """Рисует еду; мерцает если бонусная"""
        if self.bonus:
            self.timer += 1
            self.bonus_timer += 1
            if self.timer % 20 == 0:
                self.visible = not self.visible
            if self.visible:
                pygame.draw.rect(surface, color, (*self.pos, CELL_SIZE, CELL_SIZE))
            # Бонус исчезает через 5 секунд (пример)
            if self.bonus_timer > 5 * 60:
                self.active = False
                self.pos = (-CELL_SIZE, -CELL_SIZE)
                self.bonus_timer = 0
        else:
            pygame.draw.rect(surface, color, (*self.pos, CELL_SIZE, CELL_SIZE))

    def is_eaten(self, snake_head):
        return snake_head == self.pos
