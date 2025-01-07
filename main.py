from robot_arm import RobotArm
from polishing_cell import Environment
from planning import PathPlanning

def main():
    # Initialize robot arm
    robot = RobotArm(
        L1=1.5,
        L2=1.0,
        L3=1.0,
        joint_angles=[0.0, 0.0, 0.0],
        base_position=(0.0, 0.0, 0.0),
    )

    # Initialize environment
    workspace_limits = {'x': (-2, 2), 'y': (-2, 2), 'z': (0, 2)}
    env = Environment(workspace_limits)
    env.setup_environment()

    # Target point for the robot
    target_point = (1.0, 1.0, 0.5)

    # Initialize path planner
    planner = PathPlanning(
        robot=robot,
        learning_rate=0.1,
        max_iterations=1000,
        tolerance=0.01,
    )

    # Perform path planning
    planner.gradient_descent(target_point)

    # Plot the final configuration
    env.plot_robot(robot)
    env.show()

if __name__ == "__main__":
    main()
