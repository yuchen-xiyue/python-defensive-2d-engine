from . import Vector

class Matrix:
    def __init__(self, rows) -> None:
        # Copying matrix
        if isinstance(rows, Matrix):
            self.data = [[e for e in row] for row in rows.data]
            self.num_rows = rows.num_rows
            self.num_cols = rows.num_cols
            return
        # Check if input is a list
        if not isinstance(rows, list):
            raise TypeError("Matrix rows must be provided as a list of lists or vectors.")
        
        # Check each row
        row_length = len(rows[0])
        for row in rows:
            # Check if elements provided as a list and in correct length
            if not isinstance(row, (list, Vector)) or len(row) != row_length:
                raise ValueError("All rows in the matrix must have the same length and be lists.")
            # Check if the elements are all numbers
            if not all(isinstance(i, (int, float)) for i in row):
                raise ValueError("All elements in the matrix must be numbers.")
        
        # Initiate attributes
        self.data = []
        for row in rows: 
            self.data.append([e for e in row])
        self.num_rows = len(rows)
        self.num_cols = row_length

    @staticmethod
    def dimension_check(obj, input_, op_name: str) -> None:
        """Check the dimension for operations with non-numeric inputs"""
        # Element-wise operation dimensions check
        if   op_name in ["addition", "substraction", "element-wise production"]:
            if not isinstance(input_, Matrix): 
                raise TypeError(f"Operation {op_name} not supported between Matrix and {type(input_)}")
            if obj.dim[0] != input_.dim[0] or obj.dim[1] != input_.dim[1]: 
                raise ValueError(f"Dimension mismatch for {op_name}: {obj.dim[0]}x{obj.dim[1]} with {input_.dim}-vector. ")
        # Matrix * Vector
        elif op_name in ["matrix multiply vector"]:
            if obj.dim[1] != input_.dim: 
                raise ValueError(f"Dimension mismatch for {op_name}: {obj.dim[0]}x{obj.dim[1]} with {input_.dim}-vector. ")
        # Vector * Matrix
        elif op_name in ["vector multiply matrix"]:
            if obj.dim[0] != input_.dim: 
                raise ValueError(f"Dimension mismatch for {op_name}: {input_.dim}-vector with {obj.dim[0]}x{obj.dim[1]}. ")
        # Matrix * Matrix
        elif op_name in ["matrix multiply matrix"]: 
            if obj.dim[1] != input_.dim[0]: 
                raise ValueError(f"Dimension mismatch for {op_name}: {obj.dim[0]}x{obj.dim[1]} with {input_.dim[0]}x{input_.dim[1]}-matrix. ")
        else: 
            raise ValueError(f"Invalid operation name: {op_name}.")
        
    
    @staticmethod
    def identity_matrix(dim: int): 
        Matrix.dimension_check(obj=None, input_=(dim, dim), op_name="creating identity matrix")

        return Matrix(rows=[
            [ 1 if i == j else 0 for j in range(dim) ] for i in range(dim)
        ])
    
    @staticmethod
    def one_matrix(dim: tuple[int, int]): 
        Matrix.dimension_check(obj=None, input_=dim, op_name="creating one matrix")

        return Matrix(rows=[
            [1 for _ in range(dim[1])] for _ in range(dim[0])
        ])
    
    @staticmethod
    def zero_matrix(dim: tuple[int, int]): 
        Matrix.dimension_check(obj=None, input_=dim, op_name="creating zero matrix")

        return Matrix(rows=[
            [0 for _ in range(dim[1])] for _ in range(dim[0])
        ])
    
    @staticmethod
    def expend_vector(vector: Vector, axis: int, dim: int): 
        """Expand vector to matrix along given axis to make a matrix"""
        if not isinstance(dim, int) or dim <= 0: 
            raise ValueError(f"Invalid dimension input {dim}. ")

        if axis == 0: 
            result = Matrix(rows=[vector.data for _ in range(dim)])
        elif axis == 1 or axis == -1:
            result = Matrix(rows=[[vector.data[i]] * dim for i in range(dim)])
        else: 
            raise ValueError(f"Invalid axis number {axis} to expand. ")

        return result
    
    @staticmethod
    def rotation_matrix(theta: float): 
        from math import sin, cos
        result = [
            [cos(theta), -sin(theta)],
            [sin(theta),  cos(theta)]
            ]
        return Matrix(rows=result)
    
    @staticmethod
    def scaling_matrix(a: float, b: float): 
        result = [
            [a, 0.],
            [0., b]
            ]
        return Matrix(rows=result)

    @property
    def dim(self) -> tuple[int, int]: 
        return (self.num_rows, self.num_cols)
    
    def transpose(self): 
        transposed = [
            [ self.data[j][i] for j in range(self.num_rows) ] 
            for i in range(self.num_cols)
            ]
        return Matrix(rows=transposed)
    
    def row(self, index: int) -> Vector: 
        """Get the i-th row vector"""
        return Vector(elements=self.data[index])
    
    def col(self, index: int) -> Vector: 
        """Get the j-th column vector"""
        return Vector(elements=[row[index] for row in self.data])

    
    def __add__(self, input_): 
        """Add by another matrix or a number"""
        # Add a number
        if isinstance(input_, (int, float)): 
            result = [
                [self.data[i][j] + input_ for j in range(self.num_cols)] 
                    for i in range(self.num_rows)
                ]
            return Matrix(rows=result)
        # Add a matrix
        Matrix.dimension_check(obj=self, input_=input_, op_name="addition")
        result = [
            [self.data[i][j] + input_[i][j] for j in range(self.num_cols)] 
                for i in range(self.num_rows)
            ]
        return Matrix(rows=result)
    
    def __sub__(self, input_): 
        """Substract another matrix or a number"""
        # Substract a number
        if isinstance(input_, (int, float)): 
            result = [
                [self.data[i][j] - input_ for j in range(self.num_cols)] 
                    for i in range(self.num_rows)
                ]
            return Matrix(rows=result)
        # Substract a matrix
        Matrix.dimension_check(obj=self, input_=input_, op_name="substraction")
        result = [
            [self.data[i][j] - input_[i][j] for j in range(self.num_cols)] 
                for i in range(self.num_rows)
            ]
        return Matrix(rows=result)

    def __mul__(self, input_): 
        # Scale by number
        if isinstance(input_, (int, float)): 
            result = Matrix(rows=[
                [ input_ * self.data[i][j] for j in range(self.num_cols) ]
                for i in range(self.num_rows)
                ])
        # right multiply a vector
        elif isinstance(input_, Vector): 
            Matrix.dimension_check(obj=self, input_=input_, op_name="matrix multiply vector")
            result = Vector(elements=[
                self.row(index=i).dot_product(input_=input_) for i in range(self.num_rows)
            ])
        # right multiply a matrix
        elif isinstance(input_, Matrix): 
            Matrix.dimension_check(obj=self, input_=input_, op_name="matrix multiply matrix")
            result = Matrix(rows=[
                [ self.row(index=i).dot_product(input_=input_.col(index=j)) for j in range(input_.num_cols) ] 
                for i in range(self.num_rows)
            ])
        else: 
            raise TypeError("Input must be integer, vector or matrix.")

        return result
    
    def __rmul__(self, input_): 
        # Scale by number
        if isinstance(input_, (int, float)): 
            result = Matrix(rows=[
                [ input_ * self.data[i][j] for j in range(self.num_cols) ]
                for i in range(self.num_rows)
                ])
        # left multiply a vector
        elif isinstance(input_, Vector): 
            Matrix.dimension_check(obj=self, input_=input_, op_name="vector multiply matrix")
            result = Vector(elements=[
                self.col(index=i).dot_product(input_=input_) for i in range(self.num_cols)
            ])
        # left multiply a matrix
        elif isinstance(input_, Matrix): 
            Matrix.dimension_check(obj=input_, input_=self, op_name="matrix multiply matrix")
            result = Matrix(rows=[
                [ input_.row(index=i).dot_product(input_=self.col(index=j)) for j in range(self.num_cols) ] 
                for i in range(input_.num_rows)
            ])
        else: 
            raise TypeError("Input must be integer, vector or matrix.")

        return result
    
    __radd__ = __add__

    def elementwise_product(self, input_): 
        Matrix.dimension_check(obj=self, input_=input_, op_name="element-wise production")
        result = [
            [self.data[i][j] * input_[i][j] for j in range(self.num_cols)] 
                for i in range(self.num_rows)
            ]
        return Matrix(rows=result)


    def __repr__(self) -> str:
        return f"Matrix{self.data}"