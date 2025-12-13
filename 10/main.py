import os
from loguru import logger
import sys
from itertools import combinations
from copy import deepcopy
logger.remove()
logger.add(sys.stdout, level="INFO")

SWITCH_ON = "#"
SWITCH_OFF = "."

class Machine:
    
    def __init__(self, light_diagram: str, buttons: list[list[str]], joltage_reqs: list[int]):
        self.light_diagram = light_diagram
        self.goal_schema = [char == SWITCH_ON for char in light_diagram]
        self.buttons= buttons
        self.joltage_reqs = joltage_reqs
        
    def __str__(self):
        return f"Machine: diagram: {self.light_diagram} | schema: {self.goal_schema} | buttons: {self.buttons} | reqs: {self.joltage_reqs}"
    
    def evaluate_button_presses(self, init_array: list[bool], combination: tuple):
        for button_press in combination:
            button = self.buttons[button_press]
            for switch in button:
                init_array[switch] = not init_array[switch]
        return init_array
            
    
    def button_press_to_turn_on(self) -> int:
        """
        Starting from all controls turned off, returns mininal number of button presses needed to 
        get to final schema
        """
        min_presses = 0
        init_array = [False for item in range(len(self.goal_schema))]
        for i in range(1, len(self.buttons)):
            combs = combinations(range(len(self.buttons)), i)
            for comb in combs:
                logger.debug(comb)
                result = self.evaluate_button_presses(deepcopy(init_array), comb)
                logger.info(f"Correct combination: {comb}")
                if result == self.goal_schema:
                    return i
        
        return 0
        

def process_input(lines: str):
    machines = []
    for row in lines:
        splitted = row.split(' ')
        light_diagram = splitted[0].replace("[", "").replace("]", "")
        splitted = splitted[1:]
        joltage_reqst = splitted[-1]
        joltage_reqst = joltage_reqst.replace("{", "").replace("}", "")
        joltage_reqst = [int(req) for req in joltage_reqst.split(',')]
        splitted = splitted[:-1]
        buttons = []
        for item in splitted:
            stripped = item.replace("(", "").replace(")", "").replace(" ", "")
            buttons.append([int(item) for item in stripped.split(',')])
        machines.append(Machine(light_diagram=light_diagram,
                                buttons=buttons,
                                joltage_reqs=joltage_reqst))
    return machines


def main():
    task_input = None
    file_path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(file_path, "ex_input.txt"), "r") as f:
        task_input = f.readlines()
        task_input = [row.strip() for row in task_input]
    
    machines = process_input(task_input)
    presses = 0
    for machine in machines: 
        logger.debug(machine)
        min_press = machine.button_press_to_turn_on()
        logger.info(f"Machine: {machine} | presses: {min_press}")
        presses += min_press
    logger.info(f"Task1 result: {presses}")


if __name__ == "__main__":
    main()