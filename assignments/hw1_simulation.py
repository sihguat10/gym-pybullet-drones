"""Simulation script for assignment 1.
The script uses the control defined in file "hw_control.py".

Example:
    To run the simulation, type in a terminal

        $ python hw1_simulation.py
"""
import time
import numpy as np
from gym_pybullet_drones.envs.CtrlAviary import CtrlAviary
from gym_pybullet_drones.utils.Logger import Logger
from gym_pybullet_drones.utils.utils import sync
from hw1_control import HW1Control

DURATION = 10 # int: the duration of the simulation in seconds
GUI = True # bool: whether to use PyBullet graphical interface

if __name__ == "__main__":

    #### Create the ENVironment ################################
    ENV = CtrlAviary(gui=GUI)

    #### Initialize the LOGGER #################################
    LOGGER = Logger(logging_freq_hz=ENV.SIM_FREQ)

    #### Initialize the controller #############################
    CTRL = HW1Control(ENV)

    #### Initialize the ACTION #################################
    ACTION = {}
    OBS = ENV.reset()
    STATE = OBS["0"]["state"]
    ACTION["0"] = CTRL.compute_control(current_position=STATE[0:3],
                                       current_quaternion=STATE[3:7],
                                       current_velocity=STATE[10:13],
                                       current_angular_velocity=STATE[13:16],
                                       target_position=STATE[0:3],
                                       target_velocity=np.zeros(3)
                                       )

    #### Initialize target trajectory ##########################
    TARGET_TRAJECTORY = np.array([[np.sin(i*((2*np.pi)/(DURATION*ENV.SIM_FREQ))), 0, STATE[2]] for i in range(DURATION*ENV.SIM_FREQ)])
    TARGET_VELOCITY = np.zeros([DURATION*ENV.SIM_FREQ, 3])

    #### Run the simulation ####################################
    START = time.time()
    for i in range(0, DURATION*ENV.SIM_FREQ):

        #### Step the simulation ###################################
        OBS, _, _, _ = ENV.step(ACTION)

        #### Compute control #######################################
        STATE = OBS["0"]["state"]
        ACTION["0"] = CTRL.compute_control(current_position=STATE[0:3],
                                           current_quaternion=STATE[3:7],
                                           current_velocity=STATE[10:13],
                                           current_angular_velocity=STATE[13:16],
                                           target_position=TARGET_TRAJECTORY[i, :],
                                           target_velocity=TARGET_VELOCITY[i, :]
                                           )

        #### Log the simulation ####################################
        LOGGER.log(drone=0, timestamp=i/ENV.SIM_FREQ, state=STATE)

        #### Printout ##############################################
        if i%ENV.SIM_FREQ == 0:
            ENV.render()

        #### Sync the simulation ###################################
        if GUI:
            sync(i, START, ENV.TIMESTEP)

    #### Close the ENVironment #################################
    ENV.close()

    #### Plot the simulation results ###########################
    LOGGER.plot()
