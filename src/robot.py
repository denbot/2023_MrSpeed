# ----------------------------------------------------------------------------
# Copyright (c) 2017-2018 FIRST. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.
# ----------------------------------------------------------------------------

import rev
import wpilib
import wpilib.drive
from wpilib.drive import DifferentialDrive


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        self.leftLeadMotor = rev.CANSparkMax(10, rev.CANSparkMax.MotorType.kBrushless)
        self.rightLeadMotor = rev.CANSparkMax(40, rev.CANSparkMax.MotorType.kBrushless)
        self.leftFollowMotor = rev.CANSparkMax(20, rev.CANSparkMax.MotorType.kBrushless)
        self.rightFollowMotor = rev.CANSparkMax(30, rev.CANSparkMax.MotorType.kBrushless)

        # Passing in the lead motors into DifferentialDrive allows any
        # commmands sent to the lead motors to be sent to the follower motors.
        self.driveTrain = DifferentialDrive(self.leftLeadMotor, self.rightLeadMotor)
        self.joystick = wpilib.Joystick(0)
        
        # The RestoreFactoryDefaults method can be used to reset the
        # configuration parameters in the SPARK MAX to their factory default
        # state. If no argument is passed, these parameters will not persist
        # between power cycles
        self.leftLeadMotor.restoreFactoryDefaults()
        self.rightLeadMotor.restoreFactoryDefaults()
        self.leftFollowMotor.restoreFactoryDefaults()
        self.rightFollowMotor.restoreFactoryDefaults()

        # In CAN mode, one SPARK MAX can be configured to follow another. This
        # is done by calling the follow() method on the SPARK MAX you want to
        # configure as a follower, and by passing as a parameter the SPARK MAX
        # you want to configure as a leader.
        #
        # One motor on each side of our drive train is configured to follow a lead motor.
        self.leftFollowMotor.follow(self.leftLeadMotor)
        self.rightFollowMotor.follow(self.rightLeadMotor)

    def teleopPeriodic(self):
        # Drive with arcade style
        self.driveTrain.arcadeDrive(self.joystick.getX() / 3, self.joystick.getY() / 3)

if __name__ == "__main__":
    wpilib.run(Robot)
