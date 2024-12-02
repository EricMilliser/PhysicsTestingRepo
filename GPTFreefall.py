import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PIVOT = (400, 100)  # Pivot point (x, y)
LENGTH = 300        # Length of the string
BOB_RADIUS = 15     # Radius of the pendulum bob
GRAVITY = 9.8       # Gravitational acceleration (pixels/s²)
TIME_STEP = 1 / FPS

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Pendulum with Drag and Drop")
clock = pygame.time.Clock()

# Pendulum properties
angle = math.pi / 4  # Initial angle (45 degrees)
angular_velocity = 0
dragging = False
free_fall = False
bob_position = [PIVOT[0] + LENGTH * math.sin(angle), PIVOT[1] + LENGTH * math.cos(angle)]
bob_velocity = [0, 0]  # Velocity during free fall

def pendulum_acceleration(theta):
    """Compute angular acceleration for pendulum motion."""
    return -GRAVITY / LENGTH * math.sin(theta)

def rk4_update(theta, omega, dt):
    """Runge-Kutta 4th order method for pendulum motion."""
    k1_theta = omega
    k1_omega = pendulum_acceleration(theta)
    
    k2_theta = omega + 0.5 * dt * k1_omega
    k2_omega = pendulum_acceleration(theta + 0.5 * dt * k1_theta)
    
    k3_theta = omega + 0.5 * dt * k2_omega
    k3_omega = pendulum_acceleration(theta + 0.5 * dt * k2_theta)
    
    k4_theta = omega + dt * k3_omega
    k4_omega = pendulum_acceleration(theta + dt * k3_theta)
    
    theta_new = theta + dt / 6 * (k1_theta + 2 * k2_theta + 2 * k3_theta + k4_theta)
    omega_new = omega + dt / 6 * (k1_omega + 2 * k2_omega + 2 * k3_omega + k4_omega)
    return theta_new, omega_new

def distance(point1, point2):
    """Calculate distance between two points."""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if distance((mouse_x, mouse_y), bob_position) <= BOB_RADIUS:
                dragging = True
                free_fall = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                dx = bob_position[0] - PIVOT[0]
                dy = bob_position[1] - PIVOT[1]
                dist = math.sqrt(dx**2 + dy**2)
                if dist > LENGTH:
                    # Transition to free fall
                    free_fall = True
                    bob_velocity = [0, 0]  # Reset velocity
                else:
                    # Resume pendulum motion
                    free_fall = False
                    angle = math.atan2(dx, dy)
                    angular_velocity = 0  # Reset velocity

        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bob_position = [mouse_x, mouse_y]

    if dragging:
        # Override physics while dragging
        continue

    if free_fall:
        # Free-fall physics
        bob_velocity[1] += GRAVITY * TIME_STEP  # Apply gravity
        bob_position[0] += bob_velocity[0] * TIME_STEP
        bob_position[1] += bob_velocity[1] * TIME_STEP

        # Check if string becomes taut again
        dx = bob_position[0] - PIVOT[0]
        dy = bob_position[1] - PIVOT[1]
        dist = math.sqrt(dx**2 + dy**2)
        if dist <= LENGTH:
            free_fall = False
            angle = math.atan2(dx, dy)
            angular_velocity = 0  # Reset velocity
    else:
        # Pendulum physics
        angle, angular_velocity = rk4_update(angle, angular_velocity, TIME_STEP)
        bob_position[0] = PIVOT[0] + LENGTH * math.sin(angle)
        bob_position[1] = PIVOT[1] + LENGTH * math.cos(angle)

    # Drawing
    screen.fill((30, 30, 30))  # Background color
    pygame.draw.line(screen, (200, 200, 200), PIVOT, bob_position, 2)  # String
    pygame.draw.circle(screen, (255, 100, 100), (int(bob_position[0]), int(bob_position[1])), BOB_RADIUS)  # Bob

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
