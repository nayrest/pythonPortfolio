import random
import os
from settings import WIDTH, HEIGHT, CELL_SIZE, RECORD_FILE

# --- Рекорд ---
def load_record():
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_record(record):
    with open(RECORD_FILE, "w") as f:
        f.write(str(record))

# --- Генерация еды и бонусов ---
def random_cell():
    return (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))

def generate_obstacles(count=5):
    return [random_cell() for _ in range(count)]
