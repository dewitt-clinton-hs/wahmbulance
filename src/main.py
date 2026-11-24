# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       student                                                      #
# 	Created:      11/13/2026, 2:58:06 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

brain = Brain()
controller = Controller()

def pre_autonomous():

    # I put all these in an object so it's more organized
    class Wahmbulance:
        def __init__(self):

            # Initialize all wheels
            self.front_left = Motor(Ports.PORT9, True) # The True arg reverses the motor direction, which has to be done since the motor was screwed into the robot reversed, so this undoes it
            self.front_right = Motor(Ports.PORT2)
            self.back_left = Motor(Ports.PORT10, True)
            self.back_right = Motor(Ports.PORT1)

            self.stretch_motor = Motor(Ports.PORT20) # Motor in charge of the stretcher
            self.stretch_motor.reset_position() # Set the position of the stretcher to 0 on initialization

            # Set the max torque for all motors to 40% to avoid overheating due to friction
            self.front_left.set_max_torque(40, PERCENT)
            self.front_right.set_max_torque(40, PERCENT)
            self.back_left.set_max_torque(40, PERCENT)
            self.back_right.set_max_torque(40, PERCENT)
            self.stretch_motor.set_max_torque(40, PERCENT)

        def drive(self, tilt_degree, wait=True):
            rpm = tilt_degree * 1.5 # y = 1.5x, where y is rpm and x is the amount the joystick is tilted

            # Spin all wheels in a given direction
            # The base direction is FORWARD, but if the RPM of the wheels is negative, direction reverses
            self.front_left.spin(FORWARD, rpm, wait)
            self.front_right.spin(FORWARD, rpm, wait)
            self.back_left.spin(FORWARD, rpm, wait)
            self.back_right.spin(FORWARD, rpm, wait)

        def turn(self, tilt_degree_l, tilt_degree_r):
        
            # By having a different measurement for each stick, the turn's intensity changes based on the right stick 
            # but the initial velocity prior to the turn is kept
            # May need testing
            rpm_l = tilt_degree_l * 1.5
            rpm_r = tilt_degree_r * 1.5

            # If the front left wheel and the back right wheel spin in opposite directions, the robot will turn whichever direction the RPM is (positiive forward, negative backward)
            # The center of gravity of the turn should be in the center of the robot, I might change this later
            # The front left wheel will spin with the initial velocity the robot is driving at
            # The back right wheel will spin in reverse with the intensity of the turn based on how hard the right stick is tilted
            self.front_left.spin(FORWARD, rpm_l)
            self.back_right.spin(REVERSE, rpm_r)

            # By spinning the wheels next to them in the reverse direction, the turn the original wheels produce is aided
            # The turn will be dulled by the friction of the floor if these wheels stay still, I also might change this later
            # I have to test this bit to see if I'm correct about the directions these wheels should spin to aid the turn, and the way that affects the cente of gravity
            # These wheels turn with the speed of the right stick to aid in intensity
            self.front_right.spin(REVERSE, rpm_r)
            self.back_left.spin(FORWARD, rpm_r)

        def stretch(self, button=0): # button=1 is R1, button=2 is L1
            
            if button == 1: # If L1
                self.stretch_motor.spin_to_position(100, PERCENT, 25, PERCENT) # Spin to 600 degrees at 25% speed
            elif button == 2: # If R2
                self.stretch_motor.spin_to_position(0, PERCENT, 25, PERCENT) # Spin back to 0 at 25% speed
                self.stretch_motor.reset_position() # Reset the position so that the current position is known as 0
            else:
                wait(1, SECONDS) # Wait for 2 seconds so gravity can bring the stretcher back down
                self.stretch_motor.reset_position() # Reset the position

        def check_move(self, left_vertical, right_horizontal, stretch_up, stretch_down):
            pass           

    global wahmbulance
    wahmbulance = Wahmbulance()

def autonomous():
    pass

def user_control():
    while True: # While true to consistently check the changing values on the robot (joystick position, etc.)
        pass

comp = Competition(user_control, autonomous) # Put both function in a Competition object so they can be called by the external VEX device
pre_autonomous()