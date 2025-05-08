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

def get_user_input():
    print("\nEnter your 8-puzzle (3x3), using a 0 to represent the blank.")
    print("Enter the numbers for each row, delimited by spaces.")

    state_list = []

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