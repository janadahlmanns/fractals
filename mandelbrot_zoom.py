from manim import *
import numpy as np


fps = 3
duration = 2
frames = fps * duration
max_iter = 100


# ---------- Config ----------
config.pixel_width = 800      # quick test
config.pixel_height = 800
config.frame_width = 6
config.frame_height = 6
config.frame_rate = fps


# initial full view 
center0 = (0,0)
width0 = 3.0

# zoom target (Mandelbrot coords)
target_center = (0.0, 1)
target_width = 0.1


# ---------- Scene ----------
class MandelbrotZoom(Scene):
    def construct(self):
        dot = Dot(color=RED, radius=0.1).move_to([target_center[0], target_center[1], 0])
        self.add(dot)

        img = self.render_mandelbrot(center0, width0)
        m = ImageMobject(img)
        self.add(m)


    def render_mandelbrot(center, width, height_px=2160, width_px=2160, max_iter=100):

        cx, cy = center
        half_w = width / 2
        half_h = width / 2

        x_min, x_max = cx - half_w, cx + half_w
        y_min, y_max = cy - half_h, cy + half_h

        image = np.zeros((height_px, width_px, 3), dtype=np.uint8)

        palette = [
            np.array([14, 64, 88]),
            np.array([87, 127, 141]),
            np.array([14, 88, 77]),
            np.array([231, 158, 22]),
            np.array([255, 222, 5]),
            np.array([158, 43, 53]),
        ]

        for i in range(height_px):
            for j in range(width_px):
                # map pixel to complex plane
                x = x_min + (j / width_px) * (x_max - x_min)
                y = y_min + (i / height_px) * (y_max - y_min)
                c = complex(x, y)
                z = 0
                n = 0
                while abs(z) <= 2 and n < max_iter:
                    z = z * z + c
                    n += 1

                if n == max_iter:
                    color = np.array([0, 0, 0])
                else:
                    smooth = n + 1 - np.log(np.log2(abs(z)))
                    t = smooth / max_iter * (len(palette) - 1)
                    idx, frac = int(t), t - int(t)
                    color = ((1 - frac) * palette[idx]
                            + frac * palette[min(idx + 1, len(palette) - 1)])
                image[i, j] = np.clip(color, 0, 255)

        return image