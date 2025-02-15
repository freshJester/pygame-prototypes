import pygame

# pygame setup
t = 1
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
player_height = 40
player_width = 40
dt = 0
actual_player_height = screen_height - player_height

player_pos = pygame.Vector2(screen_width / 2, actual_player_height)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    player = pygame.draw.rect(screen, "red", [player_pos.x, player_pos.y, player_width, player_height] )
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        t = 1
        player_pos.y -= 300 * dt
    elif player.bottom < screen_height:
        t += .05
        player_pos.y += 375 * t**2 * dt   
        if player_pos.y > actual_player_height:
            player_pos.y = actual_player_height   
    if keys[pygame.K_a] and player.left > 0:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d] and player.right < screen.get_width():
        player_pos.x += 300 * dt 
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()