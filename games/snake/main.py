import pygame
import random
import sys
from settings import *
from entities.snake import Snake
from entities.food import Food
from entities.obstacles import Obstacles
from sounds import eat_sound, bonus_sound, gameover_sound

pygame.init()
pygame.mixer.init()
FONT = pygame.font.SysFont("Arial", 24)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка для детей")
clock = pygame.time.Clock()

# ------------------ ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ------------------
difficulty = "medium"
colors = THEMES[difficulty]
snake = Snake()
normal_food = Food(bonus=False)
bonus_food = Food(bonus=True)
bonus_food.pos = (-CELL_SIZE, -CELL_SIZE)  # скрыта в начале
obstacles = Obstacles()
score = 0
paused = False
highscore = 0

# Таймеры для бонусной еды
bonus_timer = 0
bonus_interval = 0
bonus_duration = 0

# ------------------ ЗАГРУЗКА РЕКОРДА ------------------
try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except:
    highscore = 0

# ------------------ ФУНКЦИИ ------------------
def reset_game():
    global snake, normal_food, bonus_food, score, colors
    global bonus_timer, bonus_interval, bonus_duration
    snake.reset()
    normal_food.reset()
    bonus_food.pos = (-CELL_SIZE, -CELL_SIZE)  # убираем бонус
    obstacles.generate()
    score = 0
    colors = THEMES[difficulty]
    bonus_timer = 0
    bonus_interval = random.randint(5, 15) * DIFFICULTIES[difficulty]["speed"]
    bonus_duration = 0

def draw_text(text, pos, color):
    label = FONT.render(text, True, color)
    screen.blit(label, pos)

def toggle_pause():
    global paused
    paused = not paused

def game_over():
    global highscore
    pygame.mixer.music.stop()
    gameover_sound.play()
    if score > highscore:
        highscore = score
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))
    screen.fill((0,0,0))
    draw_text(f"Игра окончена! Счет: {score}", (WIDTH//6, HEIGHT//2), colors["text"])
    draw_text(f"Рекорд: {highscore}", (WIDTH//6, HEIGHT//2 + 40), colors["text"])
    pygame.display.flip()
    pygame.time.wait(3000)
    main_menu()

def main_menu():
    global difficulty
    while True:
        screen.fill((0,0,0))
        draw_text("Выберите уровень сложности", (WIDTH//6, 100), (255,255,255))
        draw_text("1 - Легкий", (WIDTH//6, 160), (0,255,0))
        draw_text("2 - Средний", (WIDTH//6, 200), (255,255,0))
        draw_text("3 - Сложный", (WIDTH//6, 240), (255,0,0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    set_difficulty("easy")
                    start_game()
                elif event.key == pygame.K_2:
                    set_difficulty("medium")
                    start_game()
                elif event.key == pygame.K_3:
                    set_difficulty("hard")
                    start_game()

def set_difficulty(level):
    global difficulty, colors
    difficulty = level
    colors = THEMES[difficulty]

def start_game():
    reset_game()
    pygame.mixer.music.load(DIFFICULTIES[difficulty]["music"])
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    game_loop()

def game_loop():
    global score, paused
    global bonus_timer, bonus_interval, bonus_duration
    speed = DIFFICULTIES[difficulty]["speed"]

    while True:
        # ----------------- ОБРАБОТКА СОБЫТИЙ -----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, CELL_SIZE):
                    snake.change_direction((0, -CELL_SIZE))
                elif event.key == pygame.K_DOWN and snake.direction != (0, -CELL_SIZE):
                    snake.change_direction((0, CELL_SIZE))
                elif event.key == pygame.K_LEFT and snake.direction != (CELL_SIZE, 0):
                    snake.change_direction((-CELL_SIZE, 0))
                elif event.key == pygame.K_RIGHT and snake.direction != (-CELL_SIZE, 0):
                    snake.change_direction((CELL_SIZE, 0))
                elif event.key == pygame.K_p:
                    toggle_pause()

        # ----------------- ПАУЗА -----------------
        if paused:
            screen.fill((0,0,0))
            draw_text("ПАУЗА", (WIDTH//2 - 50, HEIGHT//2), (255,255,255))
            pygame.display.flip()
            clock.tick(5)
            continue

        # ----------------- ДВИЖЕНИЕ ЗМЕЙКИ -----------------
        snake.move()

        # ----------------- ПРОВЕРКА СТОЛКНОВЕНИЙ -----------------
        x, y = snake.head
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or snake.check_collision_self() or snake.head in obstacles.positions:
            game_over()

        # ----------------- ОРДИНАРНАЯ ЕДА -----------------
        if snake.head == normal_food.pos:
            score += 1
            eat_sound.play()
            snake.move(grow=True)
            normal_food.reset()

        # ----------------- БОНУСНАЯ ЕДА -----------------
        if bonus_food.pos == (-CELL_SIZE, -CELL_SIZE):  # бонуса нет
            bonus_timer += 1
            if bonus_timer >= bonus_interval:  # пора показать бонус
                bonus_food.reset(bonus=True)
                bonus_duration = 12 * speed  # живёт 12 секунд
                bonus_timer = 0
                bonus_interval = random.randint(5, 15) * speed
        else:
            bonus_duration -= 1
            if bonus_duration <= 0:  # время вышло
                bonus_food.pos = (-CELL_SIZE, -CELL_SIZE)

        # съедена бонусная еда
        if snake.head == bonus_food.pos:
            score += 5
            bonus_sound.play()
            snake.move(grow=True)
            snake.move(grow=True)
            bonus_food.pos = (-CELL_SIZE, -CELL_SIZE)

        # ----------------- ОТРИСОВКА -----------------
        screen.fill(colors["bg"])
        snake.draw(screen, colors["snake"])
        normal_food.draw(screen, colors["food"])
        if bonus_food.pos != (-CELL_SIZE, -CELL_SIZE):
            bonus_food.draw(screen, (255,0,255))  # фиолетовый бонус
        obstacles.draw(screen, OBSTACLE_COLOR)
        draw_text(f"Счет: {score}", (10,10), colors["text"])
        draw_text(f"Рекорд: {highscore}", (10,40), colors["text"])
        pygame.display.flip()
        clock.tick(speed)

# ----------------- ЗАПУСК -----------------
try:
    main_menu()
except KeyboardInterrupt:
    pygame.quit()
    sys.exit()