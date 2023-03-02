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
import typing

import wpilib.simulation

from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units
from wpilib.simulation import SimDeviceSim
from wpimath._controls._controls.plant import DCMotor, LinearSystemId

import constants

if typing.TYPE_CHECKING:
    from robot import Robot


class PhysicsEngine:
    """
    Simulates a motor moving something that strikes two limit switches,
    one on each end of the track. Obviously, this is not particularly
    realistic, but it's good enough to illustrate the point
    """

    def __init__(self, physics_controller: PhysicsInterface, robot: "Robot"):
        robot.is_simulating = True

        self.physics_controller = physics_controller

        self.pdu_sim = wpilib.simulation.PowerDistributionSim(robot.pdu)

        self.dio1 = wpilib.simulation.DIOSim(1)
        self.dio2 = wpilib.simulation.DIOSim(2)
        self.ain2 = wpilib.simulation.AnalogInputSim(2)

        self.motor = wpilib.simulation.PWMSim(4)

        # Gyro
        self.gyro = wpilib.simulation.AnalogGyroSim(1)

        self.position = 0

        # Change these parameters to fit your robot!
        bumper_width = 2.75 * units.inch

        # fmt: off
        # self.drivetrain = tankmodel.TankModel.theory(
        #     motor_cfgs.MOTOR_CFG_CIM,  # motor configuration
        #     116 * units.lbs,  # robot mass
        #     10.71,  # drivetrain gear ratio
        #     2,  # motors per side
        #     5 * units.inch,  # robot wheelbase
        #     16 * units.inch + bumper_width * 2,  # robot width
        #     17 * units.inch + bumper_width * 2,  # robot length
        #     5 * units.inch,  # wheel diameter
        # )
        # fmt: on

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

        self.left_motor = SimDeviceSim("SPARK MAX [10]")
        self.left_motor_output = self.left_motor.getDouble("Applied Output")
        self.right_motor = SimDeviceSim("SPARK MAX [40]")
        self.right_motor_output = self.right_motor.getDouble("Applied Output")

    def update_sim(self, now: float, tm_diff: float) -> None:
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """

        # Simulate the drivetrain
        l_motor = self.left_motor_output.get()
        r_motor = self.right_motor_output.get()

        # Update driving simulator based on motor output
        self.drivesim.setInputs(l_motor, r_motor)
        self.drivesim.update(tm_diff)

        # Get simulated pose
        pose = self.drivesim.getPose()

        # Actually update the UI
        self.physics_controller.field.setRobotPose(pose)

        # transform = self.drivetrain.calculate(l_motor, r_motor, tm_diff)
        # pose = self.physics_controller.move_robot(transform)

        # Update the gyro simulation
        # -> FRC gyros are positive clockwise, but the returned pose is positive
        #    counter-clockwise
        # self.gyro.setAngle(-pose.rotation().degrees())

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
