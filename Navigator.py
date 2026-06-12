"""
Navigator script
Handles the A* pathfinding ang creates "navigators" for enemies to use
"""

from GameManager import Game, GRID_SIZE
import heapq

game_manager = Game.get_instance()

COOLDOWN = 1

# Functions and classes for A* 
class NavCell():
    def __init__(self):
        self.contents = None
        self.parent_i = 0
        self.parent_j = 0
        self.f = float("inf")
        self.g = float("inf")
        self.h = 0

def get_target():
    plr = Game.get_instance().get_player()



    return round(plr._position[0] / 48) * 48, round(plr._position[1] / 48) * 48

def is_valid(i, j): 
    if i >= 15 or j >= 15 or i < 0 or j < 0:
        return False
    if game_manager.get_grid().grid[i][j] != None:
        return False
    return True

def reached_destination(i, j, target): 
    return (i * 48, j * 48) == target

def calculate_h_value(i, j, targ):
    targ_x = int(targ[0] // 48)
    targ_y = int(targ[1] // 48)
    return ((i - targ_x) ** 2 + (j - targ_y) ** 2) ** 0.5

def trace_path(cells, targ):
    path = []
    # dest = get_target()
    row = int(targ[0] // 48)
    col = int(targ[1] // 48)

    # Trace the path from destination to source using parent cells
    while not (cells[row][col].parent_i == row and cells[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cells[row][col].parent_i
        temp_col = cells[row][col].parent_j
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append((row, col))
    # Reverse the path to get the path from source to destination
    path.reverse()
    return path


# Navigator class
class Navigator:
    NAVIGATORS = []

    def __init__(self, instance):
        self._queue = []
        self.instance = instance
        self._last_calculation = 0
        Navigator.NAVIGATORS.append(self)

    def enqueue(self, pos : tuple): self._queue.append(pos)
    def front(self): 
        if len(self._queue) == 0: 
            self._calculate_route() # Recalculate the route if empty

            if len(self._queue) == 0: # In case the route is still empty, simply make a direct path towards the player
                return get_target() 
        return self._queue[0]
    def clear(self): self._queue = []
    def dequeue(self):
        if len(self._queue) == 0: 
            self._calculate_route() # Recalculate the route if empty
        return self._queue.pop(0)

    # Calculates the fastest route to the player using A*
    def _calculate_route(self):
        print(get_target())
        # Cooldown for recalculating routes
        if game_manager.time - self._last_calculation < COOLDOWN: return
        self._last_calculation = game_manager.time

        self.clear()
        plr = Game.get_instance().get_player()
        target = get_target()
        

        # A* Pathfinding
        pos = self.instance._position
        i, j = int(pos[0] // 48), int(pos[1] // 48) # Get the enemy's position on the grid
 
        if not is_valid(i, j) or reached_destination(i, j, target): # If enemy cannot navigate to the player, take a straight path towards the player
            self.enqueue(target)
            return
        

        # Initialize the closed list
        closed_list = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        cell_details = [[NavCell() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        # Starting cell
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j

        # Initialize the open list with the starting cell 
        open_list = []
        heapq.heappush(open_list, (0, i, j))
    
        # Repeat until the open list is empty or the destination is found
        found_end = False
        while len(open_list) > 0:

            # Find the cell with the lowest f and pop it off the open list

            cell = heapq.heappop(open_list) # Pop the minimum f value from the heap
            i, j = int(cell[1]), int(cell[2])
            closed_list[i][j] = True
            
            # Look through the cell's 8 successors in each direction
            dirs =  [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for d in dirs:
                new_i, new_j = i + d[0], j + d[1]

                if is_valid(new_i, new_j) and not closed_list[new_i][new_j]:
                    
                    # Check for diagonal movement
                    is_diagonal = (d[0] != 0 and d[1] != 0) 

                    # If moving diagonally, try not to bump into corner walls:
                    if is_diagonal: 
                        # Check the two straight tiles flanking the diagonal path
                        if not is_valid(i + d[0], j) or not is_valid(i, j + d[1]):
                            continue 

                    # If the destination is reached, trace back the path and add cells to the queue
                    if reached_destination(new_i, new_j, target):
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        found_end = True
                        
                        # Trace the path, convert from grid format to coordinates, and push to the queue
                        for cell in trace_path(cell_details, target):
                            self.enqueue((cell[0] * 48, cell[1] * 48))

                        # In case the queue is still empty:
                        if len(self._queue) == 0:
                            self.enqueue(target)

                        return
                    else:
                        # Check the new g,h,f values for the cell
                        g_new = cell_details[i][j].g + 1.0 if not is_diagonal else cell_details[i][j].g + 1.414 # Diagonal cells take longer to cross
                        h_new = calculate_h_value(new_i, new_j, target)
                        f_new = g_new + h_new

                        # If the cell is not yet in the open list, or the f of the successor is smaller than the cell's f
                        if cell_details[new_i][new_j].f == float("inf") or f_new < cell_details[new_i][new_j].f:
                            heapq.heappush(open_list, (f_new, new_i, new_j))

                            cell_details[new_i][new_j].f = f_new
                            cell_details[new_i][new_j].g = g_new
                            cell_details[new_i][new_j].h = h_new
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j
        if not found_end: # Destination not found - simply walk towards the enemy
            self.enqueue(target)




    
    def _destroy(self):
        Navigator.NAVIGATORS.remove(self)

    # Triggers recalculation of routes for all navigators
    @staticmethod
    def update_all_navs():
        for nav in Navigator.NAVIGATORS:
            nav._calculate_route()