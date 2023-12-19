import pygame
import random

# Initialize Pygame
pygame.init()

# Create game window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Airplane variables
airplane_color = (0, 255, 0)  # Green color for the airplane
airplane_size = 30  # Size of the triangle representing the airplane
airplane_speed = 0.5  # Slow speed
airplane_pos = [screen_width / 2 - airplane_size / 2, screen_height - airplane_size * 2]  # Use a list to store float position
airplane_rect = pygame.Rect(airplane_pos[0], airplane_pos[1], airplane_size, airplane_size)

# Laser variables
lasers = []
laser_speed = 2  # Reduced laser speed
laser_width, laser_height = 1, 15
laser_cooldown = 0
laser_cooldown_period = 30  # Increased cooldown period

# Enemy variables
enemies = []
enemy_speed = 0.1  # Very slow speed
enemy_size = 40  # Size of the enemies
enemy_spawn_rate = 5  # How often to spawn enemies

# Game Loop
running = True
spawn_counter = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Shoot laser if space is held down
    if keys[pygame.K_SPACE] and laser_cooldown == 0:
        lasers.append(pygame.Rect(airplane_rect.centerx - laser_width / 2, airplane_rect.top, laser_width, laser_height))
        laser_cooldown = laser_cooldown_period

    # Update airplane position with float values
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        airplane_pos[0] -= airplane_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        airplane_pos[0] += airplane_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        airplane_pos[1] -= airplane_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        airplane_pos[1] += airplane_speed

    # Update airplane rect
    airplane_rect.x = int(airplane_pos[0])
    airplane_rect.y = int(airplane_pos[1])

    # Keep airplane on screen
    airplane_pos[0] = max(0, min(airplane_pos[0], screen_width - airplane_size))
    airplane_pos[1] = max(0, min(airplane_pos[1], screen_height - airplane_size))

    # Update lasers
    if laser_cooldown > 0:
        laser_cooldown -= 1
    for laser in lasers[:]:
        laser.y -= laser_speed
        if laser.y < 0:
            lasers.remove(laser)

    # Spawn enemies
    spawn_counter += 1
    if spawn_counter >= enemy_spawn_rate:
        spawn_counter = 0
        enemy_x = random.randint(0, screen_width - enemy_size)
        enemies.append([enemy_x, -enemy_size, enemy_speed])  # Store as [x, y, speed]

    # Move enemies with float values
    for enemy in enemies[:]:
        enemy[1] += enemy[2]
        if enemy[1] > screen_height:
            enemies.remove(enemy)

    # Check for laser hits
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0], int(enemy[1]), enemy_size, enemy_size)
        for laser in lasers[:]:
            if enemy_rect.colliderect(laser):
                enemies.remove(enemy)
                lasers.remove(laser)
                break

        # Check for collision with airplane
        if airplane_rect.colliderect(enemy_rect):
            running = False  # End the game

    # Render game
    screen.fill((0, 0, 0))  # Fill the screen with black

    # Draw the airplane (triangle)
    pygame.draw.polygon(screen, airplane_color, [
        (airplane_rect.x + airplane_size / 2, airplane_rect.y),
        (airplane_rect.x, airplane_rect.y + airplane_size),
        (airplane_rect.x + airplane_size, airplane_rect.y + airplane_size)
    ])

    # Draw lasers
    for laser in lasers:
        pygame.draw.rect(screen, (255, 0, 0), laser)  # Draw lasers (red color)

    # Draw enemies
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], int(enemy[1]), enemy_size, enemy_size)
        pygame.draw.rect(screen, (255, 255, 0), enemy_rect)  # Draw enemies (yellow color)
    
    pygame.display.update()

pygame.quit()

