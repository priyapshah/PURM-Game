from config import *
from path import *
import time
from heapq import *
import math as m
import random

# Create a node in the graph
class Node():
    def __init__(self, x, y):
        self.adj_list = []
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.gridX = x
        self.gridY = y

        self.g = 0
        self.h = 0
        self.f = 0

        self.depth = 0

# Create a graph of the tilemap/screen
class Graph():
    def __init__(self, tilemap, game):
        self.walls = ['W', 'F']
        self.nodes = []
        self.game = game

        self.c = [(250,235,215), (255,239,219), (238,223,204), (205,192,176), (139,131,120), (0,255,255), (127,255,212), (118,238,198), (102,205,170), (69,139,116), (240,255,255), (224,238,238), (193,205,205), (131,139,139), (227,207,87), (245,245,220), (255,228,196), (238,213,183), (205,183,158), (139,125,107), (0,0,0), (255,235,205), (0,0,255), (0,0,238), (0,0,205), (0,0,139), (138,43,226), (156,102,31), (165,42,42), (255,64,64), (238,59,59), (205,51,51), (139,35,35), (222,184,135), (255,211,155), (238,197,145), (205,170,125), (139,115,85), (138,54,15), (138,51,36), (95,158,160), (152,245,255), (142,229,238), (122,197,205), (83,134,139), (255,97,3), (255,153,18), (237,145,33), (127,255,0), (118,238,0), (102,205,0), (69,139,0), (210,105,30), (255,127,36), (238,118,33), (205,102,29), (139,69,19), (61,89,171), (61,145,64), (128,138,135), (255,127,80), (255,114,86), (238,106,80), (205,91,69), (139,62,47), (100,149,237), (255,248,220), (238,232,205), (205,200,177), (139,136,120), (220,20,60), (0,238,238), (0,205,205), (0,139,139), (184,134,11), (255,185,15), (238,173,14), (205,149,12), (139,101,8), (169,169,169), (0,100,0), (189,183,107), (85,107,47), (202,255,112), (188,238,104), (162,205,90), (110,139,61), (255,140,0), (255,127,0), (238,118,0), (205,102,0), (139,69,0), (153,50,204), (191,62,255), (178,58,238), (154,50,205), (104,34,139), (233,150,122), (143,188,143), (193,255,193), (180,238,180), (155,205,155), (105,139,105), (72,61,139), (47,79,79), (151,255,255), (141,238,238), (121,205,205), (82,139,139), (0,206,209), (148,0,211), (255,20,147), (238,18,137), (205,16,118), (139,10,80), (0,191,255), (0,178,238), (0,154,205), (0,104,139), (105,105,105), (30,144,255), (28,134,238), (24,116,205), (16,78,139), (252,230,201), (0,201,87), (178,34,34), (255,48,48), (238,44,44), (205,38,38), (139,26,26), (255,125,64), (255,250,240), (34,139,34), (220,220,220), (248,248,255), (255,215,0), (238,201,0), (205,173,0), (139,117,0), (218,165,32), (255,193,37), (238,180,34), (205,155,29), (139,105,20)]

        # Add node for every cell
        for row in range(len(tilemap)):
            self.nodes.append([])
            for col in range(len(tilemap[0])):
                self.nodes[row].append(Node(row, col))

        # Add edges
        for r in range(len(tilemap)):
            for c in range(len(tilemap[0])):
                if tilemap[c][r] in self.walls:
                    continue
                if c != 0 and tilemap[c-1][r] not in self.walls:
                    self.nodes[r][c].adj_list.append(self.nodes[r][c-1])
                if c != len(tilemap) - 1 and tilemap[c+1][r] not in self.walls:
                    self.nodes[r][c].adj_list.append(self.nodes[r][c+1])
                if r != 0 and tilemap[c][r-1] not in self.walls:
                    self.nodes[r][c].adj_list.append(self.nodes[r-1][c])
                if r != len(tilemap[0]) - 1 and tilemap[c][r+1] not in self.walls:
                    self.nodes[r][c].adj_list.append(self.nodes[r+1][c])


    # Backtrack to get the path
    def getPath(self, x, y, endX, endY, parents):
        path = []
        start = self.nodes[x][y]
        curr = self.nodes[endX][endY]

        while curr != start:
            path.insert(0, curr)
            curr = parents[curr]

        path.insert(0, start)

        return path

    # Breadth First Search Algorithm
    def bfs(self, x, y, endX, endY, showPath):
        visited = []
        queue = []
        parents = {}

        curr = self.nodes[x][y]
        queue.append(curr)
        visited.append(curr)

        while queue:
            curr = queue[0]
            queue.pop(0)
            if showPath:
                self.colorSearch(curr, 'red')

            for neighbor in curr.adj_list:
                if neighbor not in visited:
                    if showPath:
                        self.colorSearch(neighbor, 'blue')
                    visited.append(neighbor)
                    queue.append(neighbor)
                    parents[neighbor] = curr

                if neighbor == self.nodes[endX][endY]:
                    return self.getPath(x, y, endX, endY, parents)
        return[]

    # Depth First Search Algorithm
    def dfs(self, x, y, endX, endY):
        visited = []
        stack = []
        parents = {}

        curr = self.nodes[x][y]
        stack.append(curr)
        visited.append(curr)

        while stack:
            curr = stack.pop()
            self.colorSearch(curr, 'red')

            for neighbor in curr.adj_list:
                if neighbor not in visited:
                    self.colorSearch(neighbor, 'blue')
                    visited.append(neighbor)
                    stack.append(neighbor)
                    parents[neighbor] = curr

                if neighbor == self.nodes[endX][endY]:
                    return self.getPath(x, y, endX, endY, parents)
        return[]


    def aStar(self, x, y, endX, endY):
        visited = []
        frontier = []
        parents = {}

        curr = self.nodes[x][y]
        # heappush(frontier, (curr.f, id(curr), curr))
        frontier.append(curr)
      
        while frontier:
            # curr = heappop(frontier)[2]
            curr = self.findMin(frontier)
            frontier.remove(curr)
            visited.append(curr)

            for neighbor in curr.adj_list:
                if neighbor not in visited:
                    self.colorSearch(neighbor, 'blue')
                    visited.append(neighbor)
                    parents[neighbor] = curr

                    neighbor.g = curr.g + self.distance(neighbor.gridX, neighbor.gridY, curr.gridX, curr.gridY)
                    neighbor.h = self.distance(neighbor.gridX, neighbor.gridY, endX, endY)
                    neighbor.f = neighbor.g + neighbor.h

                    frontier.append(neighbor)
                    # heappush(frontier, (neighbor.f, id(neighbor), neighbor))

                if neighbor == self.nodes[endX][endY]:
                    return self.getPath(x, y, endX, endY, parents)
        return[]

    def distance(self, x, y, endX, endY):
        return m.sqrt(m.pow((x-endX),2) + m.pow((y-endY),2))

    def findMin(self, list):
        self.minVal = float('inf')
        for node in list:
            if node.f < self.minVal:
                self.minVal = node.f
                self.minNode = node
        return self.minNode

    def iddfs(self, x, y, endX, endY):
        for depth in range(100):
            p = self.idfs(x, y, endX, endY, depth, self.c[depth % 145])
            if not len(p) == 0:
                return self.getPath(x, y, endX, endY, p)
        return []

    def idfs(self, x, y, endX, endY, depth, color):
        visited = []
        stack = []
        parents = {}

        curr = self.nodes[x][y]
        curr.depth = 0
        print(curr.depth)
        stack.append(curr)
        visited.append(curr)

        while stack:
            curr = stack.pop()

            if curr.depth >= depth:
                continue

            visited.append(curr)
            self.colorSearch(curr, color)

            for neighbor in curr.adj_list:
                
                if neighbor not in visited:
                    parents[neighbor] = curr
                    neighbor.depth = curr.depth + 1
                    stack.append(neighbor)

                if neighbor == self.nodes[endX][endY]:
                    return parents
        return[]


    def colorSearch(self, neighbor, color):
        ExpandPath(self.game, int(neighbor.x/32), int(neighbor.y/32), color)
        time.sleep(0.01)
        self.game.draw()


    def mazeDFS(self, x, y):
        visited = []
        stack = []
        path = []

        curr = self.nodes[x][y]
        stack.append(curr)
        visited.append(curr)

        while stack:
            curr = stack.pop()
            neighbors = []
            for neighbor in curr.adj_list:
                if neighbor not in visited:
                    neighbors.append(neighbor)
                    visited.append(neighbor)
            if len(neighbors) > 0:
                nextNode = neighbors[random.randint(0, len(neighbors)-1)]
                stack.append(nextNode)
                path.append(nextNode)
        
            if not stack and len(path) < 180:
                visited = []
                stack.append(path[random.randint(0, len(path)-1)])
                # stack.append(self.nodes[random.randint(0, 20)][random.randint(0, 15)])


        return path