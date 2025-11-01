from manim import *
import numpy as np

config.pixel_width = 2160
config.pixel_height = 2160
config.frame_width = 6
config.frame_height = 6

class Mandelbrot(Scene):
    def construct(self):
        max_iter = 100
        width, height = 2160, 2160


        x_min, x_max = -2.0, 1.0
        y_min, y_max = -1.5, 1.5

        image = self.generate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter)

        mobject = ImageMobject(image)
        mobject.set(width=config.frame_width)  # fills the full 6x6 frame width perfectly
        self.add(mobject)

    def generate_mandelbrot(self, width, height, x_min, x_max, y_min, y_max, max_iter):
        image = np.zeros((height, width, 3), dtype=np.uint8)

        # Substack palette
        palette = [
            np.array([14, 64, 88]),     # dark blue
            np.array([87, 127, 141]),   # middle blue
            np.array([14, 88, 77]),     # dark green
            np.array([231, 158, 22]),   # orange
            np.array([255, 222, 5]),    # yellow
            np.array([158, 43, 53]),    # red
        ]

        for i in range(height):
            for j in range(width):
                x = x_min + (j / width) * (x_max - x_min)
                y = y_min + (i / height) * (y_max - y_min)
                c = complex(x, y)
                z = 0
                n = 0

                while abs(z) <= 2 and n < max_iter:
                    z = z * z + c
                    n += 1

                if n == max_iter:
                    color = np.array([0, 0, 0])
                else:
                    # Smooth iteration count for continuous gradients
                    smooth = n + 1 - np.log(np.log2(abs(z)))
                    t = smooth / max_iter
                    t *= len(palette) - 1

                    idx = int(t)
                    frac = t - idx
                    if idx + 1 < len(palette):
                        color = (1 - frac) * palette[idx] + frac * palette[idx + 1]
                    else:
                        color = palette[-1]

                image[i, j] = np.clip(color, 0, 255)

        return image
