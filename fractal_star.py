from manim import *
import numpy as np

class SnowflakeStar(Scene):
    def construct(self):
        arm_length = 5
        max_depth = 2
        base_color = "#AFCBCF"
        line_width = 2

        # Initial 6 arms pointing outward from origin
        segments = []
        for i in range(6):
            angle = np.radians(i * 60)
            start = np.array([0, 0, 0])
            end = start + arm_length * np.array([np.cos(angle), np.sin(angle), 0])
            segments.append((start, end))

        for _ in range(max_depth):
            new_segments = []
            for p1, p2 in segments:
                new_segments.append((p1, p2))  # keep original
                new_segments += self.add_branches(p1, p2)
            segments = new_segments

        all_lines = VGroup()
        for p1, p2 in segments:
            line = Line(p1, p2, stroke_color=base_color, stroke_width=line_width)
            all_lines.add(line)

        self.add(all_lines)
        self.wait(2)

    def add_branches(self, p1, p2):
        branches = []
        v = p2 - p1
        base_dir = v / np.linalg.norm(v)
        seg_len = np.linalg.norm(v)

        # 2/3 point, ±30°, length 2/9
        origin_2_3 = p1 + (2/3) * v
        length_2_9 = (2/9) * seg_len
        branches += self.sprout(origin_2_3, base_dir, length_2_9, angles_deg=[+30, -30])

        # 1/3 point, ±60°, length 1/3
        origin_1_3 = p1 + (1/3) * v
        length_1_3 = (1/3) * seg_len
        branches += self.sprout(origin_1_3, base_dir, length_1_3, angles_deg=[+50, -50])

        return branches

    def sprout(self, origin, base_dir, length, angles_deg):
        branches = []
        for angle_deg in angles_deg:
            angle_rad = np.radians(angle_deg)
            rot = np.array([
                [np.cos(angle_rad), -np.sin(angle_rad), 0],
                [np.sin(angle_rad),  np.cos(angle_rad), 0],
                [0, 0, 1]
            ])
            new_dir = rot @ base_dir
            new_end = origin + length * new_dir
            branches.append((origin, new_end))
        return branches
