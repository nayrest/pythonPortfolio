import pygame

pygame.mixer.init()

eat_sound = pygame.mixer.Sound("assets/sounds/eat.wav")
eat_sound.set_volume(0.3)

bonus_sound = pygame.mixer.Sound("assets/sounds/bonus.wav")
bonus_sound.set_volume(0.3)

gameover_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")
gameover_sound.set_volume(0.3)
