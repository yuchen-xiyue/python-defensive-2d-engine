from math import pi as PI
from ..shapes import RegularPolygon
from ..ops import Vector
from ..ops.utils import rotation_matrix, scaling_matrix

class ScriptLoader:
    def __init__(self, filename):
        self.filename = filename
        self.width, self.height = 0, 0
        self.num_shapes   = 0  
        self.shapes       = []
        self.transforms   = []
        self.translations = []

    def read_script(self): 
        with open(self.filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
        data = [line.split() for line in lines]
        # Check input format
        if len(data[0]) != 2: 
            raise ValueError(f"The first line of script should specify the window size. ")
        for i in range(1, len(data)-1): 
            if len(data[i]) != 6: 
                raise ValueError(f"Invalid script in line {i+1}. ")
        # First line specifies the window size
        self.height, self.width = int(data[0][0]), int(data[0][1])
        for values in data[1: ]: 
            # data format: n-sides, scale-x, scale-y, rot-degree, position-x, position-y
            self.num_shapes += 1
            self.shapes.append(
                RegularPolygon(num_sides=int(values[0]), radius=1.)
                )
            self.transforms.append(
                rotation_matrix(float(values[3])*PI/180) * scaling_matrix(float(values[1]), float(values[2]))
                )
            self.translations.append(
                Vector([float(values[4]), float(values[5])])
            )
            
        return
    
    def __len__(self): 
        return len(self.shapes)
    
    def __getitem__(self, index): 
        return self.shapes[index].transform(self.transforms[index]).translate(self.translations[index])
