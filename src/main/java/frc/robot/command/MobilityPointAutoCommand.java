package frc.robot.command;

import edu.wpi.first.wpilibj.Timer;
import edu.wpi.first.wpilibj2.command.CommandBase;
import frc.robot.subsystems.DriveBase;

public class MobilityPointAutoCommand extends CommandBase {
    private static final double FORWARD_TIME = 0.5;
    private static final double BACK_TIME = 0.4;
    private static final double PUSH_TIME = 0.4;
    private final double backDriveTime;
    private final boolean backAndForth;

    private final DriveBase driveBase;
    private final Timer timer;

    public MobilityPointAutoCommand(DriveBase driveBase, double backDriveTime, boolean backAndForth) {
        this.driveBase = driveBase;
        this.backDriveTime = backDriveTime;
        this.backAndForth = backAndForth;

        addRequirements(driveBase);

        timer = new Timer();
    }

    @Override
    public void initialize() {
        timer.restart();
    }

    @Override
    public void execute() {
        double currentTime = timer.get();
        currentTime -= FORWARD_TIME;
        if (currentTime < 0) {
            driveBase.arcadeDrive(-1, 0);
            return;
        }

        if (backAndForth) {
            currentTime -= BACK_TIME;
            if (currentTime < 0) {
                driveBase.arcadeDrive(.4, 0);
                return;
            }

            currentTime -= PUSH_TIME;
            if (currentTime < 0) {
                driveBase.arcadeDrive(-0.4, 0);
                return;
            }
        }

        currentTime -= backDriveTime;
        if (currentTime < 0) {
            driveBase.arcadeDrive(1, 0);
            return;
        }

        driveBase.stop();
    }
}
