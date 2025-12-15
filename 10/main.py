import os
from loguru import logger
import sys
from itertools import combinations, product
from copy import deepcopy
logger.remove()
logger.add(sys.stdout, level="DEBUG")

SWITCH_ON = "#"
SWITCH_OFF = "."

class Machine:
    
    def __init__(self, light_diagram: str, buttons: list[list[str]], joltage_reqs: list[int]):
        self.light_diagram = light_diagram
        self.goal_schema = [char == SWITCH_ON for char in light_diagram]
        self.buttons= buttons
        self.joltage_reqs = joltage_reqs
        self.task2_button_press = 0
        
    def __str__(self):
        return f"Machine: diagram: {self.light_diagram} | schema: {self.goal_schema} | buttons: {self.buttons} | reqs: {self.joltage_reqs}"
    
    def evaluate_button_presses(self, init_array: list[bool], combination: tuple):
        for button_press in combination:
            button = self.buttons[button_press]
            for switch in button:
                init_array[switch] = not init_array[switch]
        return init_array
            
    
    def button_press_to_turn_on(self):   #task1
        """
        Starting from all controls turned off, returns mininal number of button presses needed to 
        get to final schema
        """
        init_array = [False for item in range(len(self.goal_schema))]
        for i in range(1, len(self.buttons)):
            combs = combinations(range(len(self.buttons)), i)
            for comb in combs:
                logger.debug(comb)
                result = self.evaluate_button_presses(deepcopy(init_array), comb)
                # logger.info(f"Correct combination: {comb}")
                if result == self.goal_schema:
                    # logger.info(f"Returning: {i} | {comb}")
                    return i, comb
        # logger.info(f"Returning 0")
        return 0
    
    
    def get_lognest_buttons(self,):
        max_length = max([len(button) for button in self.buttons])
        max_buttons = []
        for button in self.buttons:
            if len(button) == max_length:
                max_buttons.append(button)
        return max_buttons    
    
    def pick_best_button(self, buttons, voltages):
        candidates = buttons
        while len(candidates) > 1:
            logger.debug(f"Cand length: {len(candidates)}")
            max_voltage_index = max(range(len(voltages)), key=voltages.__getitem__)
            current_candidates = []
            for cand in candidates:
                if max_voltage_index in cand:
                    current_candidates.append(cand)
            candidates = current_candidates
            voltages[max_voltage_index] = 0
        if len(candidates) == 1:
            return candidates[0]
        else:
            return cand
    
    def if_button_comb_returns_zeros(self, target_voltage: list[int], button_combination: list[list[int]] ) -> bool:
        for combination in button_combination:
            for switch in combination:
                target_voltage[switch] -= 1
                if target_voltage[switch] < 0:
                    return False
        if all([num == 0 for num in target_voltage]):
            return True
        return False
           
    def get_least_presses(self, target_voltage: list[int]) -> int:
        while min(target_voltage) >= 4:
            button = self.pick_best_button(self.buttons, deepcopy(target_voltage))
            self.task2_button_press += 1
            for switch in button:
                target_voltage[switch] -= 1
        logger.info(f"Voltages after pressing large buttons: {target_voltage}")
        min_button_presses = max(target_voltage)
        max_button_presses = sum(target_voltage)
        for i in range(min_button_presses, max_button_presses+1):
            options = product(self.buttons, repeat=i)
            for option in options:
                #calculate options 
                if self.if_button_comb_returns_zeros(deepcopy(target_voltage), option):
                    return i
        return 0
    
    def task2_button_press_joltage_reqs(self, combination: tuple):
        self.task2_button_press = 0
        voltages = deepcopy(self.joltage_reqs)
        # get max button presses of each_button:
        for comb in combination:
            self.task2_button_press += 1
            for switch in self.buttons[comb]:
                voltages[switch] -= 1
        logger.info(f"voltages: {voltages}")
        half_voltages = [int(volt / 2) for volt in voltages]
        logger.info(f"Processing half: {half_voltages}")
        min_presses = self.get_least_presses(target_voltage=half_voltages)
            
        self.task2_button_press += (2 * min_presses)

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
    with open(os.path.join(file_path, "input.txt"), "r") as f:
        task_input = f.readlines()
        task_input = [row.strip() for row in task_input]
    
    machines = process_input(task_input)
    presses = 0
    joltage_presses = 0
    
    for machine in machines: 
        logger.debug(machine)
        min_press, combination = machine.button_press_to_turn_on()
        logger.info(f"Machine: {machine} | presses: {min_press} | comb: {combination}")
        presses += min_press
        machine.goal_schema = [number % 2 == 1 for number in machine.joltage_reqs]
        min_press, combination = machine.button_press_to_turn_on()
        machine.task2_button_press_joltage_reqs(combination)
        logger.info(f"Button press: {machine.task2_button_press}")
        joltage_presses += machine.task2_button_press
    logger.info(f"Task1 result: {presses}")
    logger.info(f"Task 2 result: {joltage_presses}")


if __name__ == "__main__":
    main()