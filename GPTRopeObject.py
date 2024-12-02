import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PIVOT = (400, 100)  # Pivot point (x, y)
LENGTH = 300        # Total length of the rope
ROPE_SEGMENTS = 20  # Number of segments in the rope
BOB_RADIUS = 15     # Radius of the pendulum bob
GRAVITY = 9.8       # Gravitational acceleration (pixels/s²)
TIME_STEP = 1 / FPS

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Curved Rope Pendulum")
clock = pygame.time.Clock()

# Rope nodes and constraints
nodes = []
segment_length = LENGTH / ROPE_SEGMENTS

# Initialize rope nodes
for i in range(ROPE_SEGMENTS + 1):
    x = PIVOT[0]
    y = PIVOT[1] + i * segment_length
    nodes.append({"pos": [x, y], "prev_pos": [x, y]})  # Verlet requires previous position

# Bob
bob_position = nodes[-1]["pos"]
bob_velocity = [0, 0]  # Velocity for free fall
dragging = False
free_fall = False

def apply_gravity():
    """Apply gravity to all nodes except the pivot."""
    for i in range(1, len(nodes)):
        nodes[i]["pos"][1] += GRAVITY * TIME_STEP

def verlet_integration():
    """Update node positions using Verlet integration."""
    for node in nodes:
        current_pos = node["pos"]
        prev_pos = node["prev_pos"]
        # Verlet formula
        temp_pos = current_pos[:]
        node["pos"][0] += (current_pos[0] - prev_pos[0])
        node["pos"][1] += (current_pos[1] - prev_pos[1])
        node["prev_pos"] = temp_pos

def constrain_nodes():
    """Enforce distance constraints between connected nodes."""
    for _ in range(5):  # Iterate to stabilize constraints
        for i in range(len(nodes) - 1):
            node_a = nodes[i]
            node_b = nodes[i + 1]
            dx = node_b["pos"][0] - node_a["pos"][0]
            dy = node_b["pos"][1] - node_a["pos"][1]
            dist = math.sqrt(dx**2 + dy**2)
            diff = (dist - segment_length) / dist
            if i == 0:  # Pivot is fixed
                node_b["pos"][0] -= dx * 0.5 * diff
                node_b["pos"][1] -= dy * 0.5 * diff
            else:
                node_a["pos"][0] += dx * 0.5 * diff
                node_a["pos"][1] += dy * 0.5 * diff
                node_b["pos"][0] -= dx * 0.5 * diff
                node_b["pos"][1] -= dy * 0.5 * diff

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
            dragging = False
            if distance(bob_position, PIVOT) > LENGTH:
                free_fall = True
                bob_velocity = [0, 0]  # Reset velocity
        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bob_position[0], bob_position[1] = mouse_x, mouse_y

    if not dragging:
        if free_fall:
            # Free fall motion
            bob_velocity[1] += GRAVITY * TIME_STEP
            bob_position[0] += bob_velocity[0] * TIME_STEP
            bob_position[1] += bob_velocity[1] * TIME_STEP

            # Check if rope becomes taut again
            dx = bob_position[0] - PIVOT[0]
            dy = bob_position[1] - PIVOT[1]
            dist = math.sqrt(dx**2 + dy**2)
            if dist <= LENGTH:
                free_fall = False
        else:
            # Apply gravity, Verlet integration, and constraints
            apply_gravity()
            verlet_integration()
            constrain_nodes()

    # Update the bob position
    nodes[-1]["pos"] = bob_position

    # Drawing
    screen.fill((30, 30, 30))  # Background color
    # Draw rope
    for i in range(len(nodes) - 1):
        pygame.draw.line(screen, (200, 200, 200), nodes[i]["pos"], nodes[i + 1]["pos"], 2)
    # Draw bob
    pygame.draw.circle(screen, (255, 100, 100), (int(bob_position[0]), int(bob_position[1])), BOB_RADIUS)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
