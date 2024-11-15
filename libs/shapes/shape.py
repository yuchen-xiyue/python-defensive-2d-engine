from ..ops import Vector, Matrix
class Shape:
    def __init__(self) -> None:
        pass

    def translate(self, input_: Vector):
        """
        Transpose shape by a given vector. 
        :param vector: A vector for translation. 
        """
        if not isinstance(input_, Vector): 
            raise TypeError(f"Translation vector should be a Vector, not {type(input_)}")
        return self

    def transform(self, input_: Matrix):
        """
        Transform shape with a 2x2 transformation matrix. 
        :param matrix: A 2x2 transformation matrix. 
        """
        if not isinstance(input_, Matrix): 
            raise TypeError(f"Transformation matrix should be a Matrix, not {type(input_)}")
        return self

    def draw(self, canvas):
        """
        Draw on buffer. 
        :param canvas: The buffer to draw. 
        """
        pass 