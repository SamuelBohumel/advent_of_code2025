import os
from loguru import logger
import sys
logger.remove()
logger.add(sys.stdout, level="INFO")



def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
    
    logger.info(task_input)


if __name__ == "__main__":
    main()