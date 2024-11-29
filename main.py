import os
import argparse
from libs import engine

SCRIPT_DIRECTORY = "scripts"

def main() -> None: 
    # Parse user input
    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=str, help="Type in your script filename. ")
    args = parser.parse_args()
    # Load script from file
    script_path = os.path.join(SCRIPT_DIRECTORY, args.script)
    script_loader = engine.ScriptLoader(filename=script_path)
    script_loader.read_script()
    height, width = script_loader.get_size()
    shapes = script_loader.get_shapes()
    buffer = engine.Buffer(height=height, width=width)
    # Draw frame to buffer
    for shape in shapes: 
        shape.draw(canvas=buffer)
    # Display 
    buffer.display(mode='square')


if __name__ == '__main__': 
    main()