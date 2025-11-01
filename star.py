from manim import *
import numpy as np

class Star(Scene):
    def construct(self):
        arm_length = 5
        angle_degrees = [90, 30, 150]  # vertical, and 60° left/right
        color = "#AFCBCF"
        width = 3

        arms = VGroup()

        for deg in angle_degrees:
            angle_rad = np.radians(deg)
            direction = np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            start = -direction * (arm_length / 2)
            end = direction * (arm_length / 2)
            arm = Line(start, end, stroke_color=color, stroke_width=width)
            arms.add(arm)

        self.play(Create(arms))
        self.wait(2)
