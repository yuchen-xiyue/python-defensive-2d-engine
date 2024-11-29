from ..ops import Vector, Matrix
class Shape:
    def __init__(self) -> None:
        pass

    def affine_transform(self, transform_matrix: Matrix, translation_vector: Vector): 
        if not isinstance(translation_vector, Vector): 
            raise TypeError(f"Translation vector should be a Vector, not {type(translation_vector)}")

        if not isinstance(transform_matrix, Matrix): 
            raise TypeError(f"Transformation matrix should be a Matrix, not {type(transform_matrix)}")
        return 

    def draw(self, canvas):
        """
        Draw on buffer. 
        :param canvas: The buffer to draw. 
        """
        pass 