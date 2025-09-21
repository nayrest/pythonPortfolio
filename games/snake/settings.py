import pygame

# Настройки окна
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

OBSTACLE_COUNT = 5  # количество препятствий на поле
OBSTACLE_COLOR = (150, 75, 0)  # коричневый


# Цвета и темы для уровней сложности
THEMES = {
    "easy": {"bg": (0, 0, 50), "snake": (0, 200, 0), "food": (255, 200, 0), "bonus": (0, 255, 255), "text": (255, 255, 255)},
    "medium": {"bg": (80, 80, 80), "snake": (0, 100, 200), "food": (200, 0, 0), "bonus": (255, 255, 0), "text": (255, 255, 255)},
    "hard": {"bg": (0, 0, 0), "snake": (255, 255, 255), "food": (255, 100, 0), "bonus": (0, 255, 0), "text": (200, 0, 200)}
}

DIFFICULTIES = {
    "easy": {"speed": 7, "music": "assets/sounds/easy.mp3"},
    "medium": {"speed": 12, "music": "assets/sounds/medium.mp3"},
    "hard": {"speed": 18, "music": "assets/sounds/hard.mp3"}
}

HIGH_SCORE_FILE = "highscore.txt"
