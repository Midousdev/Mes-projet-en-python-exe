import pygame
import random
import ctypes
import os

# Masquer la console sur Windows
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre du jeu
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jeu du Dinosaure")

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Charger les images
dino_image = pygame.image.load("dino.png").convert_alpha()
cactus_image = pygame.image.load("cactus.png").convert_alpha()
background_image = pygame.image.load("background.png").convert()

# Charger le son
point_sound = pygame.mixer.Sound("point_sound.wav")

# Redimensionner les images
dino_image = pygame.transform.scale(dino_image, (60, 60))
cactus_image = pygame.transform.scale(cactus_image, (40, 60))
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Paramètres du dinosaure
dino_width = dino_image.get_width()
dino_height = dino_image.get_height()
dino_x = 50
dino_y = screen_height - dino_height - 30
dino_velocity_y = 0
gravity = 1.0  # Gravité réaliste
jump_height = -20  # Hauteur de saut ajustée

# Paramètres des obstacles
obstacle_width = cactus_image.get_width()
obstacle_height = cactus_image.get_height()
obstacle_velocity_x = -7
obstacle_frequency = 1500  # En millisecondes

# Variables de jeu
score = 0
clock = pygame.time.Clock()

# Police pour l'affichage du score et des messages
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# Fonctions de jeu
def draw_dino(x, y):
    screen.blit(dino_image, (x, y))

def draw_obstacle(obstacle_list):
    for obs in obstacle_list:
        screen.blit(cactus_image, (obs.x, obs.y))

def check_collision(dino_rect, obstacle_list):
    for obs in obstacle_list:
        if dino_rect.colliderect(obs):
            return True
    return False

def display_score(score):
    score_text = font.render("Score: " + str(score), True, black)
    screen.blit(score_text, [10, 10])

def display_game_over():
    game_over_text = game_over_font.render("Game Over", True, black)
    screen.blit(game_over_text, [screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2])

    # Dessiner les boutons
    retry_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
    quit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 120, 200, 50)
    pygame.draw.rect(screen, green, retry_button)
    pygame.draw.rect(screen, red, quit_button)

    retry_text = font.render("Réessayer", True, black)
    quit_text = font.render("Quitter", True, black)
    screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2 + 65))
    screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 135))

    pygame.display.flip()
    return retry_button, quit_button

def game_loop():
    global score
    running = True
    obstacle_list = []
    last_obstacle_time = pygame.time.get_ticks()
    dino_y = screen_height - dino_height - 30
    dino_velocity_y = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and dino_y == screen_height - dino_height - 30:
                    dino_velocity_y = jump_height

        # Logique du dinosaure
        dino_y += dino_velocity_y
        dino_velocity_y += gravity
        if dino_y >= screen_height - dino_height - 30:
            dino_y = screen_height - dino_height - 30

        # Logique des obstacles
        current_time = pygame.time.get_ticks()
        if current_time - last_obstacle_time > obstacle_frequency:
            obstacle_x = screen_width
            obstacle_y = screen_height - obstacle_height - 30
            obstacle_list.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))
            last_obstacle_time = current_time

        for obs in obstacle_list:
            obs.x += obstacle_velocity_x

        # Supprimer les obstacles hors de l'écran
        obstacle_list = [obs for obs in obstacle_list if obs.x > 0]

        # Vérifier les collisions
        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        if check_collision(dino_rect, obstacle_list):
            retry_button, quit_button = display_game_over()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if retry_button.collidepoint(event.pos):
                            game_loop()
                            return
                        elif quit_button.collidepoint(event.pos):
                            return
            running = False

        # Jouer un son chaque fois que le score atteint un multiple de 250
        if score % 250 == 0 and score != 0:
            point_sound.play()

        # Augmenter le score
        score += 1

        # Dessiner tout
        screen.blit(background_image, (0, 0))
        draw_dino(dino_x, dino_y)
        draw_obstacle(obstacle_list)
        display_score(score)
        pygame.display.flip()

        # Limiter la vitesse de la boucle
        clock.tick(30)

    pygame.quit()

# Lancer le jeu
game_loop()
