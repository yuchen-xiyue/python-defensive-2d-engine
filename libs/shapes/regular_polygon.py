import math
from . import Polygon
from .. ops import Vector

class RegularPolygon(Polygon):
    def __init__(self, num_sides, radius):
        if num_sides < 3:
            raise ValueError("A polygon must have at least 3 sides.")
        if radius <= 0:
            raise ValueError("Radius must be positive.")

        # Calculate the vertices of reg polygon
        vertices = [
            Vector([radius * math.cos(2 * math.pi * i / num_sides), 
             radius * math.sin(2 * math.pi * i / num_sides)])
            for i in range(num_sides)
        ]
        
        super().__init__(vertices=vertices, is_closed=True)