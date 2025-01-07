from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.path import Path
from matplotlib import patches


class Environment:
    def __init__(self, workspace_limits, tail_gate, learning_rate, joints, links):
        self.workspace_limits = workspace_limits
        self.tail_gate = tail_gate
        self.learning_rate = learning_rate
        self.joints = joints
        self.links = links
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)  # Adjust the bottom to make space for the slider
        #self.ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])  # Position of the slider
        #self.slider = Slider(self.ax_slider, 'Learning Rate', 0.1, 5.0, valinit=1.0, valstep=0.1)
        self.previous_marker = [None]  # Store the previous marker (initially None)
        self.tail_gate_polygon = Path(self.tail_gate)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def setup_environment(self):
        # Initialize the figure and axes

        # Set the aspect ratio of the plot
        self.ax.set_aspect('equal', adjustable='datalim')
        
        # Set the axes limits
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-1, 6)
        
        # Turn off the axes
        self.ax.axis('on')
        
    
    def plot_base(self):
        base_width = 1.2
        base_height = 0.3
        self.ax.add_patch(
            patches.Rectangle((self.joints[0][0] - base_width/2, self.joints[0][1] - base_height/2), 
                            base_width, base_height, linewidth=1, edgecolor='gray', facecolor='gray'))
    
    def plot_links(self):
        # Function to plot the links
        for start, end in zip(self.joints[:-1], self.joints[1:]):
            x = [start[0], end[0]]
            y = [start[1], end[1]]
            self.ax.plot(x, y, 'k-', lw=3)
            
    def plot_joints(self):
        # Function to plot the joints
        for x, y in self.joints:
            self.ax.plot(x, y, 'wh', markersize=10, markeredgecolor='k', markeredgewidth=2)
            self.ax.plot(x, y, 'o', markersize=2, markeredgecolor='black', markeredgewidth=2)
        self.ax.plot(self.joints[-1][0], self.joints[-1][1], 'wo', markersize=10, markeredgecolor='k', markeredgewidth=2)

    def plot_tail_gate(self):
        # Function to plot the tail gate
        for i in range(len(self.tail_gate)):
            start = self.tail_gate[i]
            end = self.tail_gate[(i + 1) % len(self.tail_gate)]  # Connect back to the first point
            x = [start[0], end[0]]
            y = [start[1], end[1]]
            self.ax.plot(x, y, 'k-', lw=1, color='gray')
            
    def on_click(self, event):
        if event.inaxes == self.ax:
            # Check if the clicked point is within the tail gate polygon
            if self.tail_gate_polygon.contains_point((event.xdata, event.ydata)):
                # Remove the previous marker if it exists
                if self.previous_marker[0] is not None:
                    self.previous_marker[0].remove()

                # Add a new marker at the clicked position
                self.previous_marker[0] = self.ax.plot(event.xdata, event.ydata, 'ro')[0]

                # Update the canvas to show the new marker
                self.fig.canvas.draw()

    def show(self):
        plt.show()

def main():
    # Define the workspace limits
    workspace_limits = {'x': (-5, 5), 'y': (-1, 6)}

    # Define the tail gate
    tail_gate = [(-2, 1.3), (-1.5, 2.3), (1.5, 2.3), (1.3, 1.3)]

    # Define the learning rate
    learning_rate = 0.1

    # Define the joints and links
    joints = [(0, 5), (0, 4), (-1, 3), (-1, 2), (0, 1.8)]  # robot joints
    links = [(0, 1), (1, 2), (2, 3), (3, 4)]

    # Initialize the Environment
    cell = Environment(workspace_limits, tail_gate, learning_rate, joints, links)
    cell.setup_environment()
    cell.plot_base()
    cell.plot_links()
    cell.plot_joints()
    cell.plot_tail_gate()
    cell.show()
    
if __name__ == "__main__":
    main()
