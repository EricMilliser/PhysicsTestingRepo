import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 120
PIVOT = (400, 100)  # Pivot point (x, y)
LENGTH = 300        # Length of the string
BOB_RADIUS = 15     # Radius of the pendulum bob
GRAVITY = 9.8       # Gravitational constant
TIME_STEP = 5 / FPS

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loose String Pendulum")
clock = pygame.time.Clock()

# Pendulum properties
angle = math.pi / 4  # Initial angle (45 degrees)
angular_velocity = 0
angular_acceleration = 0
slack = False  # Is the string slack?

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Physics calculations
    if not slack:
        # Tension is present: standard pendulum physics
        angular_acceleration = -GRAVITY / LENGTH * math.sin(angle)
        angular_velocity += angular_acceleration * TIME_STEP
        angle += angular_velocity * TIME_STEP

        # Check if the string goes slack (e.g., due to low tension)
        if angular_velocity < 0.01 and math.cos(angle) < 0:
            slack = True
    else:
        # Slack string: free-fall physics
        angular_velocity *= 0.99  # Dampen motion slightly
        angle += angular_velocity * TIME_STEP

        # Check if the string pulls taut again
        if math.sqrt((PIVOT[1] + LENGTH * math.sin(angle) - HEIGHT)**2) >= LENGTH:
            slack = False

    # Bob position
    bob_x = PIVOT[0] + LENGTH * math.sin(angle)
    bob_y = PIVOT[1] + LENGTH * math.cos(angle)

    # Drawing
    screen.fill((30, 30, 30))  # Background color
    pygame.draw.line(screen, (200, 200, 200), PIVOT, (bob_x, bob_y), 2)  # String
    pygame.draw.circle(screen, (255, 100, 100), (int(bob_x), int(bob_y)), BOB_RADIUS)  # Bob

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
