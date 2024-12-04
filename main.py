import os
import traceback
import argparse
from datetime import datetime
from libs import engine

SCRIPT_DIRECTORY = "scripts"

def create_exception_logger(log_to_file=False): 
    # create closure logging func
    logger = None
    if not log_to_file: 
        # log to console
        def logger_console(exception: str, traceback_details: str): 
            print("Exception: " + exception)
            print(traceback_details)
        return logger_console
    elif log_to_file: 
        # log to file
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".log"
        def logger_file(exception: str, traceback_details: str): 
            try: 
                with open(filename, 'a') as file_handler: 
                    file_handler.write("\nException: " + exception + "\n")
                    file_handler.write(traceback_details)
            except Exception as e: 
                print(f"An error occur when logging to file")
        return logger_file

def main() -> None: 
    # Parse user input
    parser = argparse.ArgumentParser()
    parser.add_argument("script", type=str, help="Type in your script filename. ")
    parser.add_argument("-l", "--filelogger", action='store_true', help="Create logger file. ")
    
    try: 

        args = parser.parse_args()
    
    except argparse.ArgumentError as e: 

        print(e)
        print(traceback.format_exc())

    # initiate logger
    logger = create_exception_logger(args.filelogger)

    # Load script from file
    script_path = os.path.join(SCRIPT_DIRECTORY, args.script)
    script_loader = engine.ScriptLoader(filename=script_path)

    # possible multiple exception
    exceptions, traceback_details = script_loader.read_script()
    for exception, traceback_detail in list(zip(exceptions, traceback_details)):
        logger(exception, traceback_detail)

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