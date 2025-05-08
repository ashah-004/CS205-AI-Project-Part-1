import heapq
import time

GOAL_STATE = (1,2,3,4,5,6,7,8,0) # this is the goal state of the 8-puzzle problem that we want to achieve

GRID_SIZE = 3 # this is the rows/column size for the 8-puzzle problem

TOTAL_TILES = GRID_SIZE * GRID_SIZE # this the total matrix or puzzle size i.e. 3x3 = 9
# we can change the above goal-state, grid-size and total-tiles in order if we want to change the solution in future to solve 15 or 24 puzzle problem.

def print_puzzle_board(state): # this function is specifically for printing the state of the board at any point of time
    print("[")

    for i in range(GRID_SIZE): # here we are looping over the no. of rows which will always be grid-size so we are looping it in generic way as possible which is 3 in case of 8-puzzle.
      row_start = i * GRID_SIZE # here as we will be calculating the starting index of the row that we want to print
      row_end = row_start + GRID_SIZE # here we will be calculating the ending index of the row until which we want to print
      row = list(state[row_start:row_end]) # slicing the state for the row we want and storing it

      print(f"{row}") # printing each row of the state

    print("]")


# this is how a node i.e. a state in the search space for 8-puzzle problem will look like
class Node:
  def __init__(self, state, parent=None, action=None, cost=0):
    self.state = state # the current state of the 8-puzzle that we got after expansion

    self.parent = parent # the parent node that generated this node

    self.action = action # the action that we took that led us to this state of puzzle

    self.cost = cost # the cost it takes to reach to this state from the intial state

    self.heuristic = 0 # the estimated minimum cost it will take from this code to reach to the goal state

    self.a_star_f_cost = 0 # the total cost estimated by a-star algprithm i.e. f(x) = g(x) + h(x)

  def __lt__(self, other): # used to choose which node to give priority to.
    if self.a_star_f_cost == other.a_star_f_cost: # here we are checking the total cost of both the nodes.
      return self.cost < other.cost # if total cost of both nodes are same, we will se the cost of the node as heuristic is still after all just an assumption so we give cost larger preference.
    return self.a_star_f_cost < other.a_star_f_cost # if not then we will decide the node on the basis of total cost itself.

# This is a function to find the current position of the empty space
def find_empty_space(state):
  return state.index(0) # returning the index of 0 as it is out empty space

# This is a function to calculate the row and col of a particular index in the state
def find_index_coordinates(index):
  row = index // GRID_SIZE # this will divide the index with no. of rows and give us only integer value which will ultimately tell us in which row it is
  col = index % GRID_SIZE # this will divide the index with same grid-size and give remainder which will give us the column in which that index might be in.
  return (row, col)

# This fucntion is to get the index from the row and col of particular index in the state
def find_coordinates_index(row, col):
  if (row >= 0 and row < GRID_SIZE) and (col >= 0 and col < GRID_SIZE): # checking of both row and col are in bounds and if they are then we calculate and return index
    return row * GRID_SIZE + col
  return None # else we just return None.

# Now we are defining a function that will expand current state to the possible next states
def expand_state(state):
  empty_space_index = find_empty_space(state) # first we find exactly where the empty space is.
  empty_space_row, empty_space_col = find_index_coordinates(empty_space_index) # now we find which exact row and col it is in.

# here we have defined the possible valid moves and how the row/col change when we perform that move
  valid_moves = {
      'up' : (-1,0),
      'down' : (1,0),
      'left' : (0,-1),
      'right' : (0,1)
  }

  next_possible_states = []

  # for the next states
  for move, (row_change, col_change) in valid_moves.items():
    new_row = empty_space_row + row_change
    new_col = empty_space_col + col_change

    new_state_index = find_coordinates_index(new_row, new_col)

    if new_state_index is not None: # if the move is valid, we create a new state by swapping the blank space in that direction 
      new_state = list(state) # converting into list 
      number_to_change = new_state[new_state_index]
      new_state[empty_space_index] = number_to_change
      new_state[new_state_index] = 0

      new_state_tuple = tuple(new_state) # converting back to tuple

      next_possible_states.append((new_state_tuple, move, 1)) # creating list of all possible states and then returning them

  return next_possible_states

# now we will make functions to calculate the heuristic for misplaced-tiles and manhattan-distance (UCS has heuristic hardcoded to 0 so no need to make function for it)
def calculate_misplaced_tiles_heuristic(state):
  misplaced_tile_count = 0
  for i in range(TOTAL_TILES): # here we are iterating through all of the numbers in the current state
    if (state[i] != 0) and (state[i] != GOAL_STATE[i]): # we check if the number is not a blank space and also that the number is in the correct position as it should be in the goal state
      misplaced_tile_count += 1 # if not we increment counter by 1
  return misplaced_tile_count # at the end as misplaced tiles heuristic works, we return the number of tiles that are misplaced with respect to the goal state that we have defined

def calculate_manhattan_distance_heuristic(state):
  distance = 0 # here we intialize the distance as 0

  for i in range(TOTAL_TILES): # we iterate through all the numbers in the puzzle
    tile = state[i]

    if(tile != 0):
      number_row, number_col = find_index_coordinates(i) # for each number we find its currenmt position in the puzzle
      goal_row, goal_col = find_index_coordinates(tile-1) # we find the actual position the number should be in

      distance += abs(number_row - goal_row) + abs(number_col - goal_col) # then we take the difference in the current and goal, row and col in order to find how many steps is the number away from its goal state and add it in distance
# we do it for each number and all there distances together, this is how exactly the manhattan distance heuristic works.
  return distance

