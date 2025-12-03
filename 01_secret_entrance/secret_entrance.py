from loguru import logger

import math

def solve_part_two_fixed(moves):
    N = 100  # Number of positions (0 to 99)
    current_position = 50
    zero_counter = 0

    for move_line in moves:
        move_line = move_line.strip()
        direction = move_line[0]
        distance = int(move_line[1:])
        
        P_start = current_position
        passes = 0
        
        if direction == 'R':
            # Clicks needed to hit 0 for the first time: N - P_start
            clicks_to_first_zero = N - P_start
            
            if distance >= clicks_to_first_zero and clicks_to_first_zero != N:
                # The first pass is completed, and subsequent passes are every N clicks
                passes = 1 + math.floor((distance - clicks_to_first_zero) / N)
            
            # The only case where clicks_to_first_zero = N is when P_start = 0.
            # If P_start = 0, the dial moves from 0 and clicks 0 at 100, 200, ...
            if P_start == 0:
                 passes = math.floor(distance / N)
            
            current_position = (P_start + distance) % N

        elif direction == 'L':
            # Clicks needed to hit 0 for the first time: P_start
            clicks_to_first_zero = P_start
            
            if distance >= clicks_to_first_zero and clicks_to_first_zero != 0:
                # The first pass is completed, and subsequent passes are every N clicks
                passes = 1 + math.floor((distance - clicks_to_first_zero) / N)

            # The only case where clicks_to_first_zero = 0 is when P_start = 0.
            # If P_start = 0, the dial moves from 0 and clicks 0 at 100, 200, ...
            if P_start == 0:
                passes = math.floor(distance / N)

            # Python's % handles negative numbers weirdly, so we force positive
            current_position = (P_start - distance) % N
            if current_position < 0:
                current_position += N
                
        zero_counter += passes

    return zero_counter

def main():
    input_f = "secret_entrance/input.txt"
    with open(input_f, "r") as f:
        moves = f.readlines()
    reset = 100
    position = 50
    zero_counter = 0
    zero_counter = solve_part_two_fixed(moves)
    
    # for move in moves:
    #     number = int(move.strip()[1:])
    #     # logger.info(move.strip())
    #     if move[0] == 'L':
    #         position = (position - number)
    #     elif move[0] == 'R':
    #         position = (position + number)
    #     if position % 100 == 0 and position != 0:
    #         zero_counter -= 1
    #     #count 
    #     if position < -reset or position > reset:
    #         logger.info(f"zero_counter: {zero_counter} | position: {position} | result: {(abs(position) // reset)}")
    #     zero_counter = zero_counter + (abs(position) // reset)
        

    #     position = position % reset
    #     if position == 0:
    #         zero_counter += 1
    
    logger.info(f"counter: {zero_counter}")


if __name__ == "__main__":
    main()