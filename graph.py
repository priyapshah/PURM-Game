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
            p = self.idfs(x, y, endX, endY, depth)
            if not len(p) == 0:
                return self.getPath(x, y, endX, endY, p)
        return []

    def idfs(self, x, y, endX, endY, depth):
        visited = []
        stack = []
        parents = {}

        curr = self.nodes[x][y]
        stack.append(curr)
        visited.append(curr)

        while stack:
            curr = stack.pop()

            if curr.depth >= depth:
                continue

            for neighbor in curr.adj_list:
                if neighbor not in visited:
                    self.colorSearch(neighbor, 'blue')
                    visited.append(neighbor)
                    stack.append(neighbor)
                    parents[neighbor] = curr
                    neighbor.depth = curr.depth + 1

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

        return path