def solving_puzzle(initial_state, heuristic_function):
  nodes_queue = [] # the priority queue to store the states

  visited_nodes = set() # as set to keep track of the vsisited states

  start_node = Node(initial_state, cost = 0) # creating the starting initial state

  if heuristic_function: # calculating the heuristic for intial state based on searching method selected
    start_node.heuristic = heuristic_function(start_node.state)
  else:
    start_node.heuristic = 0

  start_node.a_star_f_cost = start_node.cost + start_node.heuristic

  heapq.heappush(nodes_queue, start_node) # adding the first intial state in priority queue for processing

  nodes_expanded = 0 # to track the expanded states throughout search
  max_queue_size = 0 # to track the max queue size went throughout search

  print("Now we will start searching....")

  start_time = time.time() # intializing time before search

  while nodes_queue: # now looping until our queue is not empty

    max_queue_size = max(max_queue_size, len(nodes_queue)) # calculating max queue size

    current_node = heapq.heappop(nodes_queue) # getting the node with highest priority

    visited_nodes.add(current_node.state) # adding to vsisited nodes for tracking

    # printing the traceback that we want to show
    print(f"\nThe best state to expand with g(n) = {current_node.cost} and h(n) = {current_node.heuristic} is...")
    print_puzzle_board(current_node.state)

    # checking if this is the goal state we defined, if yes we stop and print the metrics we calculated. 
    if current_node.state == GOAL_STATE:

      end_time = time.time()
      duration = end_time - start_time

      print(f"\nGoal state!")
      print(f"Time taken: {duration:.6f} seconds")
      print(f"Solution depth was {current_node.cost}")
      print(f"Number of nodes expanded: {nodes_expanded}")
      print(f"Max queue size: {max_queue_size}")

      return current_node

    # if not, we increment nodes expanded and calculate the next possible moves
    nodes_expanded += 1
    next_possible_moves = expand_state(current_node.state)

    # then process each possible move we calculated
    for next_state, move, cost in next_possible_moves:
      
      # create a new node with it's cost
      next_node_cost = current_node.cost + cost
      next_new_node = Node(next_state, parent = current_node, action = move, cost = next_node_cost)

      # calculating heuritic and evaluation function for new node as well
      if heuristic_function:
        next_new_node.heuristic = heuristic_function(next_state)
      else:
        next_new_node.heuristic = 0

      next_new_node.a_star_f_cost = next_new_node.cost + next_new_node.heuristic
      # then we check if we have visited this state before , if not add it to visisted now.
      if next_state not in visited_nodes:
        heapq.heappush(nodes_queue, next_new_node)
  # we continue this process and at end if we dont reach goal state then we declare failure
  print("\nSearch failed: Goal not reachable.")
  return None

def get_user_input():
    # asking the user to provide the custom board state
    print("\nEnter your 8-puzzle (3x3), using a 0 to represent the blank.")
    print("Enter the numbers for each row, delimited by spaces.")

    state_list = []

    # looping to get each row of the state
    for i in range(GRID_SIZE):
        while True:
            try:
                row_name = ""
                if i == 0:
                    row_name = "first"
                elif i == 1:
                    row_name = "second"
                elif i == 2:
                    row_name = "third"

                input_str = input(f"Enter the {row_name} row: ")
                row_numbers = [int(x) for x in input_str.split()]

                if len(row_numbers) != GRID_SIZE:
                    print(f"Error: Please enter exactly {GRID_SIZE} numbers separated by spaces for this row.")
                    continue

                state_list.extend(row_numbers)
                break

            except ValueError:
                print("Error: Please enter valid integer numbers separated by spaces.")
            except Exception as e:
                print(f"An unexpected error occurred during input for this row: {e}")

    if sorted(state_list) != list(range(TOTAL_TILES)):
         print(f"Error: Invalid puzzle input. Numbers should be {0} through {TOTAL_TILES - 1} exactly once across all rows.")
         return None

    return tuple(state_list)

# selectin gthe searching algorithm we are going to use
def select_heuristic_algorithm():
    print("\nSelect algorithm:")
    print("1) Uniform Cost Search")
    print("2) A* with Misplaced Tile Heuristic")
    print("3) A* with Manhattan Distance Heuristic")

    while True:
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice == '1':
            print("Selected: Uniform Cost Search")
            return None
        elif choice == '2':
            print("Selected: A* with Misplaced Tile Heuristic")
            return calculate_misplaced_tiles_heuristic
        elif choice == '3':
            print("Selected: A* with Manhattan Distance Heuristic")
            return calculate_manhattan_distance_heuristic
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def main():
  print("welcome to my 8-Puzzle Solver")

  DEFAULT_PUZZLE = (1,2,3,4,0,5,7,8,6) # default puzzle if user selects the default option

  initial_state = None
  while initial_state is None:
    puzzle_choice = input("Type '1' for a default puzzle, or '2' to enter your own: ")
    if puzzle_choice == '1':
      initial_state = DEFAULT_PUZZLE
    elif puzzle_choice == '2':
      initial_state = get_user_input()
    else:
      print("Invalid choice. Please enter '1' or '2'.")

  if initial_state is None:
    print("Could not get valid initial state. Exiting.")
    return

  # checking if the intial state is already goal state then no need to run algorithm
  if initial_state == GOAL_STATE:
    print("\nInitial state is already the goal state!")
    print("Solution depth was 0")
    print("Number of nodes expanded: 0")
    print("Max queue size: 1")
    return

  chosen_heuristic = select_heuristic_algorithm()
    # running the search 
  goal_node = solving_puzzle(initial_state, chosen_heuristic)

if __name__ == "__main__":
  main()