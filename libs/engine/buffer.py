from ..ops import Vector

class Buffer:
    def __init__(self, height: int, width: int) -> None:
        # Initialize the buffer
        self.data = [[0 for _ in range(width)] for _ in range(height)]
        self.height = height
        self.width = width
        
    @staticmethod
    def point_to_line_distance(p: Vector, a: Vector, b: Vector) -> float:
        """
        Calculate the minimum distance from pixel p to the line segment ab. 
        """
        # Calculate the length of the given line segment
        length = (b - a).norm()
        
        # Check if the two endpoints are identical
        if length == 0:
            return (a - p).norm()
        
        # Calculate the projection coefficient
        t = (a - p).dot_product(input_=a - b) / length ** 2
        # cramp t within 0 to 1
        t_prime = max(0, min(1, t))
        
        # Calculate the project point
        p_prime = a + t_prime * (b - a)
        
        # Calculate the distance from pixel to the line segment
        return (p - p_prime).norm()

    def draw_line(self, p_a: Vector, p_b: Vector, threshold:float=0.5) -> None:
        """
        Draw pixel on buffer
        """
        for i in range(self.height):
            for j in range(self.width):
                # if distance between pixel and line segment within the threshold, render it
                if Buffer.point_to_line_distance(p=Vector(elements=[self.height - i, j]), a=p_a, b=p_b) <= threshold:
                    self.data[i][j] = 1

    def display(self, mode="default") -> None:
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