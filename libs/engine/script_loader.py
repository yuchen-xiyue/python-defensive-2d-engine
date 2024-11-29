from math import pi as PI
from ..shapes import RegularPolygon
from ..ops import Vector, Matrix

class ScriptLoader:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.width, self.height = 0, 0
        self.shapes       = []

    @staticmethod
    def input_format_check(line, idx): 
        if idx == 0: 
            if len(line) != 2: 
                raise ValueError(f"The first line of script should specify the window size. ")
            else: 
                return
        elif idx > 0: 
            if len(line) != 6: 
                raise ValueError(f"Invalid script in line {idx+1}. ")
            else:
                return


    def read_script(self) -> bool: 
        # Fatal problem: script not found
        try:
            with open(file=self.filename, mode='r') as file:
                str_lines = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"Error: The file '{self.filename}' does not exist.")
            return False
        except IOError as e:
            print(f"Error: Cannot read the file. Details: {e}")
            return False
        # convert raw string into data
        data_lines = [line.split() for line in str_lines]
        num_lines = len(data_lines)
        # First line specifies the window size
        try: 
            ScriptLoader.input_format_check(data_lines[0], 0)
        except Exception as e:
            print(f"Error in reading script: {e}")
        else:
            self.height, self.width = int(data_lines[0][0]), int(data_lines[0][1])
        for idx in range(1, num_lines):                         
            try: 
                ScriptLoader.input_format_check(data_lines[idx], idx)
            except Exception as e:
                print(f"Error in reading script: {e}")
                # Skip incorrect line
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
            
        return True
    
    def get_size(self) -> tuple[int, int]: 
        return self.height, self.width
    
    def get_shapes(self) -> list[RegularPolygon]: 
        return self.shapes
    
    def __len__(self) -> int: 
        return len(self.shapes)
    
    def __getitem__(self, index) -> RegularPolygon: 
        return self.shapes[index]
