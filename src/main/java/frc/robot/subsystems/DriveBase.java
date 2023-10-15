package frc.robot.subsystems;

import com.revrobotics.CANSparkMax;
import com.revrobotics.CANSparkMaxLowLevel;
import edu.wpi.first.wpilibj.drive.DifferentialDrive;
import edu.wpi.first.wpilibj2.command.SubsystemBase;

public class DriveBase extends SubsystemBase {
    private final CANSparkMax backLeftDrive;
    private final CANSparkMax backRightDrive;
    private final CANSparkMax frontLeftDrive;
    private final CANSparkMax frontRightDrive;

    private final DifferentialDrive drive;

    public DriveBase() {
        backLeftDrive = new CANSparkMax(2, CANSparkMaxLowLevel.MotorType.kBrushless);
        backRightDrive = new CANSparkMax(3, CANSparkMaxLowLevel.MotorType.kBrushless);
        frontLeftDrive = new CANSparkMax(1, CANSparkMaxLowLevel.MotorType.kBrushless);
        frontRightDrive = new CANSparkMax(4, CANSparkMaxLowLevel.MotorType.kBrushless);

        drive = new DifferentialDrive(backLeftDrive, backRightDrive);
    }

    public void arcadeDrive(double forward, double turn) {
        drive.arcadeDrive(forward, turn);
    }

    public void configMotors() {
        frontLeftDrive.follow(backLeftDrive);
        frontRightDrive.follow(backRightDrive);

        backLeftDrive.setInverted(true);
        frontLeftDrive.setInverted(true);

        CANSparkMax.IdleMode idleMode = CANSparkMax.IdleMode.kBrake;

        frontLeftDrive.setIdleMode(idleMode);
        frontRightDrive.setIdleMode(idleMode);
        backLeftDrive.setIdleMode(idleMode);
        backRightDrive.setIdleMode(idleMode);

        frontLeftDrive.setSmartCurrentLimit(30);
        frontRightDrive.setSmartCurrentLimit(30);
        backLeftDrive.setSmartCurrentLimit(30);
        backRightDrive.setSmartCurrentLimit(30);
    }

    public void stop() {
        backLeftDrive.set(0);
        backRightDrive.set(0);
        frontLeftDrive.set(0);
        frontRightDrive.set(0);
    }
}
