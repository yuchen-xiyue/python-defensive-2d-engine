from . import Shape
from ..ops import Vector, Matrix

class Polygon(Shape):
    def __init__(self, vertices: list[list], is_closed:bool=True): 
        super().__init__()

        self.vertices = []
        # Check input point dimension
        for vertex in vertices: 
            if Vector(vertex).dim != 2: 
                raise ValueError(f"Input vertex dimension should be 2, got {vertex.dim}")
            self.vertices.append(Vector(vertex))
        self.is_closed = is_closed

    def translate(self, input_: Vector): 
        super().translate(input_)
        for i in range(len(self.vertices)): 
            self.vertices[i] = self.vertices[i] + input_

        return self
    
    def transform(self, input_: Matrix): 
        super().transform(input_)
        for i in range(len(self.vertices)): 
            self.vertices[i] = input_ * self.vertices[i]

        return self
    
    def draw(self, canvas):
        super().draw(canvas)
        for i in range(len(self.vertices) - 1): 
            canvas.draw_line(self.vertices[i], self.vertices[i + 1])
        if self.is_closed: 
            canvas.draw_line(self.vertices[-1], self.vertices[0])
        
        return self