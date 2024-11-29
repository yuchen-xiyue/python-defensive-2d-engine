class Vector:
    def __init__(self, elements) -> None:
        # Copying vector
        if isinstance(elements, Vector):
            self.data = [e for e in elements.data]
            return
        # Check if input is a list
        if not isinstance(elements, list):
            raise TypeError("Vector elements must be provided as a list.")
        
        # Check if the elements are all numbers
        if not all(isinstance(i, (int, float)) for i in elements):
            raise ValueError("All elements in the vector must be numbers.")
        
        self.data = elements

    @staticmethod
    def zero_vector(dim: int): 
        # Check input datatype
        Vector.dimension_check(obj=None, input_=dim, op_name="creating zero vector")
        
        return Vector(elements=[0.] * dim)
    
    
    @staticmethod
    def ones_vector(dim: int): 
        # Check input datatype
        Vector.dimension_check(obj=None, input_=dim, op_name="creating one vector")
        
        return Vector(elements=[1.] * dim)
    
    @staticmethod
    def translation_vector(dx: float, dy: float): 
        result = [dx, dy]
        return Vector(elements=result)
    
    @staticmethod
    def one_hot_vector(dim: int, index: int): 
    # check input datatype
        Vector.dimension_check(obj=None, input_=dim, op_name="creating one-hot vector")

        result = [ 1 if i == index else 0 for i in range(dim) ]
        return Vector(elements=result)

    @staticmethod
    def dimension_check(obj, input_, op_name: str) -> None: 
        """Check the dimension for operations with non-numeric inputs"""

        # For vector input checking
        if op_name in ["addition", "substraction", "dot product", "element-wise product"]: 
            if not isinstance(input_, Vector) or obj.dim != input_.dim:
                raise ValueError(f"Input must be vector of the same length {obj.dim} for {op_name}, got {input_.dim}.")
        
        # For number input checking
        elif op_name in ["scaling"]: 
            if not isinstance(input_, (int, float)): 
                raise TypeError(f"Factor must be integer or float for {op_name}, got {input_}.")
        
        # For special vectors intializing
        elif op_name in ["creating zero vector", "creating one vector", "creating one-hot vector"]: 
            if not isinstance(input_, int) or input_ <= 0:
                raise ValueError(f"The dimension input of {op_name} must be integer and larger than 0.")
        
        # Unspecified operation name
        else: 
            raise ValueError(f"Invalid operation name: {op_name}.")

    
    def __add__(self, input_):
        """Add by another vector or number"""
        # Add a number
        if isinstance(input_, (int, float)): 
            result = [self[i] + input_ for i in range(self.dim)]
            return Vector(elements=result)
        # Add a vector
        Vector.dimension_check(obj=self, input_=input_, op_name="addition")
        result = [self[i] + input_[i] for i in range(self.dim)]
        return Vector(elements=result)

    def __sub__(self, input_):
        """Substract another vector or number"""
        # minus a number
        if isinstance(input_, (int, float)): 
            result = [self[i] - input_ for i in range(self.dim)]
            return Vector(elements=result)
        Vector.dimension_check(obj=self, input_=input_, op_name="substraction")
        result = [self[i] - input_[i] for i in range(self.dim)]
        return Vector(elements=result)
    
    def __mul__(self, input_: int | float): 
        """Scale vector by a factor"""
        Vector.dimension_check(obj=self, input_=input_, op_name="scaling")
        result = [input_ * self[i] for i in range(self.dim)]
        return Vector(elements=result)
    
    __rmul__ = __mul__
    __radd__ = __add__

    def dot_product(self, input_) -> int:
        """Dot product with another vector"""
        Vector.dimension_check(obj=self, input_=input_, op_name="dot product")        
        result = sum(self[i] * input_[i] for i in range(self.dim))
        return result
    
    def elementwise_product(self, input_) -> int:
        """Element-wise product with another vector"""
        Vector.dimension_check(obj=self, input_=input_, op_name="element-wise product")        
        result = sum(self[i] * input_[i] for i in range(self.dim))
        return result
    
    def norm(self) -> float | int:
        return sum(self[i] ** 2 for i in range(self.dim)) ** .5
    
    @property
    def dim(self) -> int:
        """Get vector dimension"""
        return len(self.data)

    def __len__(self) -> int: 
        """Get vector dimension"""
        return len(self.data)
    
    def __getitem__(self, index) -> int | float:
        """Get element by index"""
        return self.data[index]
    
    def __repr__(self) -> str:
        # To string
        return f"Vector{self.data}"
    