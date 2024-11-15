from math import sin, cos
from . import Vector
from . import Matrix

def dim_check(dim: int|tuple[int, int], obj: str) -> bool:
    if obj == 'vector': 
        if not isinstance(dim, int) or dim <= 0:
            raise ValueError(f"The dimension of {obj} must be integer and larger than 0.")
    elif obj == 'matrix':
        if not isinstance(dim, tuple) or len(dim) != 2 or dim[0] < 0 or dim[1] < 0: 
            raise ValueError(f"The dimension of {obj} must be integer and larger than 0.")
    else: 
        raise ValueError(f"Invalid object type {obj}. ")
    
    return True
# Initialzing special vectors
def zero_vector(dim: int): 
    # Check input datatype
    dim_check(dim, "vector")
    
    return Vector([0.] * dim)

def one_vector(dim: int): 
    # check input datatype
    dim_check(dim, "vector")

    return Vector([1.] * dim)

def one_hot_vector(dim: int, index: int): 
    # check input datatype
    dim_check(dim, "vector")

    result = [ 1 if i == index else 0 for i in range(dim) ]
    return result

def identity_matrix(dim: int): 
    dim_check((dim, dim), "matrix")

    return Matrix([
        one_hot_vector(i) for i in range(dim)
    ])

def one_matrix(dim: tuple[int, int]): 
    dim_check(dim, "matrix")

    return Matrix([
        one_vector(dim[1]) for _ in range(dim[0])
    ])

def zero_matrix(dim: tuple[int, int]): 
    dim_check(dim, "matrix")

    return Matrix([
        zero_vector(dim[1]) for _ in range(dim[0])
    ])

def expend_vector(vector: Vector, axis: int, dim: int) -> Matrix: 
    """Expand vector to matrix along given axis"""
    if not isinstance(dim, int) or dim <= 0: 
        raise ValueError(f"Invalid dimension input {dim}. ")
    
    if axis == 0: 
        result = Matrix([vector.data for _ in range(dim)])
    elif axis == 1 or axis == -1:
        result = Matrix([vector.data[i]] * dim for i in range(dim))
    else: 
        raise ValueError(f"Invalid axis number {axis} to expand. ")

    return result

def point_to_line_distance(p: Vector, a: Vector, b: Vector):
        """
        Calculate the minimum distance from pixel p to the line segment ab. 
        """
        # Calculate the length of the given line segment
        length = (b - a).norm()
        
        # Check if the two endpoints are identical
        if length == 0:
            return (a - p).norm()
        
        # Calculate the projection coefficient
        t = (a - p).dot_product(a - b) / length ** 2
        # cramp t within 0 to 1
        t_prime = max(0, min(1, t))
        
        # Calculate the project point
        p_prime = a + t_prime * (b - a)
        
        # Calculate the distance from pixel to the line segment
        return (p - p_prime).norm()

def rotation_matrix(theta: float) -> Matrix: 
    result = [
        [cos(theta), -sin(theta)],
        [sin(theta),  cos(theta)]
        ]
    return Matrix(result)

def translation_vector(dx: float, dy: float) -> Vector: 
    result = [dx, dy]
    return Vector(result)

def scaling_matrix(a: float, b: float) -> Matrix: 
    result = [
        [a, 0.],
        [0., b]
        ]
    return Matrix(result)