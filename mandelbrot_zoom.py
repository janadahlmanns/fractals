from manim import *
import numpy as np

config.pixel_width = 800
config.pixel_height = 800
config.frame_width = 6
config.frame_height = 6

class MandelbrotZoom(Scene):
    def construct(self):
        res_x = 800
        res_y = 800
        framerate = 8
        max_iter = 100

        center = (-0.5255, -0.525)
        n_frames = 160
        start_zoom = 3.0
        end_zoom = 0.0001
        zoom_factor = (end_zoom / start_zoom) ** (1 / (n_frames - 1))

        prev_img = None
        for i in range(n_frames):
            zoom = start_zoom * (zoom_factor ** i) # exponential zoom
            #zoom = start_zoom - i * ((start_zoom - end_zoom) / (n_frames - 1)) # linear zoom
            image = self.generate_mandelbrot_image(center, res_x, res_y, zoom, max_iter)
            img = ImageMobject(image).set(width=config.frame_width)
            self.add(img)
            self.wait(1 / framerate)
            if prev_img:
                self.remove(prev_img)
            prev_img = img


    def generate_mandelbrot_image(self, center, res_x, res_y, zoom, max_iter=100):
        x_center, y_center = center

        x_min = x_center - (zoom / 2)
        x_max = x_center + (zoom / 2)
        y_min = y_center - (zoom / 2)
        y_max = y_center + (zoom / 2)

        image = np.zeros((res_y, res_x, 3), dtype=np.uint8)

        palette = [
            np.array([14, 64, 88]),
            np.array([87, 127, 141]),
            np.array([14, 88, 77]),
            np.array([231, 158, 22]),
            np.array([255, 222, 5]),
            np.array([158, 43, 53]),
        ]

        for i in range(res_y):
            y = y_min + (i / (res_y - 1)) * (y_max - y_min)
            for j in range(res_x):
                x = x_min + (j / (res_x - 1)) * (x_max - x_min)
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
                    idx = int(t)
                    frac = t - idx
                    color = (
                        (1 - frac) * palette[idx] + frac * palette[min(idx + 1, len(palette) - 1)]
                    )

                image[i, j] = np.clip(color, 0, 255)

        return image
