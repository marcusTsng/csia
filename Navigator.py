"""
Navigator script
Handles the A* pathfinding ang creates "navigators" for enemies to use
"""

from GameManager import Game

class Navigator:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, pos : tuple): self.queue.append(pos)
    # def dequeue(self): return self.points.pop(-1)
    def front(self): return self.queue[0]
    def clear(self): self.queue = []

    def dequeue(self):
        if len(self.queue) == 0: # Recalculate the queue if empty
            self._calculate_route()
        return self.queue.pop(0)

    # Calculates the fastest route to the player using A*
    def _calculate_route(self):
        self.clear()
        plr = Game.get_instance().get_player()
        self.enqueue((plr._position[0] // 48 * 48, plr._position[1] // 48 * 48)) # Testing
