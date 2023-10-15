package frc.robot.command;

import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.subsystems.DriveBase;

public class DriveCommand extends CommandBase {
    private final DriveBase driveBase;
    private final XboxController controller;

    public DriveCommand(DriveBase driveBase, XboxController controller) {
        this.driveBase = driveBase;
        this.controller = controller;

        addRequirements(driveBase);
    }

    @Override
    public void execute() {
        double forward = controller.getLeftY();
        double turn = controller.getRightX() * 0.5;

        double left = controller.getLeftY();
        double right = controller.getRightY();

        // drive.tankDrive(left, right, true);
        double scale;
        if(controller.getLeftTriggerAxis() > 0.5) {
            scale = 0.4;
        } else if(controller.getRightTriggerAxis() > 0.5) {
            scale = 0.75;  // Max power
        } else {
            scale = 0.6;  // Default power
        }

        driveBase.arcadeDrive(forward * scale, turn);
    }
}
