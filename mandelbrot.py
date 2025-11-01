from manim import *
import numpy as np

class MandelbrotStatic(Scene):
    def construct(self):
        max_iter = 50
        width, height = 800, 800

        x_min, x_max = -2.0, 1.0
        y_min, y_max = -1.5, 1.5

        image = self.generate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter)

        mobject = ImageMobject(image)
        mobject.set_height(config.frame_height)
        self.add(mobject)

    def generate_mandelbrot(self, width, height, x_min, x_max, y_min, y_max, max_iter):
        image = np.zeros((height, width, 3), dtype=np.uint8)

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

                brightness = int(255 * n / max_iter)
                image[i, j] = [brightness] * 3  # grayscale

        return image
