import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Initial robot arm joint positions (base and end-effector included)
joints = np.array([(0, 5), (0, 4), (-1, 3), (-1, 2), (0, 1.8)])
segment_lengths = [
    np.linalg.norm(joints[i] - joints[i - 1]) for i in range(1, len(joints))
]  # Compute fixed segment lengths
tolerance = 1e-2  # Convergence tolerance for IK

target_point = None  # No initial target point


def compute_loss(end_effector, target):
    """Compute the distance between the end-effector and the target point."""
    return np.linalg.norm(np.array(end_effector) - np.array(target))


def cyclic_coordinate_descent(target, step_fraction=0.2):
    """Perform one iteration of inverse kinematics with smoother movement."""
    global joints
    for i in range(len(joints) - 1, 0, -1):
        to_end_effector = joints[-1] - joints[i - 1]
        to_target = np.array(target) - joints[i - 1]
        to_end_effector /= np.linalg.norm(to_end_effector)
        to_target /= np.linalg.norm(to_target)
        angle = np.arccos(np.clip(np.dot(to_end_effector, to_target), -1.0, 1.0))
        cross = np.cross(np.append(to_end_effector, 0), np.append(to_target, 0))
        angle = -angle if cross[2] < 0 else angle
        angle *= step_fraction  # Apply only a fraction of the rotation
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)],
        ])
        for j in range(i, len(joints)):
            joints[j] = joints[i - 1] + np.dot(
                rotation_matrix, joints[j] - joints[i - 1]
            )
    for i in range(1, len(joints)):
        direction = joints[i] - joints[i - 1]
        direction /= np.linalg.norm(direction)
        joints[i] = joints[i - 1] + direction * segment_lengths[i - 1]



def update(frame):
    """Update the robot arm configuration for the animation."""
    global joints, target_point

    # Skip the update if no target point has been clicked
    if target_point is None:
        return

    cyclic_coordinate_descent(target_point)

    ax.clear()
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal', 'box')
    ax.set_title("Robot Arm Simulation")

    # Plot the robot arm
    x_coords, y_coords = zip(*joints)
    ax.plot(x_coords, y_coords, 'o-', label="Robot Arm", color='blue')

    # Highlight the end-effector
    ax.plot(joints[-1][0], joints[-1][1], 'go', label="End Effector")

    # Plot the target point
    if target_point is not None:
        ax.plot(target_point[0], target_point[1], 'rx', label="Target Point")

    # Add legend
    ax.legend()


def on_click(event):
    """Handle mouse click events to move the robot arm."""
    global target_point
    if event.xdata is None or event.ydata is None:
        return  # Ignore clicks outside the plot area
    target_point = (event.xdata, event.ydata)
    print(f"New target point: {target_point}")


# Initialize the plot
fig, ax = plt.subplots()
ax.set_xlim(-5, 5)
ax.set_ylim(0, 6)
ax.set_aspect('equal', 'box')
ax.set_title("Robot Arm Simulation")

# Plot the initial robot arm configuration
x_coords, y_coords = zip(*joints)
ax.plot(x_coords, y_coords, 'o-', label="Robot Arm", color='blue')
ax.plot(joints[-1][0], joints[-1][1], 'go', label="End Effector")
ax.legend()

# Connect the click event
fig.canvas.mpl_connect('button_press_event', on_click)

# Set up the animation
ani = animation.FuncAnimation(fig=fig, func=update, frames=200, interval=20, blit=False)

# Show the plot
plt.show()
