"""
Navigator script
Handles the A* pathfinding ang creates "navigators" for enemies to use
"""

from GameManager import Game

class Navigator:
    NAVIGATORS = []

    def __init__(self):
        self._queue = []
        Navigator.NAVIGATORS.append(self)
    
    def enqueue(self, pos : tuple): self._queue.append(pos)
    def front(self): 
        if len(self._queue) == 0: 
            self._calculate_route() # Recalculate the route if empty
        return self._queue[0]
    def clear(self): self._queue = []
    def dequeue(self):
        if len(self._queue) == 0: 
            self._calculate_route() # Recalculate the route if empty
        return self._queue.pop(0)

    # Calculates the fastest route to the player using A*
    def _calculate_route(self):
        self.clear()
        plr = Game.get_instance().get_player()
        
        # A* Pathfinding
        self.enqueue((plr._position[0] // 48 * 48, plr._position[1] // 48 * 48)) # Testing !!!!!!
    
    def _destroy(self):
        Navigator.NAVIGATORS.remove(self)

    # Triggers recalculation of routes for all navigators
    @staticmethod
    def update_all_navs():
        for nav in Navigator.NAVIGATORS:
            nav._calculate_route()