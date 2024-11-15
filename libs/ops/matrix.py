from . import Vector

class Matrix:
    def __init__(self, rows: any):
        # Copying matrix
        if isinstance(rows, Vector):
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

    @property
    def dim(self): 
        return (self.num_rows, self.num_cols)
    
    def transpose(self): 
        transposed = [
            [ self.rows[j][i] for j in range(self.num_rows) ] 
            for i in range(self.num_cols)
            ]
        return Matrix(transposed)
    
    def row(self, index: int): 
        """Get the i-th row vector"""
        return Vector(self.data[index])
    
    def col(self, index: int): 
        """Get the j-th column vector"""
        return Vector([row[index] for row in self.data])

    def dimension_check(self, input_: any, op_name: str):
        """Check the dimension for operations with non-numeric inputs"""
        # Element-wise operation dimensions check
        if   op_name in ["addition", "substraction", "element-wise production"]:
            if not isinstance(input_, Matrix): 
                raise TypeError(f"Operation {op_name} not supported between Matrix and {type(input_)}")
            if self.dim[0] != input_.dim[0] or self.dim[1] != input_.dim[1]: 
                raise ValueError(f"Dimension mismatch for {op_name}: {self.dim[0]}x{self.dim[1]} with {input_.dim}-vector. ")
        # Matrix * Vector
        elif op_name in ["matrix multiply vector"]:
            if self.dim[1] != input_.dim: 
                raise ValueError(f"Dimension mismatch for {op_name}: {self.dim[0]}x{self.dim[1]} with {input_.dim}-vector. ")
        # Vector * Matrix
        elif op_name in ["vector multiply matrix"]:
            if self.dim[0] != input_.dim: 
                raise ValueError(f"Dimension mismatch for {op_name}: {input_.dim}-vector with {self.dim[0]}x{self.dim[1]}. ")
        # Matrix * Matrix
        elif op_name in ["matrix multiply matrix"]: 
            if self.dim[1] != input_.dim[0]: 
                raise ValueError(f"Dimension mismatch for {op_name}: {self.dim[0]}x{self.dim[1]} with {input_.dim[0]}x{input_.dim[1]}-matrix. ")
        else: 
            raise ValueError(f"Invalid operation name: {op_name}.")
        
        return True
    
    def __add__(self, input_: any): 
        """Add by another matrix or a number"""
        # Add a number
        if isinstance(input_, (int, float)): 
            result = [
                [self[i][j] + input_ for j in range(self.num_cols)] 
                    for i in range(self.num_rows)
                ]
            return Matrix(result)
        # Add a matrix
        self.dimension_check(input_, "addition")
        result = [
            [self[i][j] + input_[i][j] for j in range(self.num_cols)] 
                for i in range(self.num_rows)
            ]
        return Matrix(result)
    
    def __sub__(self, input_: any): 
        """Substract another matrix or a number"""
        # Substract a number
        if isinstance(input_, (int, float)): 
            result = [
                [self[i][j] - input_ for j in range(self.num_cols)] 
                    for i in range(self.num_rows)
                ]
            return Matrix(result)
        # Substract a matrix
        self.dimension_check(input_, "substraction")
        result = [
            [self[i][j] - input_[i][j] for j in range(self.num_cols)] 
                for i in range(self.num_rows)
            ]
        return Matrix(result)

    def __mul__(self, input_: any): 
        # Scale by number
        if isinstance(input_, (int, float)): 
            result = Matrix([
                [ input_ * self.data[i][j] for j in range(self.num_cols) ]
                for i in range(self.num_rows)
                ])
        # right multiply a vector
        elif isinstance(input_, Vector): 
            self.dimension_check(input_, "matrix multiply vector")
            result = Vector([
                self.row(i).dot_product(input_) for i in range(self.num_rows)
            ])
        # right multiply a matrix
        elif isinstance(input_, Matrix): 
            self.dimension_check(input_, "matrix multiply matrix")
            result = Matrix([
                [ self.row(i).dot_product(input_.col(j)) for j in range(input_.num_cols) ] 
                for i in range(self.num_rows)
            ])
        else: 
            raise TypeError("Input must be integer, vector or matrix.")

        return result
    
    def __rmul__(self, input_: any): 
        # Scale by number
        if isinstance(input_, (int, float)): 
            result = Matrix([
                [ input_ * self.data[i][j] for j in range(self.num_cols) ]
                for i in range(self.num_rows)
                ])
        # left multiply a vector
        elif isinstance(input_, Vector): 
            self.dimension_check(input_, "vector multiply matrix")
            result = Vector([
                self.col(i).dot_product(input_) for i in range(self.num_cols)
            ])
        # left multiply a matrix
        elif isinstance(input_, Matrix): 
            input_.dimension_check(self, "matrix multiply matrix")
            result = Matrix([
                [ input_.row(i).dot_product(self.col(j)) for j in range(self.num_cols) ] 
                for i in range(input_.num_rows)
            ])
        else: 
            raise TypeError("Input must be integer, vector or matrix.")

        return result
    
    __radd__ = __add__

    def elementwise_product(self, input_: any): 
        self.dimension_check(input_, "element-wise production")
        result = [
            [self[i][j] * input_[i][j] for j in range(self.num_cols)] 
                for i in range(self.num_rows)
            ]
        return Matrix(result)


    def __repr__(self):
        return f"Matrix{self.data}"