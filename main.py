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
    script_loader.read_script()

    buffer = engine.Buffer(script_loader.height, script_loader.width)

    for shape in script_loader: 
        shape.draw(buffer)

    buffer.display('square')


if __name__ == '__main__': 
    main()