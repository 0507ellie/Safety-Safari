import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Set screen size
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flood Object Selection")

# Define colors
BLUE = (70, 130, 180)  # Water color
WHITE = (255, 255, 255)  # Text color
GREEN = (0, 255, 0)  # Player color
BROWN = (139, 69, 19)  # Land color
DARK_BLUE = (0, 0, 100)  # Dark background for results

# Load images
item_images = {
    "Phone": pygame.transform.scale(pygame.image.load("phone.png"), (50, 50)),
    "Wood": pygame.transform.scale(pygame.image.load("wood.png"), (50, 50)),
    "Water Bottle": pygame.transform.scale(pygame.image.load("water.png"), (50, 50)),
    "Computer": pygame.transform.scale(pygame.image.load("computer.png"), (50, 50))
}

lion_image  = pygame.image.load('lion.png')

# Floating object class
class FloatingObject:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.image = item_images[item_type]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, wave_offset):
        # Object floats with waves
        self.rect.y = self.y + math.sin(wave_offset + self.x * 0.05) * 10
        screen.blit(self.image, self.rect)

def draw_waves():
    """Draw wave effect"""
    wave_color = (135, 206, 250)  # Wave color
    for i in range(0, screen_width, 10):  # 10-pixel interval
        wave_height = math.sin((i + wave_offset) * 0.1) * 15  # Wave height
        pygame.draw.line(screen, wave_color, (i, 300 + wave_height), (i, screen_height))

# Create floating objects list
items = ["Phone", "Wood", "Water Bottle", "Computer"]
floating_objects = [
    FloatingObject(random.randint(100, 700), random.randint(200, 400), items[i])
    for i in range(4)
]

# Player settings
player_pos = [screen_width // 2, screen_height // 2]  # Player starting position
player_radius = 20  # Player size
score = 2  # Starting score

# Game loop
running = True
wave_offset = 0
result_text = ""
font = pygame.font.Font(None, 30)
start_time = pygame.time.get_ticks()
game_duration = 15000  # 10 seconds
game_over = False

# Define land shape as a list of points for an irregular polygon
land_shape = [(650, 200), (700, 150), (750, 200), (780, 300), (650, 350), (600, 300)]

def show_result_screen(result):
    """Display the result screen"""
    while True:
        screen.fill(DARK_BLUE)
        result_surface = font.render(result, True, WHITE)
        screen.blit(result_surface, (screen_width // 2 - result_surface.get_width() // 2, screen_height // 2 - 50))

        continue_button = font.render("Continue", True, WHITE)
        exit_button = font.render("Exit", True, WHITE)

        # Draw buttons
        pygame.draw.rect(screen, WHITE, (screen_width // 2 - 80, screen_height // 2 + 20, 160, 50), 2)
        pygame.draw.rect(screen, WHITE, (screen_width // 2 - 80, screen_height // 2 + 80, 160, 50), 2)

        screen.blit(continue_button, (screen_width // 2 - continue_button.get_width() // 2, screen_height // 2 + 30))
        screen.blit(exit_button, (screen_width // 2 - exit_button.get_width() // 2, screen_height // 2 + 90))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check for button clicks
                if (screen_width // 2 - 80 < mouse_x < screen_width // 2 + 80 and
                    screen_height // 2 + 20 < mouse_y < screen_height // 2 + 70):
                    pygame.quit() 
                    os.system("python closing.py")  # Run closing.py when "Continue" is clicked
                    return  # 退出此函数以避免重复调用
                if (screen_width // 2 - 80 < mouse_x < screen_width // 2 + 80 and
                    screen_height // 2 + 80 < mouse_y < screen_height // 2 + 130):
                    pygame.quit()  # Exit the game

def display_intro_message():
    """Display the intro messages for 3 seconds each"""
    messages = [
        "You are unfortunately swept away by the flood.",
        "Please choose an item that can help you and swim toward the shore."
    ]
    for message in messages:
        screen.fill(WHITE)
        text_surface = font.render(message, True, (0, 0, 0))  # Black text
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, screen_height // 2 - text_surface.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(3000)  # Display each message for 3 seconds

# Show intro messages
display_intro_message()

while running:
    screen.fill(BLUE)

    # Draw irregular land shape
    pygame.draw.polygon(screen, BROWN, land_shape)

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Control player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > player_radius:
            player_pos[0] -= 5
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_radius:
            player_pos[0] += 5
        if keys[pygame.K_UP] and player_pos[1] > player_radius:
            player_pos[1] -= 5
        if keys[pygame.K_DOWN] and player_pos[1] < screen_height - player_radius:
            player_pos[1] += 5

        # Check for collisions with objects
        for obj in floating_objects[:]:  # Use a copy of the list
            if obj.rect.collidepoint(player_pos):
                if obj.item_type in ["Wood", "Water Bottle"]:
                    score += 2  # Gain points
                else:
                    score -= 2  # Lose points
                floating_objects.remove(obj)  # Remove the object after collision

        # Check for collision with land (win condition)
        if pygame.draw.polygon(screen, BROWN, land_shape).collidepoint(player_pos):
            game_over = True  # End game if player reaches land
            result_text = "You Win!"
        

        # Update object positions
        wave_offset += 0.1  # Increase wave movement speed
        draw_waves()  # Draw wave effect
        for obj in floating_objects:
            obj.update(wave_offset)

        # Draw player
        #pygame.draw.circle(screen, GREEN, (int(player_pos[0]), int(player_pos[1])), player_radius)
        screen.blit(lion_image, (int(player_pos[0])-player_radius, int(player_pos[1])-player_radius))

        # Check game over conditions
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, (game_duration - elapsed_time) // 1000)  # Remaining time in seconds

        if remaining_time <= 0 or score < 0:
            game_over = True  # End game if time is up or score is negative
            result_text = f"You Lose! Final Score: {score}"

        # Show score and remaining time
        score_surface = font.render(f"Score: {score}", True, WHITE)
        time_surface = font.render(f"Time: {remaining_time}s", True, WHITE)
        screen.blit(score_surface, (10, 10))
        screen.blit(time_surface, (10, 50))

    else:
        # Show result screen
        show_result_screen(result_text)

    pygame.display.flip()
    pygame.time.delay(30)

# End game
pygame.quit()
