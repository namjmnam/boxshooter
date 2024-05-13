import pygame
import random
import math

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
AIRPLANE_COLOR = (0, 255, 0)
AIRPLANE_SIZE = 30
AIRPLANE_SPEED = 0.5
LASER_SPEED = 2
LASER_WIDTH, LASER_HEIGHT = 1, 15
LASER_COOLDOWN_PERIOD = 30
LASER_AMPLITUDE = 20
LASER_FREQUENCY = 0.1
ENEMY_SIZE = 40
ENEMY_SPEED = 0.1
ENEMY_SPAWN_RATE = 5

# Initialize Pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def reset_game():
    global airplane_pos, airplane_rect, lasers, enemies, spawn_counter, laser_cooldown
    airplane_pos = [SCREEN_WIDTH / 2 - AIRPLANE_SIZE / 2, SCREEN_HEIGHT - AIRPLANE_SIZE * 2]
    airplane_rect = pygame.Rect(airplane_pos[0], airplane_pos[1], AIRPLANE_SIZE, AIRPLANE_SIZE)
    lasers = []
    enemies = []
    spawn_counter = 0
    laser_cooldown = 0

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update_game():
    global laser_cooldown
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and laser_cooldown == 0:
        shoot_laser('sine')
    if keys[pygame.K_c] and laser_cooldown == 0:
        shoot_laser('cosine')

    update_airplane(keys)
    update_lasers()
    spawn_enemies()
    check_collisions()

def shoot_laser(type):
    global laser_cooldown
    initial_x = airplane_rect.centerx - LASER_WIDTH / 2
    lasers.append({
        'type': type,
        'initial_x': initial_x,
        'age': 0,
        'rect': pygame.Rect(initial_x, airplane_rect.top, LASER_WIDTH, LASER_HEIGHT)
    })
    laser_cooldown = LASER_COOLDOWN_PERIOD

def update_airplane(keys):
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        airplane_pos[0] -= AIRPLANE_SPEED
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        airplane_pos[0] += AIRPLANE_SPEED
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        airplane_pos[1] -= AIRPLANE_SPEED
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        airplane_pos[1] += AIRPLANE_SPEED

    # Keep airplane on screen
    airplane_pos[0] = max(0, min(airplane_pos[0], SCREEN_WIDTH - AIRPLANE_SIZE))
    airplane_pos[1] = max(0, min(airplane_pos[1], SCREEN_HEIGHT - AIRPLANE_SIZE))

    airplane_rect.x, airplane_rect.y = int(airplane_pos[0]), int(airplane_pos[1])

def update_lasers():
    global laser_cooldown
    for laser in lasers[:]:
        laser['age'] += 1
        if laser['type'] == 'sine':
            wave_x = laser['initial_x'] + LASER_AMPLITUDE * math.sin(LASER_FREQUENCY * laser['age'])
        else:  # 'cosine'
            wave_x = laser['initial_x'] + LASER_AMPLITUDE * math.cos(LASER_FREQUENCY * laser['age'])
        laser['rect'].x = int(wave_x)
        laser['rect'].y -= LASER_SPEED
        if laser['rect'].y < 0:
            lasers.remove(laser)

    if laser_cooldown > 0:
        laser_cooldown -= 1

def spawn_enemies():
    global spawn_counter
    spawn_counter += 1
    if spawn_counter >= ENEMY_SPAWN_RATE:
        spawn_counter = 0
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        enemies.append([enemy_x, -ENEMY_SIZE, ENEMY_SPEED])

def check_collisions():
    global game_over
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0], int(enemy[1]), ENEMY_SIZE, ENEMY_SIZE)
        for laser in lasers[:]:
            if enemy_rect.colliderect(laser['rect']):
                enemies.remove(enemy)
                lasers.remove(laser)
                break
        if airplane_rect.colliderect(enemy_rect):
            game_over = True  # Trigger game over state

def render_game():
    screen.fill((0, 0, 0))  # Fill the screen with black
    pygame.draw.polygon(screen, AIRPLANE_COLOR, [
        (airplane_rect.x + AIRPLANE_SIZE / 2, airplane_rect.y),
        (airplane_rect.x, airplane_rect.y + AIRPLANE_SIZE),
        (airplane_rect.x + AIRPLANE_SIZE, airplane_rect.y + AIRPLANE_SIZE)
    ])
    for laser in lasers:
        pygame.draw.rect(screen, (255, 0, 0), laser['rect'])
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], int(enemy[1]), ENEMY_SIZE, ENEMY_SIZE)
        pygame.draw.rect(screen, (255, 255, 0), enemy_rect)
    pygame.display.update()

def main():
    global game_over
    reset_game()
    running = True
    game_over = False
    while running:
        running = handle_events()
        if game_over:
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 74)
            text = font.render('Game Over', True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(text, text_rect)
            pygame.display.update()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_c]:
                game_over = False
                reset_game()
            continue

        update_game()
        render_game()

    pygame.quit()

if __name__ == '__main__':
    main()
