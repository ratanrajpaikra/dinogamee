import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
GROUND_HEIGHT = 30     
FPS = 90 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")

# Load images
dino_img = pygame.image.load('dinoo.png').convert()
dino_img.set_colorkey(WHITE)
cactus_img = pygame.image.load('cactus.png').convert()
cactus_img.set_colorkey(WHITE)

# Game variables
dino_x = 0
dino_y = SCREEN_HEIGHT - GROUND_HEIGHT - dino_img.get_height()
dino_vel_y = 0
gravity = 0.5
jump_power = -15
is_jumping = False

cactus_list = []
SPAWN_CACTUS = pygame.USEREVENT
pygame.time.set_timer(SPAWN_CACTUS, 1500)

score = 0
font = pygame.font.Font(None, 40)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def spawn_cactus():
    cactus_height = random.randint(100, 150)
    cactus_x = SCREEN_WIDTH
    cactus_y = SCREEN_HEIGHT - GROUND_HEIGHT - cactus_height
    cactus_list.append([cactus_x, cactus_y, cactus_img.get_width(), cactus_height])

def check_collision(dino_rect, cactus_list):
    for cactus in cactus_list:
        cactus_rect = pygame.Rect(cactus[0], cactus[1], cactus[2], cactus[3])
        if dino_rect.colliderect(cactus_rect):
            return True
    return False

clock = pygame.time.Clock()
running = True   

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_CACTUS:
            spawn_cactus()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                dino_vel_y = jump_power
                is_jumping = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not  is_jumping:
        dino_vel_y = jump_power
        is_jumping = False

    # Update Dino
    dino_vel_y += gravity
    dino_y += dino_vel_y
    if dino_y >= SCREEN_HEIGHT - GROUND_HEIGHT - dino_img.get_height():
        dino_y = SCREEN_HEIGHT - GROUND_HEIGHT - dino_img.get_height()
        dino_vel_y = 10  
        is_jumping = False

    dino_rect = pygame.Rect(dino_x, dino_y, dino_img.get_width(), dino_img.get_height())

    # Update Cactus
    for cactus in cactus_list:
        cactus[0] -= 10
        if cactus[0] + cactus[2] < 0:
            cactus_list.remove(cactus)
            score += 1

    # Check collision
    if check_collision(dino_rect, cactus_list):
        running = False
    

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
    screen.blit(dino_img, (dino_x, dino_y))
    for cactus in cactus_list:
        screen.blit(cactus_img, (cactus[0], cactus[1]))

    draw_text(f'Score: {score}', font, WHITE, 10, 10)

    pygame.display.flip()

pygame.quit()