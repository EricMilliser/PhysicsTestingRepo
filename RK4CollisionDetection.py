import pygame
import math
import sys

#start pygame
pygame.init()

#declaration of the pygame screen constants
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiple Pendulum Collision Detection using RK4")

#Time constant using the pygame clock
clock = pygame.time.Clock()



#color constants in RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Pendulum parameters
length = 100  # Pixel length for pendulum
gravity = 9.81  # Gravitational speed constant in m/s^2
mass = 5.0  # Pendulum mass in kilograms
origin_1 = (WIDTH // 2, HEIGHT // 4)  # Placing one origin of the pendulum at Width integer division of 2, which is 400, and Height by integer division of 4, which is 150
origin_2 = (WIDTH // 2, HEIGHT // 4) #placing a second pendulum at a separate origin.

# Initial conditions
theta_1 = math.pi / 4  # starting theta at a angle of 45 degrees
theta_2 = (math.pi / 4 ) * (-1) # starting theta for second pendulum
omega_1 = 0.0  # Omega starting out at a velocity of 0.0 m/s
omega_2 = 0.0 #Omega for the second starting out at 0.0
h = 0.10  # h corresponding to step size for pendulum in RK4 method


circle = {"x": 400, "y": 400, "radius": 50} # circle for showing collision detection


def angularDerivatives_Pendulum(theta, omega): #takes a theta and corresponding omega for the angular derivates
    dtheta_h = omega #make the change in angle the angular velocity
    domega_h = -(gravity / length) * math.sin(theta) #find the acceleration based on gravity
    return dtheta_h, domega_h # return the derivatives


def rk4_step(theta, omega, h): #rk4 method function, taking an angular velocity, a current angle and a step size in time h



    k_1Theta, k_1Omega = angularDerivatives_Pendulum(theta, omega) #find k_1




    k_2Theta, k_2Omega = angularDerivatives_Pendulum(
        theta + k_1Theta * h / 2, omega + k_1Omega * h / 2
    ) # find k_2


    k_3Theta, k_3Omega = angularDerivatives_Pendulum(
        theta + k_2Theta * h / 2, omega + k_2Omega * h / 2
    ) #find k_3


    k_4Theta, k_4Omega = angularDerivatives_Pendulum(
        theta + k_3Theta * h, omega + k_3Omega * h
    ) #find K_4

    theta_next = theta + (h / 6) * (
        k_1Theta + 2 * k_2Theta + 2 * k_3Theta + k_4Theta
    ) #find next corresponding angle


    omega_next = omega + (h / 6) * (
        k_1Omega + 2 * k_2Omega + 2 * k_3Omega + k_4Omega
    ) #find next corresponding angluar velocity



    return theta_next, omega_next #return these values


def draw_pendulum(theta, origin): #function for drawing pendulums at a certain angle and orign



    #set the origins to the corresponding x and y values
    x = origin[0] + length * math.sin(theta)
    y = origin[1] + length * math.cos(theta)
 

    pygame.draw.line(screen, WHITE, origin, (x, y), 2) #draw the line for the pendulum 


    pygame.draw.circle(screen, RED, (int(x), int(y)), 10) #draw the pendulum part

    return x, y #return x and y pos for collision tracking


running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get(): # quit if the x is pressed on the program
        if event.type == pygame.QUIT:
            running = False


    #Updating the two pendulums
    theta_1, omega_1 = rk4_step(theta_1, omega_1, h) #using the first theta and omega values for the rk4 step
    theta_2, omega_2 = rk4_step(theta_2, omega_2, h) #using the second theta and omega values for the rk4 step


    x_1, y_1 = draw_pendulum(theta_1, origin_1) #set the x and y for the first pendulum

    x_2, y_2 = draw_pendulum(theta_2, origin_2) # set the x and y for the second pendulum


    

    # Calculate distance between circle centers
    dx = x_1 - x_2
    dy = y_1 - y_2
    distance = math.sqrt(dx**2 + dy**2)

    # Collision detection using the distance of the two radiuses added
    if distance < 20:
        color = RED
    else:
        color = BLUE




    pygame.draw.circle(screen, color, (circle["x"], circle["y"]), circle["radius"]) #draw the collision detecting circle





    
    pygame.display.flip() #display update

    #framerate cap
    clock.tick(60)


#exit after loop ends, the break condition is met.
pygame.quit()
sys.exit()
