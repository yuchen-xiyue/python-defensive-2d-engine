import traceback

from math import pi as PI
from ..shapes import RegularPolygon
from ..ops import Vector, Matrix

class ScriptLoader:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.width, self.height = 10, 10 # default values
        self.shapes       = []

    @staticmethod
    def input_format_check(line: list, idx: int): 
        # parameters: idx-th line of input data

        # the first line should specify the size of screen buffer
        if idx == 0: 
            if len(line) != 2: 
                raise ValueError(f"The first line of script should specify the window size. ")
        
            if not isinstance(line[0], int) or not isinstance(line[1], int): 
                raise TypeError(f"Window size parameters should be integer and integer, got {type(line[0])} and {type(line[1])}. ")

            if line[0] <= 0 or line[1] <= 0: 
                raise ValueError(f"Window size parameters should be integers greater than zero, got {line[0]} and {line[1]}. ")
        
        # other lines should give 6 parameters for each shape
        elif idx > 0: 
            if len(line) != 6: 
                raise ValueError(f"Invalid script in line {idx+1}: incorrect number of parameters. ")
            if any(not isinstance(x, (int, float)) for x in line): 
                raise ValueError(f"Invalid script in line {idx+1}: invalid input. ")
            
    def read_script(self): 
        # read script and return any errors caused by inputs
        exceptions, traceback_details = [], []
        
        # catching file not found error and io error
        try:
            with open(file=self.filename, mode='r') as file:
                str_lines = [line.strip() for line in file if line.strip()]
        except FileNotFoundError as e:
            exceptions.append(f"Error: The file '{self.filename}' does not exist.")
            traceback_details.append(traceback.format_exc())
            return exceptions, traceback_details
        except IOError as e:
            exceptions.append(f"Error: Cannot read the file. Details: {e}")
            traceback_details.append(traceback.format_exc())
            return exceptions, traceback_details
        
        # convert raw string data into numeric data
        data_lines = [[eval(x) for x in line.split()] for line in str_lines]
        num_lines = len(data_lines)

        # check if the inputs are in correct form
        # First line specifies the window size
        try: 
            ScriptLoader.input_format_check(data_lines[0], 0)
        # handle the blank input error
        except IndexError: 
            exceptions.append(f"Error in reading script: blank file as input. ")
            traceback_details.append(traceback.format_exc())
            return exceptions, traceback_details
        # handle input format error
        except (ValueError, TypeError) as e:
            exceptions.append(f"Error in reading script: {e}")
            traceback_details.append(traceback.format_exc())
            return exceptions, traceback_details
        else:
            # if everything is correct, assign shape values
            self.height, self.width = int(data_lines[0][0]), int(data_lines[0][1])
        
        # initiate each shape
        for idx in range(1, num_lines):                         
            try: 
                ScriptLoader.input_format_check(data_lines[idx], idx)
            except Exception as e:
                exceptions.append(f"Error in reading script: {e}")
                traceback_details.append(traceback.format_exc())
                # Skip incorrect line and continue to load data
                continue

            # data format: n-sides, scale-x, scale-y, rot-degree, position-x, position-y
            num_sides, sx, sy, rot, px, py = data_lines[idx]
            # initialize a uniform shape
            shape = RegularPolygon(num_sides=int(num_sides), radius=1.)
            # apply affine transformation
            shape.affine_transform(
                    transform_matrix=Matrix.scaling_matrix(a=float(sx), b=float(sy)) * Matrix.rotation_matrix(float(rot)*PI/180), 
                    translation_vector=Vector(elements=[float(px), float(py)])
                )
            # append to list
            self.shapes.append(shape)
            
        return exceptions, traceback_details
    
    def get_size(self) -> tuple[int, int]: 
        return self.height, self.width
    
    def get_shapes(self) -> list[RegularPolygon]: 
        return self.shapes
    
    def __len__(self) -> int: 
        return len(self.shapes)
    
    def __getitem__(self, index) -> RegularPolygon: 
        return self.shapes[index]
