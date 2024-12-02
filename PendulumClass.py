import math



class Object():
    def __init__(self, mass_input):
        self.mass_kg = mass_input


class PendulumObject(Object):
    def __init__(self, mass_input, length_input, radius_input, starting_angle = 0.0, starting_velocity = 0.0, slack_input = False):
        super().__init__(mass_input)()
        self.length = length_input
        self.radius = radius_input
        self.theta = starting_angle
        self.omega = starting_velocity
        self.slack = slack_input
        self.acceleration = 0.0
        self.origin_x = 0
        self.origin_y = 0
        self.GRAVITY = 9.8
        self.dt = .05
        self.dragged = False

    def setOrigin(self, x_input, y_input):
        self.origin_x = x_input
        self.origin_y = y_input

    def setLength(self, length_input):
        self.length = length_input
    
    def setRadius(self, radius_input):
        self.radius = radius_input

    def setTheta(self, starting_angle):
        self.theta = starting_angle
    
    def setVelocity(self, starting_velocity):
        self.omega = starting_velocity

    def setSlack(self, slack_input):
        self.slack = slack_input

    def setAcceleration(self, acceleration_input):
        self.acceleration = acceleration_input

    def setTimeStep(self, time_step):
        self.dt = time_step


    def getOrigin_XY(self):
        return self.origin_x, self.origin_y
    
    def getLength(self):
        return self.length
    
    def getRadius(self):
        return self.radius
    
    def getTheta(self):
        return self.theta
    
    def getVelocity(self):
        return self.omega
    
    def getSlack(self):
        return self.slack
    
    def getAcceleration(self):
        return self.acceleration
    
    def getDT(self):
        return self.dt

    def computeAcceleration(self):
        return -self.GRAVITY / self.length * math.sin(self.theta)
    

    def computeRK4Step(self, kStep_Theta):
        return self.theta + 0.5 * self.dt * kStep_Theta
    
    def eulerUpdate(self):
        alpha = self.computeAcceleration()
        theta_new = self.theta + self.omega * self.dt
        omega_new = self.omega + alpha * self.dt
        self.setTheta(theta_new)
        self.setVelocity(omega_new)
        return
    
    def RK4_UPDATE(self):
        k_1_Theta = self.omega
        k_1_Omega = self.computeAcceleration()

        k_2_Theta = self.omega + 0.5 * self.dt * k_1_Omega
        k_2_Omega = self.computeRK4Step(k_1_Theta)

        k_3_Theta = self.omega + 0.5 * self.dt * k_2_Omega
        k_3_Omega = self.computeRK4Step(k_2_Theta)

        k_4_Theta = self.omega + 0.5 * self.dt * k_3_Omega
        k_4_Omega = self.computeRK4Step(k_3_Theta)

        theta_new = self.theta + self.dt / 6 *(k_1_Theta + 2 * k_2_Theta + 2 * k_3_Theta + k_4_Theta)
        omega_new = self.omega + self.dt / 6 *(k_1_Omega + 2 * k_2_Omega + 2 * k_3_Omega + k_4_Omega)

        self.setVelocity(omega_new)
        self.setTheta(theta_new)
        return
    
    def is_slack(self):
        v_squared = (self.length * self.omega) ** 2
        tension = v_squared / self.length + self.GRAVITY * math.cos(self.theta)
        self.setSlack(tension <= 0)
        return



    


    
    

    

