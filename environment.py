from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.patches as patches
from matplotlib.path import Path


# Initialize the figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Leave space for the slider
#ax.set_title("Click to place a red marker")

# Coordinates for the joints and links
joints = [(0, 5), (0, 4), (-1, 3), (-1, 2), (0, 1.8)]
links = [(0, 1), (1, 2), (2, 3), (3, 4)]
tail_gate = [(-0.7, 0.5), (0.5, 2.5), (4.7, 2.5), (3.5, 0.5)]

# Plot the base
base_width = 1.2
base_height = 0.3
ax.add_patch(
    patches.Rectangle((joints[0][0] - base_width/2, joints[0][1] - base_height/2), 
                      base_width, base_height, linewidth=1, edgecolor='gray', facecolor='gray'))

# Plot links
for start, end in links:
    x = [joints[start][0], joints[end][0]]
    y = [joints[start][1], joints[end][1]]
    ax.plot(x, y, 'k-', lw=3)

# Plot joints
for x, y in joints[:-1]:
    ax.plot(x, y, 'wh', markersize=10, markeredgecolor='k', markeredgewidth=2)
    ax.plot(x, y, 'o', markersize=2, markeredgecolor='black', markeredgewidth=2)
ax.plot(joints[-1][0], joints[-1][1], 'wo', markersize=10, markeredgecolor='k', markeredgewidth=2)


# Plot the tail gate
for i in range(len(tail_gate)):
    start = tail_gate[i]
    end = tail_gate[(i + 1) % len(tail_gate)]  # Connect back to the first point
    x = [start[0], end[0]]
    y = [start[1], end[1]]
    ax.plot(x, y, 'k-', lw=1, color='gray')

# Define the tail gate polygon using Path
tail_gate_polygon = Path(tail_gate)

# Add learning rate text
learning_rate = 3.75

# Add slider
ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])  # Position of the slider
slider = Slider(ax_slider, 'Learning Rate', 0.1, 5.0, valinit=learning_rate, valstep=0.1)

previous_marker = [None]  # Store the previous marker (initially None)

# Update function for the slider
def update(val):
    pass

# Event handler for mouse clicks
def on_click(event):
    if event.inaxes == ax:
        # Check if the clicked point is within the tail gate polygon
        if tail_gate_polygon.contains_point((event.xdata, event.ydata)):
            # Remove the previous marker if it exists
            if previous_marker[0] is not None:
                previous_marker[0].remove()

            # Add a new marker at the clicked position
            previous_marker[0] = ax.plot(event.xdata, event.ydata, 'ro')[0]

            # Update the canvas to show the new marker
            fig.canvas.draw()

# Connect the click event
fig.canvas.mpl_connect('button_press_event', on_click)

slider.on_changed(update)

# Customize axes
ax.set_xlim(-5, 5)
ax.set_ylim(-1, 6)
ax.set_aspect('equal', adjustable='datalim')
ax.axis('off')
plt.show()
