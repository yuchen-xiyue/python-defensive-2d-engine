import os
import argparse
from libs import engine

SCRIPT_DIRECTORY = "scripts"

def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=str, help="Type in your script filename. ")
    args = parser.parse_args()

    script_path = os.path.join(SCRIPT_DIRECTORY, args.script)
    script_loader = engine.ScriptLoader(script_path)
    height, width = script_loader.read_script()
    shapes = script_loader.get_shapes()

    buffer = engine.Buffer(height, width)

    for shape in shapes: 
        shape.draw(buffer)

    buffer.display('square')


if __name__ == '__main__': 
    main()