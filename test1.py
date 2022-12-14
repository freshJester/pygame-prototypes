# Simple pygame program, much of this code borrowed from https://realpython.com/pygame-a-primer/

# Import and initialize the pygame library
import pygame
import pygame.freetype
import random

# Setup the clock
clock = pygame.time.Clock()

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1000

ENEMIES_DEFEATED = 0


# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()  # Initializes this class as an object of it's parent, sprite
        self.surf = pygame.Surface((75, 25))  # Creates the surface this player will exist on, essentially the "hit box"
        self.surf.fill((255, 255, 255))  # Fills that surface with a color
        self.rect = self.surf.get_rect(center=(250, SCREEN_HEIGHT/2))  # Grabs a rectangle from the space on the Surface, useful for drawing the player later
        self.health = 1

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        # If "UP" key pressed and we're not above the top
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -15)

        # If "DOWN" key pressed and we're not below the bottom
        if pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, 15)

        # If "LEFT" key pressed and we're not beyond the minimum x-value
        if pressed_keys[K_LEFT] and self.rect.left >= 0:
            self.rect.move_ip(-20, 0)

        # If "RIGHT" key pressed and we're not beyond the maximum x-value
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(15, 0)


# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        # self.speed = random.randint(5, 20)
        self.speed = random.gauss(mu=55, sigma=10)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self,player):
        global ENEMIES_DEFEATED
        global score

        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            ENEMIES_DEFEATED += 1
            score += 1



# Define the armor object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'armor'
class Armor(pygame.sprite.Sprite):
    def __init__(self):
        super(Armor, self).__init__()
        self.surf = pygame.Surface((30, 30))  # Size of the hitbox
        self.surf.fill((0, 0, 255))  # Blue
        # Where spawn
        self.rect = self.surf.get_rect(  
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        # self.speed = random.randint(5, 20)
        self.speed = 30

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self, player):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

        if pygame.sprite.spritecollideany(player, armors,):
            player.health+=1
            self.kill()


# Initialize pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
GAME_FONT = pygame.freetype.Font("ConnectionIii-Rj3W.otf", 24)
with open("highscore.txt", "r") as f:
    highscore = f.read()

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250)
pygame.time.set_timer(ADDENEMY, 100)

# Create a custome event for adding a armor powerup
# ADDARMOR = pygame.USEREVENT + 2

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites, better than a list because:
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
armors = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

# Run until the user asks to quit
running = True
score = 0
armor_check = False
while running:
    print("PLAYER.HEALTH: ", player.health)
    # Did the user click the window close button?
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == pygame.QUIT:
            running = False
            
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # # Add powerup?
        # elif event.type == ADDARMOR and ENEMIES_DEFEATED == 10:
        #     # Create the new armor and add it to sprite groups
        #     new_armor = Armor()
        #     armors.add(new_armor)
        #     all_sprites.add(new_armor)

    # Responsible for spawning armor   
    # for entity in all_sprites:
    #     if type(entity) == armor:
    #         armor_check = True

    if ENEMIES_DEFEATED % 10 == 0 and armor_check == False:
        # Create the new armor and add it to sprite groups
        new_armor = Armor()
        armors.add(new_armor)
        all_sprites.add(new_armor)
        armor_check = True
    else:
        armor_check = False


    # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Get all keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    # Update the player sprite based on user keypress
    player.update(pressed_keys)

    # Update enemy position
    enemies.update(player)

    # Update armor position
    armors.update(player)

    # Erase the previous position of the player
    screen.fill((0, 0, 0))

    # Draw in the score
    text_surface, rect = GAME_FONT.render("High score: " + highscore + "--Current score: " + str(score), (255, 255, 255))
    screen.blit(text_surface, ((SCREEN_WIDTH/2)-100, 10))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)  # .blit() (Block Transfer) - transfers contents from one surface to another

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies,):
        # If so, then remove the player and stop the loop
        player.health -= 1
        if player.health<1:
            player.kill()
            running = False

        # Save the high score to a txt file, if score higher than the high score
        if score > int(highscore):
            with open('highscore.txt', 'w') as f:
                f.write(str(score))

    # Flip the display
    pygame.display.flip()

    clock.tick(60)  # Ensure frame rate is maintained

# Done! Time to quit.
pygame.quit()