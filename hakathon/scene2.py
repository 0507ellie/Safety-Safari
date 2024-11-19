import pygame 
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
FONT_COLOR = (0, 0, 0)
ITEM_SIZE = (60, 60)  # Set item size to 60x60 pixels
DOOR_COLOR = (255, 0, 0)  # Color for the door (red)
TIME_LIMIT = 20  # Time limit in seconds

# Load images (only for items, door will be a rectangle)
def load_image(name):
    image = pygame.image.load(name)
    return pygame.transform.scale(image, ITEM_SIZE)  # Scale image to ITEM_SIZE

# Item class
class Item:
    def __init__(self, name, points, image, position):
        self.name = name
        self.points = points
        self.image = image
        self.rect = self.image.get_rect(topleft=position)

# Function to display introductory text
def show_intro():
    screen.fill(WHITE)  # Fill the screen with white
    font = pygame.font.Font(None, 30)

    # First line of text
    intro_text = font.render("The first earthquake just ended...", True, FONT_COLOR)
    text_rect = intro_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))  # Adjust position slightly

    # Second line of text
    additional_text = font.render("You have to to pick up helpful objects to escape this room.", True, FONT_COLOR)
    additional_rect = additional_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))  # Position it below the first line

    screen.blit(intro_text, text_rect)  # Draw the introductory text
    screen.blit(additional_text, additional_rect)  # Draw the additional text

    pygame.display.flip()  # Update the display
    pygame.time.delay(3000)  # Wait for 3 seconds

# Setup the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pick Up Items Game")

# Load background image
background_img = pygame.image.load('background1.png')  # Replace with your own background image file
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Scale background to screen size

# Load item images
water_img = load_image('water.png')
coat_img = load_image('coat.png')
fruit_img = load_image('fruit.png')
phone_img = load_image('phone.png')
computer_img = load_image('computer.png')
headphones_img = load_image('headphones.png')

cat_image = pygame.image.load('cat.png')

# Create items
items = [
    Item("Water", 2, water_img, (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))),
    Item("Coat", 2, coat_img, (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))),
    Item("Fruit", 2, fruit_img, (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))),
    Item("Phone", -2, phone_img, (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))),
    Item("Computer", -2, computer_img, (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))),
    Item("Headphones", -2, headphones_img, (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))),
]

# Player position
player_pos = [WIDTH // 2, HEIGHT // 2]
score = 4
font = pygame.font.Font(None, 36)

# Game timer
start_ticks = pygame.time.get_ticks()  # Start timer

# Create a transparent door
door_surface = pygame.Surface((60, 60))  # Create surface for the door
door_surface.fill(DOOR_COLOR)  # Fill it with red color
door_surface.set_colorkey(DOOR_COLOR)  # Set red color as transparent

# Show the introduction screen
show_intro()

# Game loop
running = True
success = False
while running:
    screen.blit(background_img, (0, 0))  # Draw the background image

    # Display items
    for item in items:
        screen.blit(item.image, item.rect)

    # Draw the door (with transparency)
    door_rect = pygame.Rect(WIDTH - 70, HEIGHT - 70, 60, 60)  # Create a rectangle for the door
    screen.blit(door_surface, door_rect.topleft)  # Draw the transparent door surface

    # Display score and time left
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # Calculate elapsed seconds
    time_left = TIME_LIMIT - seconds
    score_text = font.render(f"Score: {score}", True, FONT_COLOR)
    time_text = font.render(f"Time Left: {max(0, time_left)}", True, FONT_COLOR)

    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (10, 40))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5

    # Draw the player (represented as a small rectangle)
    # pygame.draw.rect(screen, (0, 255, 0), (player_pos[0], player_pos[1], 20, 20))
    screen.blit(cat_image, (player_pos[0], player_pos[1]))


    # Check for item collision
    for item in items[:]:
        if item.rect.colliderect(pygame.Rect(player_pos[0], player_pos[1], 20, 20)):
            score += item.points
            items.remove(item)

    # Check for door collision
    if door_rect.colliderect(pygame.Rect(player_pos[0], player_pos[1], 20, 20)):
        success = True
        running = False

    # Check if time is up
    if time_left <= 0 and not success:
        running = False

    # Check if score is below 0
    if score < 0:
        running = False

    # Refresh the screen
    pygame.display.flip()
    pygame.time.delay(30)

# After the game loop ends, display results
def show_results(success):
    screen.fill(WHITE)
    if success:
        result_text = font.render(f"Success! Final Score: {score}", True, FONT_COLOR)
    else:
        result_text = font.render(f"You Lost! Final Score: {score}", True, FONT_COLOR)

    # Draw buttons
    continue_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)

    pygame.draw.rect(screen, (0, 200, 0), continue_button)  # Green button for continue
    pygame.draw.rect(screen, (200, 0, 0), exit_button)  # Red button for exit

    # Render button text
    continue_text = font.render("Continue", True, WHITE)
    exit_text = font.render("Exit", True, WHITE)

    screen.blit(result_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
    screen.blit(continue_text, (WIDTH // 2 - 50, HEIGHT // 2 + 35))
    screen.blit(exit_text, (WIDTH // 2 - 35, HEIGHT // 2 + 105))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if continue_button.collidepoint(mouse_pos):
                        waiting = False
                        # Automatically run scene3.py
                        pygame.quit()  # Close the current game window
                        os.system('python scene3.py')  # This will run scene3.py
                        sys.exit()  # Exit the program
                    elif exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

# Show results at the end of the game
show_results(success)
