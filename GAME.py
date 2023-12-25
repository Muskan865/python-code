import pygame
import sys
import random
from PIL import Image

# Initialize Pygame

pygame.init()

# Constants

WIDTH, HEIGHT = 800, 600
FPS = 60
CHARACTER_SPEED = 5
MAX_LIFE = 5
player_info={"score": 0}

# Colors

WHITE = (255, 255, 255)

RED = (255, 0, 0)

BLACK = (0, 0, 0)

# Create the screen

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Dodge the Objects!")

# Load images

image = Image.open('background.jpg')
new_image = image.resize((WIDTH, HEIGHT))
new_image.save('bg.jpg')
background_image = pygame.image.load("bg.jpg") 


char_image = Image.open('character.png')
character_image = char_image.resize((100, 50))
character_image.save('char.png')
character_image = pygame.image.load("char.png")


object_image = Image.open('object.png')
object_image = object_image.resize((160, 100))
object_image.save('ob.png')
object_image = pygame.image.load("ob.png")

# Set up the character

character_rect = character_image.get_rect()

character_rect.topleft = (10, HEIGHT // 2 - character_rect.height // 2)  # Adjust the initial position

character_life = MAX_LIFE

# Create a list to store objects

objects = []

# Object speed variables

OBJECT_SPEED = 5

SPEED_INCREASE_INTERVAL = 1000  # Increase speed every 1 seconds (in milliseconds)

SPEED_INCREASE_AMOUNT = 1  # Amount to increase the speed by

last_speed_increase_time = pygame.time.get_ticks()

# Clock to control the frame rate

clock = pygame.time.Clock()

# Function to draw the character and life bar

def draw_character(character_rect):

    screen.blit(character_image, character_rect)

    pygame.draw.rect(screen, RED, (10, 10, character_life * 50, 25)) 

# Function to move the character

def move_character(keys, character_rect):

    if keys[pygame.K_LEFT] and character_rect.left > 0 and character_rect.centerx > WIDTH // 2:

        character_rect.x -= CHARACTER_SPEED

    if keys[pygame.K_RIGHT] and character_rect.right < WIDTH and character_rect.centerx > WIDTH // 2:
        
        character_rect.x += CHARACTER_SPEED

    if keys[pygame.K_UP] and character_rect.top > 0:

        character_rect.y -= CHARACTER_SPEED

    if keys[pygame.K_DOWN] and character_rect.bottom < HEIGHT:

        character_rect.y += CHARACTER_SPEED

    return character_rect

# Function to generate objects

def draw_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score: {}".format(score), True, WHITE)
    text_rect = text.get_rect()
    text_rect.topleft = (WIDTH - text_rect.width - 10, 10)
    screen.blit(text, text_rect)

def generate_object():
     global player_info

     if len(objects) == 0 or objects[-1].x + objects[-1].width // 2 < WIDTH // 2:
        object_rect = object_image.get_rect()
        object_rect.x = WIDTH
        object_rect.y = random.randint(0, HEIGHT - object_rect.height)
        objects.append(object_rect)

        player_info["score"]+=1

        # Check if there are no objects or the last object has crossed the halfway point
        if len(objects) == 1 or objects[-1].x + objects[-1].width // 2 < WIDTH // 2:
            # Schedule the next object generation using recursion
            pygame.time.set_timer(pygame.USEREVENT + 1, random.randint(1000, 5000))
        else:
            # If not, immediately call the function recursively
            generate_object()

# Function to move objects

def move_objects():

    for falling_object in objects:

        falling_object.x -= OBJECT_SPEED

# Function to check collisions

def check_collisions():
    global character_life

    for falling_object in objects:
        if falling_object.colliderect(character_rect):
            character_life -= 1
            objects.remove(falling_object)

# Function to remove objects that are out of the screen

def remove_out_of_screen_objects():

    global objects

    objects = [falling_object for falling_object in objects if falling_object.x < WIDTH]




#Function to display game-over screen
    
def display_game_over_screen():
    screen.fill(WHITE)  # Fill the screen with a white background
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over! Final Score: {}".format(player_info["score"]), True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Display for 5 seconds
    pygame.quit()
    sys.exit()

# Game loop
while True:

    while character_life > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.USEREVENT + 1:
              generate_object()  # Call the function when the timer event occurs

  

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and character_rect.left > 0 and character_rect.centerx <= WIDTH // 2:
            character_rect.x -= CHARACTER_SPEED

        if keys[pygame.K_RIGHT] and character_rect.right < WIDTH and character_rect.centerx < WIDTH // 2:
            character_rect.x += CHARACTER_SPEED

        if keys[pygame.K_UP] and character_rect.top > 0:
            character_rect.y -= CHARACTER_SPEED

        if keys[pygame.K_DOWN] and character_rect.bottom < HEIGHT:
            character_rect.y += CHARACTER_SPEED

        character_rect = move_character(keys, character_rect)

        generate_object()
        move_objects()

        check_collisions()
        remove_out_of_screen_objects()

        screen.blit(background_image, (0, 0))
        draw_character(character_rect)

        for falling_object in objects:
            screen.blit(object_image, falling_object)

         # Draw the score
        draw_score(player_info["score"])
        pygame.display.flip()

        # Check if it's time to increase the object speed
        current_time = pygame.time.get_ticks()
        if current_time - last_speed_increase_time >= SPEED_INCREASE_INTERVAL:
            OBJECT_SPEED += SPEED_INCREASE_AMOUNT
            last_speed_increase_time = current_time

        clock.tick(FPS)

    # After the game loop ends (when character_life <= 0)
    display_game_over_screen()

    pygame.display.flip()
    clock.tick(FPS)  # Add this line to control the frame rate





