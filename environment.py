from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

# Initialize the figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Leave space for the slider
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title("Click to place a red marker")

# Add a slider for marker size
ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
slider = Slider(ax_slider, 'Size', 1, 10, valinit=5)

previous_marker = [None]  # Store the previous marker (initially None)


# Event handler for mouse clicks
def on_click(event):
    if event.inaxes == ax:
        # Remove the previous marker if it exists
        if previous_marker[0] is not None:
            previous_marker[0].remove()

        # Add a new marker at the clicked position
        previous_marker[0] = ax.plot(event.xdata, event.ydata, 'ro')[0]

        # Update the canvas to show the new marker
        fig.canvas.draw()

# Connect the click event
fig.canvas.mpl_connect('button_press_event', on_click)

# Show the plot
plt.show()
