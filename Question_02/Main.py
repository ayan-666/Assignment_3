import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My First Pygame Window")

# Set background color
background_color = (30, 30, 30)  # dark gray

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)  # Fill the screen with the background color
    pygame.display.flip()          # Update the display

# Quit Pygame
pygame.quit()
sys.exit()

