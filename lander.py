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
    K_w,
    K_s,
    K_a,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1000

ENEMIES_DEFEATED = 0



# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()  # Initializes this class as an object of it's parent, sprite
        self.surf = pygame.Surface((25, 25))  # Creates the surface this player will exist on, essentially the "hit box"
        self.surf.fill((255, 255, 255))  # Fills that surface with a color
        self.rect = self.surf.get_rect(center=(500, SCREEN_HEIGHT/5))  # Grabs a rectangle from the space on the Surface, useful for drawing the player later
        self.health = 1
        self.player_pos_x = 0 #initialize x position of player object
        self.player_pos_y = 0 #initialize y position of player object
        self.x_speed = 0 # x speed, based on user input
        self.y_speed = 0 # y speed, based on user input

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        # If "UP" key pressed and we're not above the top
        if pressed_keys[K_w] and self.rect.top > 0:
            self.x_speed -= 0.01

        # If "DOWN" key pressed and we're not below the bottom
        if pressed_keys[K_s] and self.rect.bottom < SCREEN_HEIGHT:
            self.x_speed += 0.01

        # If "LEFT" key pressed and we're not beyond the minimum x-value
        if pressed_keys[K_a] and self.rect.left >= 0:
            self.y_speed -= 0.01

        # If "RIGHT" key pressed and we're not beyond the maximum x-value
        if pressed_keys[K_d] and self.rect.right < SCREEN_WIDTH:
            self.y_speed += 0.01
        
        # if 'Space" key is pressed get current position of the the player object
        # Used in Projectile Class   
        if pressed_keys[K_SPACE]:
            self.player_pos_x = self.rect.x
            self.player_pos_y = self.rect.y

# Define the wall object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'wall'
class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super(Wall, self).__init__()
        self.surf = pygame.Surface((SCREEN_WIDTH, 100))
        self.surf.fill((255, 255, 255))  # Fills that surface with color
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT))  # Grabs a rectangle from the space on the Surface, useful for drawing the player later

        # # Randomly chooses a spawn point of the enemy
        # self.rect = self.surf.get_rect(
        #     center=(
        #         random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
        #         random.randint(0, SCREEN_HEIGHT),
        #     )
        # )
        # self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self,player):
        global score

        self.rect.move_ip(-self.speed, 0)

        # Check if the player has collided with any walls
        if pygame.sprite.spritecollideany(player, walls,):
            global running
            player.health -= 1
            if player.health < 1:
                player.kill()
                running = False

                # If score higher than the high score save the high score to a txt file
                if score > int(highscore):
                    with open('highscore.txt', 'w') as f:
                        f.write(str(score))
            self.kill()


# Define the armor object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'armor'
class Armor(pygame.sprite.Sprite):
    def __init__(self):
        super(Armor, self).__init__()
        self.surf = pygame.Surface((30, 30))  # Size of the hitbox
        self.surf.fill((0, 0, 255))  # Blue
        self.speed = random.randint(25, 35)  # Speed
        # Where spawn
        self.rect = self.surf.get_rect(  
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self, player):
        global armor_check
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

        if pygame.sprite.spritecollideany(player, armors,):

            player.health+=1
            self.kill()
            
# Define the projectile object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'projectile'           
class Projectile(pygame.sprite.Sprite):
    def __init__(self, player_pos_x, player_pos_y):
        super(Projectile, self).__init__()
        self.surf = pygame.Surface((10,10))
        self.surf.fill((255,0,0)) # red
        self.speed = 20
        self.rect = self.surf.get_rect(
            center = (player_pos_x + 60,
                      player_pos_y + 10)
        )
  
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
        if pygame.sprite.spritecollideany(self, walls):
            self.kill()
                   
# TODO: This does not currently work
# Or maybe it does, but the thing that draws it isn't working?
class Health(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Health, self).__init__()
        self.surf = pygame.Surface((30, 30))  # Size of the hitbox
        self.surf.fill((136, 8, 8))  # Red
        # Where spawn
        self.rect = self.surf.get_rect(  
            center=(x, y)
        )
   

if __name__ == "__main__":
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
    # pygame.time.set_timer(ADDENEMY, 85)  # This is the timer for when each enemy gets added

    # Create a custome event for adding a armor powerup
    # ADDARMOR = pygame.USEREVENT + 2

    # Instantiate player. Right now, this is just a rectangle.
    player = Player()

    # Create groups to hold enemy sprites and all sprites, better than a list because:
    # - enemies is used for collision detection and position updates
    # - all_sprites is used for rendering
    walls = pygame.sprite.Group()
    armors = pygame.sprite.Group()
    health = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Draw the moon
    wall = Wall()
    all_sprites.add(wall)

    # Variable to keep the main loop running
    running = True

    # Run until the user asks to quit
    running = True
    score = 0
    time = 0
    projectile_sleep = 0
    X_SPEED = 0
    Y_SPEED = 0
    while running:
        print("PLAYER.HEALTH: ", player.health)
        time += 1
        projectile_sleep += 1

        X_SPEED += player.x_speed
        Y_SPEED += player.y_speed
        player.rect.move_ip(Y_SPEED, X_SPEED)

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

        # TODO: I think this block is trying to draw health in, the red block(s?) in the top right
        # Definitely not what it does currently...
        if player.health >= 1:
            new_health = Health(100,100)
            health.add(new_health)
            all_sprites.add(new_health)

        # Draw a solid blue circle in the center
        # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        # Get all keys currently pressed
        pressed_keys = pygame.key.get_pressed()

        # Update the player sprite based on user keypress
        player.update(pressed_keys)
        
        # if space pressed generate projectiles
        if pressed_keys[K_SPACE] and projectile_sleep > 5:
            new_projectile = Projectile(player.player_pos_x,player.player_pos_y)
            projectiles.add(new_projectile)
            all_sprites.add(new_projectile)
            projectile_sleep = 0

        # Update enemy position
        # enemies.update(player)

        # Update armor position
        armors.update(player)

        #update projectile position
        projectiles.update()
        
        # Erase the previous position of the player
        screen.fill((0, 0, 0))

        # Draw in the score
        text_surface, rect = GAME_FONT.render("High score: " + highscore + "--Current score: " + str(score) + "--player.health: " +str(player.health), (255, 255, 255))
        screen.blit(text_surface, ((SCREEN_WIDTH/2)-100, 10))

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)  # .blit() (Block Transfer) - transfers contents from one surface to another
            
        # Flip the display
        pygame.display.flip()

        clock.tick(60)  # Ensure frame rate is maintained

    # Done! Time to quit.
    pygame.quit()