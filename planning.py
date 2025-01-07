import numpy as np
import matplotlib.pyplot as plt

# Robot arm parameters
L1, L2, L3 = 1.5, 1.0, 1.0  # Link lengths
joint_angles = np.radians([45, 30, 0])  # Initial joint angles [theta1, theta2, theta3]

# Fixed base position
base_position = [0.0, 0.0]

# Target point (red point on the tail gate)
target_point = [2.5, 1.5]

# Learning rate and optimization parameters
learning_rate = 0.1
max_iterations = 1000
tolerance = 1e-3

# Forward kinematics to compute end-effector position
def forward_kinematics(angles):
    theta1, theta2, theta3 = angles
    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)
    x2 = x1 + L2 * np.cos(theta1 + theta2)
    y2 = y1 + L2 * np.sin(theta1 + theta2)
    x3 = x2 + L3 * np.cos(theta1 + theta2 + theta3)
    y3 = y2 + L3 * np.sin(theta1 + theta2 + theta3)
    return np.array([x3, y3]), [[0, x1, x2, x3], [0, y1, y2, y3]]

# Loss function (distance between end-effector and target)
def compute_loss(end_effector, target):
    return np.linalg.norm(end_effector - target)

# Compute gradients for joint angles
def compute_gradients(angles, target):
    theta1, theta2, theta3 = angles
    end_effector, _ = forward_kinematics(angles)
    x_end, y_end = end_effector
    x_target, y_target = target

    # Partial derivatives of the loss w.r.t joint angles
    dL_dx = 2 * (x_end - x_target)
    dL_dy = 2 * (y_end - y_target)

    # Gradients using the Jacobian matrix
    dtheta1 = -dL_dx * (-L1 * np.sin(theta1) - L2 * np.sin(theta1 + theta2) - L3 * np.sin(theta1 + theta2 + theta3)) \
              - dL_dy * (L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2) + L3 * np.cos(theta1 + theta2 + theta3))
    dtheta2 = -dL_dx * (-L2 * np.sin(theta1 + theta2) - L3 * np.sin(theta1 + theta2 + theta3)) \
              - dL_dy * (L2 * np.cos(theta1 + theta2) + L3 * np.cos(theta1 + theta2 + theta3))
    dtheta3 = -dL_dx * (-L3 * np.sin(theta1 + theta2 + theta3)) \
              - dL_dy * (L3 * np.cos(theta1 + theta2 + theta3))

    return np.array([dtheta1, dtheta2, dtheta3])

# Gradient descent loop
for i in range(max_iterations):
    # Compute the current position of the end-effector
    end_effector, link_positions = forward_kinematics(joint_angles)

    # Compute the loss
    loss = compute_loss(end_effector, target_point)

    # Check for convergence
    if loss < tolerance:
        print(f"Converged after {i} iterations.")
        break

    # Compute gradients
    gradients = compute_gradients(joint_angles, target_point)

    # Update joint angles
    joint_angles -= learning_rate * gradients

    # Clamp joint angles within physical limits (optional)
    joint_angles = np.clip(joint_angles, np.radians(-90), np.radians(90))

    # Print loss for debugging
    if i % 50 == 0:
        print(f"Iteration {i}: Loss = {loss:.4f}")

# Final results
final_position, link_positions = forward_kinematics(joint_angles)
print(f"Final joint angles (degrees): {np.degrees(joint_angles)}")
print(f"Final position: {final_position}")
print(f"Target point: {target_point}")

# Visualization
fig, ax = plt.subplots()
ax.set_xlim(-L1 - L2 - L3, L1 + L2 + L3)
ax.set_ylim(-L1 - L2 - L3, L1 + L2 + L3)
ax.set_aspect('equal', 'box')

# Plot robot arm
ax.plot(link_positions[0], link_positions[1], 'o-', color='blue', label="Robot Arm")

# Plot target point
ax.plot(target_point[0], target_point[1], 'rx', label="Target Point")

# Draw the tail gate
tail_gate = plt.Rectangle((1.5, 1), 2.0, 1.0, fill=None, edgecolor='gray', linewidth=1.5)
ax.add_patch(tail_gate)

ax.legend()
plt.show()
