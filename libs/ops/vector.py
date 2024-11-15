class Vector:
    def __init__(self, elements: any):
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

    def dimension_check(self, input_, op_name: str): 
        """Check the dimension for operations with non-numeric inputs"""
        # For vector input checking
        if op_name in ["addition", "substraction", "dot product", "element-wise product"]: 
            if not isinstance(input_, Vector) or self.dim != input_.dim:
                raise ValueError(f"Input must be vector of the same length {self.dim} for {op_name}, got {input_.dim}.")
        # For number input checking
        elif op_name in ["scaling"]: 
            if not isinstance(input_, (int, float)): 
                raise TypeError(f"Factor must be integer or float for {op_name}, got {input_}.")
        else: 
            raise ValueError(f"Invalid operation name: {op_name}.")

        return True
    
    def __add__(self, input_: any):
        """Add by another vector or number"""
        # Add a number
        if isinstance(input_, (int, float)): 
            result = [self[i] + input_ for i in range(self.dim)]
            return Vector(result)
        # Add a vector
        self.dimension_check(input_, "addition")
        result = [self[i] + input_[i] for i in range(self.dim)]
        return Vector(result)

    def __sub__(self, input_: any):
        """Substract another vector or number"""
        # minus a number
        if isinstance(input_, (int, float)): 
            result = [self[i] - input_ for i in range(self.dim)]
            return Vector(result)
        self.dimension_check(input_, "substraction")
        result = [self[i] - input_[i] for i in range(self.dim)]
        return Vector(result)
    
    def __mul__(self, input_: int | float): 
        """Scale vector by a factor"""
        self.dimension_check(input_, "scaling")
        result = [input_ * self[i] for i in range(self.dim)]
        return Vector(result)
    
    __rmul__ = __mul__
    __radd__ = __add__

    def dot_product(self, input_):
        """Dot product with another vector"""
        self.dimension_check(input_, "dot product")        
        result = sum(self[i] * input_[i] for i in range(self.dim))
        return result
    
    def elementwise_product(self, input_):
        """Element-wise product with another vector"""
        self.dimension_check(input_, "element-wise product")        
        result = sum(self[i] * input_[i] for i in range(self.dim))
        return result
    
    def norm(self):
        return sum(self[i] ** 2 for i in range(self.dim)) ** .5
    
    @property
    def dim(self):
        """Get vector dimension"""
        return len(self.data)

    def __len__(self): 
        """Get vector dimension"""
        return len(self.data)
    
    def __getitem__(self, index):
        """Get element by index"""
        return self.data[index]
    
    def __repr__(self):
        # To string
        return f"Vector{self.data}"