// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.CommandScheduler;
import frc.robot.command.DriveCommand;
import frc.robot.command.MobilityPointAutoCommand;
import frc.robot.subsystems.DriveBase;

/**
 * The VM is configured to automatically run this class, and to call the functions corresponding to
 * each mode, as described in the TimedRobot documentation. If you change the name of this class or
 * the package after creating this project, you must also update the build.gradle file in the
 * project.
 */
public class Robot extends TimedRobot {
    private final SendableChooser<String> m_chooser = new SendableChooser<>();
    private static final String kDefaultAuto = "Default";
    private static final String kMobileOpen = "Mobility Open Side";
    private static final String kMobileBump = "Mobility Bump Side";

    private final DriveCommand driveCommand;
    private final MobilityPointAutoCommand autoOpen;
    private final MobilityPointAutoCommand autoBump;

    DriveBase driveBase;

    public Robot() {
        driveBase = new DriveBase();

        XboxController controller = new XboxController(0);
        driveCommand = new DriveCommand(driveBase, controller);
        autoOpen = new MobilityPointAutoCommand(driveBase, 1.1);
        autoBump = new MobilityPointAutoCommand(driveBase, 1.5);
    }

    /**
     * This function is run when the robot is first started up and should be used for any
     * initialization code.
     */
    @Override
    public void robotInit() {
        m_chooser.setDefaultOption("Default Auto", kDefaultAuto);
        m_chooser.addOption("Mobility: Open side", kMobileOpen);
        m_chooser.addOption("Mobility: Bump side", kMobileBump);
        SmartDashboard.putData("Auto choices", m_chooser);

        driveBase.configMotors();
        CommandScheduler.getInstance().setDefaultCommand(driveBase, driveCommand);
    }

    /**
     * This function is called every 20 ms, no matter the mode. Use this for items like diagnostics
     * that you want ran during disabled, autonomous, teleoperated and test.
     *
     * <p>This runs after the mode specific periodic functions, but before LiveWindow and
     * SmartDashboard integrated updating.
     */
    @Override
    public void robotPeriodic() {
        CommandScheduler.getInstance().run();
    }

    /**
     * This autonomous (along with the chooser code above) shows how to select between different
     * autonomous modes using the dashboard. The sendable chooser code works with the Java
     * SmartDashboard. If you prefer the LabVIEW Dashboard, remove all of the chooser code and
     * uncomment the getString line to get the auto name from the text box below the Gyro
     *
     * <p>You can add additional auto modes by adding additional comparisons to the switch structure
     * below with additional strings. If using the SendableChooser make sure to add them to the
     * chooser code above as well.
     */
    @Override
    public void autonomousInit() {
        String m_autoSelected = m_chooser.getSelected();
        // m_autoSelected = SmartDashboard.getString("Auto Selector", kDefaultAuto);
        System.out.println("Auto selected: " + m_autoSelected);
        switch (m_autoSelected) {
            case kMobileOpen:
                autoOpen.schedule();
                break;
            case kMobileBump:
                autoBump.schedule();
                break;
            case kDefaultAuto:
            default:
                // Do nothing
                break;
        }
    }

    /**
     * This function is called periodically during autonomous.
     */
    @Override
    public void autonomousPeriodic() {
    }

    /**
     * This function is called once when teleop is enabled.
     */
    @Override
    public void teleopInit() {
    }

    /**
     * This function is called periodically during operator control.
     */
    @Override
    public void teleopPeriodic() {



    }

    /**
     * This function is called once when the robot is disabled.
     */
    @Override
    public void disabledInit() {
        driveBase.stop();
    }

    /**
     * This function is called periodically when disabled.
     */
    @Override
    public void disabledPeriodic() {
    }

    /**
     * This function is called once when test mode is enabled.
     */
    @Override
    public void testInit() {
    }

    /**
     * This function is called periodically during test mode.
     */
    @Override
    public void testPeriodic() {
    }

    /**
     * This function is called once when the robot is first started up.
     */
    @Override
    public void simulationInit() {
    }

    /**
     * This function is called periodically whilst in simulation.
     */
    @Override
    public void simulationPeriodic() {
    }
}
