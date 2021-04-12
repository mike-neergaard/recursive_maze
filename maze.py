import random
import sys
import os
import time
import argparse

directions  = ["N", "S", "E", "W"]
backmap = {"N":"S", "S":"N", "E":"W", "W":"E"}
ANIMATE = False
DEBUG = False

def clear():
    """ cler

    clear the screen
    """
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def key_string(a):
    """ key_string

    The key_string function turns a [row,column] pair into a string
    
    Args:
        a (list):  A [row,column] pair

    Returns:
        str: a string of the form "row,col"
    """
    return str(a[0])+","+str(a[1])

def connect_neighbors(maze, this_cell, width, height): 
    """ connect_neighbors
    
    The connect_neighbors function recursively deletes walls between cells

    Args:
        maze (dict): The maze itself
        this_cell (list): A [row, column] coordinate pair
        width (int): The width of the maze
        height(int): The height of the maze

    Returns:
        dict: The maze
    """
    if ANIMATE: print_maze(maze, width, height)
    this_cell_key = key_string(this_cell)
    row = this_cell[0]
    col = this_cell[1]

    # Mark this cell as visited
    maze[this_cell_key]["Visited"] = True

    #No?  We have to process it then.

    #Let's randomize our directions
    random.shuffle(directions)
    
    for n in directions:
        do_next = False
        if n == "N":
            next_cell = [row-1, col]
        elif n == "S":
            next_cell = [row+1, col]
        elif n == "E":
            next_cell = [row, col+1]
        elif n == "W":
            next_cell = [row, col-1]
        else: 
            # This is not possible.  The code must never reach this point
            print("Random direction chosen that is not N, S, E, or W: "+n, file=sys.stderr)
            exit(1)

        next_cell_key = key_string(next_cell)
        if next_cell_key in maze: 
            if maze[next_cell_key]["Visited"] == True: continue
            # Erase wall 
            maze[this_cell_key][n]  = False 
            maze[next_cell_key][backmap[n]] = False 
            # Process next cell 
            if DEBUG: print(n+":"+ this_cell_key + " -> "+next_cell_key+ " "+str(maze[this_cell_key])+" -> "+str(maze[next_cell_key])) 
            connect_neighbors(maze, next_cell, width, height)



def make_maze(width, height):
    """ make_maze
    
    The make_maze function makes a maze.  
    The maze is a dictionary.  Each element of the dictionary is a cell.  
    The key of each entry is the x,y location of the cell

    Args:
        width (int): The width of the maze
        height(int): The height of the maze

    Returns:
        dict: The maze
    """

    # Create an empty dictionary to hold the maze
    ret_maze = {}

    # Fill the matrix with fully walled cells
    for row in range(height):
        for col in range(width):
            ret_maze[key_string([row,col])] = {"Visited": False, "N" : True, "S" : True, "E" : True, "W" : True}



    # Start recursive exploration
    random_cell = [random.randrange(height), random.randrange(width)]
    if DEBUG: print("Starting with "+str(random_cell))

    # This generates the complete matrix
    connect_neighbors(ret_maze, random_cell, width, height)

    # Opening in upper left
    ret_maze[key_string([0,0])]["W"] = False
    if ANIMATE: print_maze(ret_maze, width, height)

    # Opening in lower right
    ret_maze[key_string([height-1,width-1])]["E"] = False
    if ANIMATE: print_maze(ret_maze, width, height)

    return ret_maze


def print_maze(maze, width, height):
    """ print_maze
    
    The make_maze function makes a maze.  
    The maze is a dictionary.  Each element of the dictionary is a cell.  
    The key of each entry is the x,y location of the cell

    Args:
        maze (dict): The maze itself
        width (int): The width of the maze
        height(int): The height of the maze

    Returns:
        -
    """
    # Clear the screen
    clear()

    #Print the very top of the maze, which always has a boundary
    for col in range(width):
        if maze[key_string([0, col])]["N"] == True:
            print("__", end="")
        else:
            print(" ", end="")
    print("_")

    # Print the rest of the maze
    for row in range(height):
        for col in range(width):
            this_cell_key = key_string([row,col])
            if maze[this_cell_key]["W"] == True:
                print("|", end="")
            else:
                if row == height-1: 
                    print("_", end="")
                else: 
                    print(" ", end="")

            if maze[this_cell_key]["S"] == True:
                print("_", end="")
            else:
                print(" ", end="")

        if maze[key_string([row, width-1])]["E"] == True:
            print("|")
        else:
            print(" ")

    # If we are animating, everything needs to finish printing right now
    sys.stdout.flush()

    if ANIMATE: time.sleep(0.2)

def main(width, height, animation, random_seed):

    random.seed(random_seed)
    global ANIMATE
    if animation: ANIMATE = True

    # Make the maze
    maze = make_maze(width, height)

    # Print the maze
    print_maze(maze, width, height)


if __name__ == "__main__":

    #Set up defaults
    width = 30
    height = 30
    animate = False
    random_seed = time.time()

    # Command-line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", "--width", type = int, help = "width of maze")
    parser.add_argument("-H", "--height", type = int, help = "height of maze")
    parser.add_argument("-A", "--ANIMATE", action = "store_true", help="turn on animation of maze generation process")
    parser.add_argument("-s", "--seed", type = int, help = "random seed")
    parser.add_argument("-d", "--debug", action = "store_true", help= "turn on debug strings")
    args = parser.parse_args()

    #Set up arguments to call main
    if args.ANIMATE: animate=True
    if args.width != None and args.width > 0:
        width = args.width
    if args.height != None and args.height > 0:
        height = args.height
    if args.seed != None and args.seed > 0:
        random_seed = args.seed
    if args.debug: DEBUG = True

    main(width, height, animate, random_seed)
