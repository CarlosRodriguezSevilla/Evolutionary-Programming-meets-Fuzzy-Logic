"""
A PyrobotSimulator world. A large room with two robots and
two lights.

(c) 2005, PyroRobotics.org. Licensed under the GNU GPL.
"""

from pyrobot.simulators.pysim import TkSimulator, TkPioneer, \
     PioneerFrontSonars, PioneerFrontLightSensors

def INIT():
    sim = TkSimulator((441,434), (22,420), 40.357554)
    
    sim.addBox(0, 0, 10, 10)

    sim.addLight(5, 6, 1)

    sim.addRobot(60000, TkPioneer("RedPioneer",
                                  5, 2, -0.86,
                                  ((.225, .225, -.225, -.225),
                                   (.175, -.175, -.175, .175))))
    # add some sensors:
    sim.robots[0].addDevice(PioneerFrontSonars())
    sim.robots[0].addDevice(PioneerFrontLightSensors())
    return sim
