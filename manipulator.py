import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Initialize figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Adjust space for the slider

# Coordinates for the joints and links
joints = [(0, 0), (0.5, 1), (1.5, 1), (2, 0.5), (2.5, 1)]
links = [(0, 1), (1, 2), (2, 3), (3, 4)]

# Plot links
for start, end in links:
    x = [joints[start][0], joints[end][0]]
    y = [joints[start][1], joints[end][1]]
    ax.plot(x, y, 'k-', lw=3)

# Plot joints
for x, y in joints:
    ax.plot(x, y, 'wo', markersize=10, markeredgecolor='k', markeredgewidth=2)

# Add learning rate text
learning_rate = 3.75
text = ax.text(0.5, 1.2, f"LearningRate = {learning_rate}", fontsize=12, ha='center')

# Add slider
ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])  # Position of the slider
slider = Slider(ax_slider, 'Learning Rate', 0.1, 5.0, valinit=learning_rate, valstep=0.1)

# Update function for the slider
def update(val):
    new_rate = slider.val
    text.set_text(f"LearningRate = {new_rate:.2f}")
    fig.canvas.draw_idle()

slider.on_changed(update)

# Customize axes
ax.set_xlim(-1, 3)
ax.set_ylim(-1, 2)
ax.set_aspect('equal', adjustable='datalim')
ax.axis('off')

plt.show()
