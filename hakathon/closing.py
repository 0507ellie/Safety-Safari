import pygame

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Ending")

# Define colors
WHITE = (255, 255, 255)
FONT_COLOR = (0, 0, 0)

# Function to display ending text
def show_end_screen():
    screen.fill(WHITE)  # Fill the screen with white
    font = pygame.font.Font(None, 48)
    
    # Ending message
    end_text = font.render("You finally survived! Congrats!", True, FONT_COLOR)
    text_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.blit(end_text, text_rect)  # Draw the ending text
    pygame.display.flip()  # Update the display

    # Wait for a few seconds before quitting
    pygame.time.delay(3000)  # Wait for 3 seconds
    pygame.quit()  # Quit Pygame

# Run the ending screen
show_end_screen()
pygame.quit() 