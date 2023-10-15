package frc.robot.command;

import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.subsystems.DriveBase;

public class MobilityPointAutoCommand extends CommandBase {
    private static final double FORWARD_TIME = 0.5;
    private final double backDriveTime;

    private final DriveBase driveBase;
    private final Timer timer;

    public MobilityPointAutoCommand(DriveBase driveBase, double backDriveTime) {
        this.driveBase = driveBase;
        this.backDriveTime = backDriveTime;

        addRequirements(driveBase);

        timer = new Timer();
    }

    @Override
    public void initialize() {
        timer.start();
    }

    @Override
    public void execute() {
        if (timer.get() < FORWARD_TIME) {
            driveBase.arcadeDrive(-1, 0);
        } else if (timer.get() < FORWARD_TIME + backDriveTime) {
            driveBase.arcadeDrive(1, 0);
        } else {
            driveBase.stop();
        }
    }
}
