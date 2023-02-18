#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#
import inspect
import traceback
import typing

import wpilib.simulation

from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units
from wpimath._controls._controls.plant import LinearSystemId, DCMotor

import constants

if typing.TYPE_CHECKING:
    from src.robot import Robot


class PhysicsEngine:
    """
    Simulates a motor moving something that strikes two limit switches,
    one on each end of the track. Obviously, this is not particularly
    realistic, but it's good enough to illustrate the point
    """

    def __init__(self, physics_controller: PhysicsInterface, robot: "Robot"):
        self.physics_controller = physics_controller

        # Joystick
        self.joystick = wpilib.simulation.JoystickSim(robot.joystick)

        # Motors
        self.l_motor = wpilib.simulation.PWMSim(10)
        self.r_motor = wpilib.simulation.PWMSim(40)
        self.l_motor_sim = wpilib.simulation.DCMotorSim(DCMotor.NEO(), 0.25, 0.00005)

        self.dio1 = wpilib.simulation.DIOSim(1)
        self.dio2 = wpilib.simulation.DIOSim(2)
        self.ain2 = wpilib.simulation.AnalogInputSim(2)

        self.motor = wpilib.simulation.PWMSim(4)

        # Gyro
        self.gyro = wpilib.simulation.AnalogGyroSim(1)

        self.position = 0

        # Change these parameters to fit your robot!
        bumper_width = 2.75 * units.inch
        # self.drivetrain = robot.driveTrain

        # fmt: off
        system = LinearSystemId.identifyDrivetrainSystem(
            constants.kV_linear,
            constants.kA_linear,
            constants.kV_angular,
            constants.kA_angular,
        )

        self.drivesim = wpilib.simulation.DifferentialDrivetrainSim(
            system,
            # The robot's trackwidth, which is the distance between the wheels on the left side
            # and those on the right side. The units is meters.
            constants.kTrackWidth,
            DCMotor.CIM(10),
            10.71,
            # The radius of the drivetrain wheels in meters.
            constants.kWheelRadius,
        )
        # fmt: on

    def update_sim(self, now: float, tm_diff: float) -> None:
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """

        voltage = wpilib.simulation.RoboRioSim.getVInVoltage()

        # self.l_motor_sim.update(tm_diff)

        # Simulate the drivetrain
        l_motor = self.l_motor.getSpeed() * voltage
        r_motor = self.r_motor.getSpeed() * voltage

        print(l_motor, r_motor)

        self.l_motor_sim.setInputVoltage(l_motor)
        self.l_motor_sim.update(tm_diff)

        self.drivesim.setInputs(l_motor, r_motor)
        self.drivesim.update(tm_diff)

        # transform = self.drivesim.calculate(l_motor, r_motor, tm_diff)
        # pose = self.physics_controller.move_robot(transform)
        pose = self.drivesim.getPose()
        self.physics_controller.field.setRobotPose(pose)

        # Update the gyro simulation
        # -> FRC gyros are positive clockwise, but the returned pose is positive
        #    counter-clockwise
        self.gyro.setAngle(-pose.rotation().degrees())

        # update position (use tm_diff so the rate is constant)
        self.position += self.motor.getSpeed() * tm_diff * 3

        # update limit switches based on position
        if self.position <= 0:
            switch1 = True
            switch2 = False

        elif self.position > 10:
            switch1 = False
            switch2 = True

        else:
            switch1 = False
            switch2 = False

        # set values here
        self.dio1.setValue(switch1)
        self.dio2.setValue(switch2)
        self.ain2.setVoltage(self.position)