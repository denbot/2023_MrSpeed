# ----------------------------------------------------------------------------
# Copyright (c) 2017-2018 FIRST. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.
# ----------------------------------------------------------------------------
from typing import Optional

import rev
import wpilib
import wpilib.drive
from wpilib.drive import DifferentialDrive


class Robot(wpilib.TimedRobot):
    def __init__(self):
        super().__init__()
        self.is_simulating = False

        self.pdu: Optional[wpilib.PowerDistribution] = None

        self.leftLeadMotor: Optional[rev.CANSparkMax] = None
        self.rightLeadMotor: Optional[rev.CANSparkMax] = None
        self.leftFollowMotor: Optional[rev.CANSparkMax] = None
        self.rightFollowMotor: Optional[rev.CANSparkMax] = None

        self.left: Optional[wpilib.MotorControllerGroup] = None
        self.right: Optional[wpilib.MotorControllerGroup] = None

    def robotInit(self):
        self.pdu = wpilib.PowerDistribution(50, wpilib.PowerDistribution.ModuleType.kRev)

        self.leftLeadMotor = rev.CANSparkMax(10, rev.CANSparkMax.MotorType.kBrushless)
        self.rightLeadMotor = rev.CANSparkMax(40, rev.CANSparkMax.MotorType.kBrushless)
        self.leftFollowMotor = rev.CANSparkMax(20, rev.CANSparkMax.MotorType.kBrushless)
        self.rightFollowMotor = rev.CANSparkMax(30, rev.CANSparkMax.MotorType.kBrushless)

        self.left = wpilib.MotorControllerGroup(self.leftLeadMotor, self.leftFollowMotor)
        self.right = wpilib.MotorControllerGroup(self.rightLeadMotor, self.rightFollowMotor)

        # Passing in the lead motors into DifferentialDrive allows any
        # commmands sent to the lead motors to be sent to the follower motors.
        self.driveTrain = DifferentialDrive(self.left, self.right)
        self.joystick = wpilib.Joystick(0)
        self.driveTrain.setExpiration(0.1)

        # The RestoreFactoryDefaults method can be used to reset the
        # configuration parameters in the SPARK MAX to their factory default
        # state. If no argument is passed, these parameters will not persist
        # between power cycles
        # self.leftLeadMotor.restoreFactoryDefaults()
        # self.rightLeadMotor.restoreFactoryDefaults()
        # self.leftFollowMotor.restoreFactoryDefaults()
        # self.rightFollowMotor.restoreFactoryDefaults()

        # In CAN mode, one SPARK MAX can be configured to follow another. This
        # is done by calling the follow() method on the SPARK MAX you want to
        # configure as a follower, and by passing as a parameter the SPARK MAX
        # you want to configure as a leader.
        #
        # One motor on each side of our drive train is configured to follow a lead motor.
        # self.leftFollowMotor.follow(self.leftLeadMotor)
        # self.rightFollowMotor.follow(self.rightLeadMotor)
    def teleopInit(self):
        """
        Configures appropriate robot settings for teleop mode
        """
        self.driveTrain.setSafetyEnabled(True)

    def teleopPeriodic(self):
        # Drive with arcade style
        joystick_x = -self.joystick.getX() / 3
        joystick_y = -self.joystick.getY()
        self.driveTrain.arcadeDrive(joystick_y, joystick_x)

        if self.is_simulating:  # TODO Figure out if this only works in simulation
            # TODO Replace 12 with actual bus voltage
            voltage = self.pdu.getVoltage()
            self.left.setVoltage(voltage * self.left.get())
            self.right.setVoltage(voltage * self.right.get())


if __name__ == "__main__":
    wpilib.run(Robot)
