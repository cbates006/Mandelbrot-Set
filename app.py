from PIL import Image
from mandelbrot import MandelbrotSet
from viewport import Viewport
import matplotlib.cm
import numpy as np
from scipy.interpolate import interp1d
from PIL.ImageColor import getrgb
from dataclasses import dataclass

@dataclass
class Main:
    def paint(mandelbrot_set, viewport, palette, smooth):
        for pixel in viewport:
            stability = mandelbrot_set.stability(complex(pixel), smooth)
            index = int(min(stability * len(palette), len(palette) - 1))
            pixel.color = palette[index % len(palette)]

    def denormalize(palette):
        return [
            tuple(int(channel * 255) for channel in color)
            for color in palette
        ]

    def make_gradient(colors, interpolation="linear"):
        X = [i / (len(colors) - 1) for i in range(len(colors))]
        Y = [[color[i] for color in colors] for i in range(3)]
        channels = [interp1d(X, y, kind=interpolation) for y in Y]
        return lambda x: [np.clip(channel(x), 0, 1) for channel in channels]

    def hsb(hue_degrees: int, saturation: float, brightness: float):
        return getrgb(
            f"hsv({hue_degrees % 360},"
            f"{saturation * 100}%,"
            f"{brightness * 100}%)"
        )
    
    def displaySet():
        print("=====================================================")
        print("The Mandelbrot set is a fascinating mathematical object, " \
        "\nspecifically a set of points in the complex plane, known for"
        "\nits intricate fractal structure. It's defined by a simple" \
        "\niterative process involving complex numbers, where points" \
        "\nthat remain bounded under repeated calculations are considered  " \
        "\npart of the set, while those that diverge to infinity are not. " \
        "\nThis program will allow you to visualize this set by generating" \
        "\nan image of the Mandelbrot set according to your own" \
        "\nspecifications. Run the program and answer the questions below " \
        "\nto begin! ")
        print("=====================================================")
        
        def size():
            sizing = input("Would you prefer a small (512x512) or large (1920x1080) image? ")
            if sizing == "small":
                dimensions = (512,512)
            if sizing == "large":
                dimensions = (1930, 1080)
            return dimensions

        print("=====================================================")
        print("List of palettes: 'magma', 'inferno', 'plasma', 'viridis', 'cividis', 'twilight', 'twilight_shifted', 'turbo'")
        print("=====================================================")
        choosePalette = input("Which of the above color pallets would you like to use to generate your set? ")

        def smoothing():
            smoothQuest = input("Would you like to enable smoothing for a more gradient-like effect? Respond 'y' for yes or 'n' for no. ")
            if smoothQuest == "y":
                return True
            if smoothQuest == "n":
                return False
            
        def chooseType():
            type = input("Would you prefer an image of the full Mandelbrot Set, or a zoomed in image that shows the patterns spiral? Respond 'full' or 'spiral.' ")
            coords = [0,0,0]
            if type == "full":
                coords[0] = -0.75
                coords[1] = 3.5
                coords[2] = 20
            if type == "spiral":
                coords[0] = -0.7435 + 0.1314j
                coords[1] = 0.002
                coords[2] = 512
            return coords

        colormap = matplotlib.cm.get_cmap(choosePalette).colors
        palette = Main.denormalize(colormap)

        image = Image.new(mode="RGB", size=size())
        coords = chooseType()
        viewport = Viewport(image, center=coords[0], width=coords[1])

        mandelbrot_set = MandelbrotSet(max_iterations=coords[2], escape_radius=1000)
        Main.paint(mandelbrot_set, viewport, palette, smooth=smoothing())
        image.show()

Main.displaySet()