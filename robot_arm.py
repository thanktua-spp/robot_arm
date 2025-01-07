import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.path import Path
import matplotlib.patches as patches


class Robot:
    def __init__(self, joint_angles, links, tail_gate):
        self.joint_angles = joint_angles
        self.links = links


    def compute_link_lengths(self):
        link_lengths = [
            np.sqrt((self.links[i + 1][0] - self.links[i][0])**2 + (self.links[i + 1][1] - self.links[i][1])**2)
            for i in range(len(self.links) - 1)
        ]
        return link_lengths

    

def main():
    # Coordinates for the joints and links
    joints = [(0, 5), (0, 4), (-1, 3), (-1, 2), (0, 1.8)]
    links = [(0, 1), (1, 2), (2, 3), (3, 4)]
    tail_gate = [(0, 0), (1, 0), (1, 1), (0, 1)]

    robot = Robot(joints, links, tail_gate)
    link_lengths = robot.compute_link_lengths()

    # Assign the lengths to L1, L2, L3
    L1, L2, L3 = link_lengths[:3]

    print(f"Computed Link Lengths: L1 = {L1}, L2 = {L2}, L3 = {L3}")


if __name__ == "__main__":
    main()