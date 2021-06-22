from config import *

class Node():
    def __init__(self, x, y):
        self.adj_list = []
        self.x = x
        self.y = y

class Graph():
    def __init__(self, tilemap):
        self.nodes = []

        # Add node for every cell
        for row in range(len(tilemap)):
            self.nodes.append([])
            for col in range(len(tilemap[0])):
                self.nodes[row].append(Node(row * TILESIZE, col * TILESIZE))

        # Add edges
        for r in range(len(tilemap)):
            for c in range(len(tilemap[0])):
                if tilemap[c][r] == 'W':
                    continue
                if c != 0 and tilemap[c-1][r] != 'W':
                    self.nodes[r][c].adj_list.append(self.nodes[r][c-1])
                if c != len(tilemap) - 1 and tilemap[c+1][r] != 'W':
                    self.nodes[r][c].adj_list.append(self.nodes[r][c+1])
                if r != 0 and tilemap[c][r-1] != 'W':
                    self.nodes[r][c].adj_list.append(self.nodes[r-1][c])
                if r != len(tilemap[0]) - 1 and tilemap[c][r+1] != 'W':
                    self.nodes[r][c].adj_list.append(self.nodes[r+1][c])

    #adversarial search
                
    def getPath(self, x, y, endX, endY, parents):
        path = []
        start = self.nodes[x][y]
        curr = self.nodes[endX][endY]

        while curr != start:
            path.insert(0, curr)
            curr = parents[curr]

        path.insert(0, start)

        return path

    def bfs(self, x, y, endX, endY):
        visited = []
        queue = []
        parents = {}

        curr = self.nodes[x][y]
        queue.append(curr)
        visited.append(curr)

        while queue:
            curr = queue[0]
            queue.pop(0)

            for neighbor in curr.adj_list:
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)
                    parents[neighbor] = curr

                if neighbor == self.nodes[endX][endY]:
                    return self.getPath(x, y, endX, endY, parents)
        return[]
