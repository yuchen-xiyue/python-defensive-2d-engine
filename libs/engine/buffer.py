from ..ops.utils import point_to_line_distance
from ..ops import Vector

class Buffer:
    def __init__(self, height: int, width: int):
        # Initialize the buffer
        self.data = [[0 for _ in range(width)] for _ in range(height)]
        self.height = height
        self.width = width

    def draw_line(self, p_a: Vector, p_b: Vector, threshold:float=0.5):
        """
        Draw pixel on buffer
        """
        for i in range(self.height):
            for j in range(self.width):
                # if distance between pixel and line segment within the threshold, render it
                if point_to_line_distance(Vector([self.height - i, j]), p_a, p_b) <= threshold:
                    self.data[i][j] = 1

    def display(self, mode="default"):
        """
        Display current buffered data
        """
        if mode == "default": 
            for row in self.data:
                print(' '.join(str(pixel) for pixel in row))
            return
        elif mode == "square": 
            for row in self.data:
                print(' '.join('■' if pixel else '□' for pixel in row))
            return