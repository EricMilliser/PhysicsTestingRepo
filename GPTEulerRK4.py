import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PIVOT = (400, 100)  # Pivot point (x, y)
LENGTH = 300        # Length of the string
BOB_RADIUS = 15     # Radius of the pendulum bob
GRAVITY = 9.8       # Gravitational constant
TIME_STEP = 1 / FPS

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum Simulation with Euler and RK4")
clock = pygame.time.Clock()

# Pendulum properties
angle = math.pi / 4  # Initial angle (45 degrees)
angular_velocity = 0
method = "rk4"  # Choose between "euler" or "rk4"

def pendulum_acceleration(theta):
    """Compute angular acceleration."""
    return -GRAVITY / LENGTH * math.sin(theta)

def euler_update(theta, omega, dt):
    """Euler's method for updating angle and angular velocity."""
    alpha = pendulum_acceleration(theta)
    theta_new = theta + omega * dt
    omega_new = omega + alpha * dt
    return theta_new, omega_new

def rk4_update(theta, omega, dt):
    """Runge-Kutta 4th order method for updating angle and angular velocity."""
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

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                method = "euler"
            elif event.key == pygame.K_r:
                method = "rk4"

    # Physics calculations
    if method == "euler":
        angle, angular_velocity = euler_update(angle, angular_velocity, TIME_STEP)
    elif method == "rk4":
        angle, angular_velocity = rk4_update(angle, angular_velocity, TIME_STEP)

    # Bob position
    bob_x = PIVOT[0] + LENGTH * math.sin(angle)
    bob_y = PIVOT[1] + LENGTH * math.cos(angle)

    # Drawing
    screen.fill((30, 30, 30))  # Background color
    pygame.draw.line(screen, (200, 200, 200), PIVOT, (bob_x, bob_y), 2)  # String
    pygame.draw.circle(screen, (255, 100, 100), (int(bob_x), int(bob_y)), BOB_RADIUS)  # Bob

    # Display method on screen
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Method: {method.upper()}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()