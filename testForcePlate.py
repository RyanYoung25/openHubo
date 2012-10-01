#!/usr/bin/env python
from openravepy import *
import time
import numpy
import tab

def setJoints(robot,refPos):
    for x in refPos.keys():
        #print "setting joint ",x,"to angle ",refPos[x]
        ind=robot.GetJointIndex(x)
        #This command has less overhead than a full set of angles, though maybe
        # not for only manipulator
        cmd="setpos1 {0} {1}".format(ind,refPos[x])
        #print cmd
        robot.GetController().SendCommand(cmd)

if __name__ == "__main__":
    
    env = Environment()
    env.SetViewer('qtcoin')
    env.Load('forcePlate.env.xml') 
    
    #The first robot defined in the XML file is Jaemi Hubo
    robot = env.GetRobots()[0]
    #The second "robot" is the force plate, which is grossly oversized to
    #prevent weird collision issues, like the plates completely intersecting
    #each other.
    plate = env.GetRobots()[1]
    forceSensor = robot.GetAttachedSensors()[0].GetSensor()

    force = 0
    torque = 0
    sumForce = 0
    sumTorque = 0
    sumForceBody = 0
    sumTorqueBody = 0
    with env:
        robot = env.GetRobots()[0]
        robot.SetController(RaveCreateController(env,'servocontroller'))
        collisionChecker = RaveCreateCollisionChecker(env,'bullet')
        env.SetCollisionChecker(collisionChecker)

        env.StopSimulation()
        env.StartSimulation(timestep=0.001 )

        robot.GetController().SendCommand('setpos1 0 0 ')

    for i in xrange(500):
        t=time.time();
        omega=2*numpy.pi/2
        A=numpy.sin(omega*t)*2.0
        data = forceSensor.GetSensorData()
        #tilt hips back and forth
        setJoints(robot,{'RAP':A,'LAP':A})
        #Optionally compare to the force/torque data from the force plate
        [force,torque] = env.GetPhysicsEngine().GetLinkForceTorque( plate.GetLink('Plate') )
        print data.force, data.torque
        time.sleep(.05)
