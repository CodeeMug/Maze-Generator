# Import area
import pygame
from Algorithm import AStarAlgorithm as AStar


# Maze object
class Maze(object):


    def __init__(self, **kwargs):
        
        self.thickness = kwargs['thickness']
        self.display = kwargs['display']
        self.resolution = kwargs['resolution']
        self.amount = kwargs['amount']
        self.totalCells = self.amount * self.amount 

        self.pathOrder = list()
        self.drawOrder = list()

        self.createCells()
        self.findNeighbors()

    
    def createCells(self):
        
        X = 0
        Y = 0
        self.maze = list()
        row = list()

        for number in range(self.totalCells):

            # Create cell object and store it
            cell = Cell(X=X, Y=Y, size=self.resolution, display=self.display)
            row.append(cell)
            
            # Update X and Y
            X += 1
            if X == self.amount:

                self.maze.append(row)
                row = list()
                X = 0
                Y += 1


    def drawMaze(self):

        for cell in self.drawOrder:
            cell.draw(self.thickness)


    def drawCells(self):

        colorDict = \
        {1: (200, 200, 235),
         'current': (100, 100, 135)}

        for cell in self.drawOrder:

            color = colorDict[cell.state]
            
            size = cell.size
            X = cell.X
            Y = cell.Y 

            pygame.draw.rect(
            self.display, color, 
            (X, Y, size, size))


    def findNeighbors(self):

        for rows in self.maze:
            for cell in rows:

                row = cell.row
                column = cell.column

                indexList = \
                [(row, column-1, 'up'), 
                (row+1, column, 'right'), 
                (row, column+1, 'down'), 
                (row-1, column, 'left')]

                for number in range(4):
                    index = indexList[number]

                    if (index[0] >= 0 and index[1] >= 0) and (index[0] < self.amount and index[1] < self.amount):
                        neighbor = self.maze[index[1]][index[0]]
                        cell.neighbors[index[2]] = neighbor
                

# Cell object
class Cell(object):

    
    def __init__(self, **kwargs):
        
        size = kwargs['size'] 
        self.X = (kwargs['X'] * size)
        self.Y = (kwargs['Y'] * size)
        W = self.X + size
        Z = self.Y + size

        self.state = 0
        self.neighbors = dict()
        self.walls = [1, 1, 1, 1]
        self.display = kwargs['display']
        
        self.row = kwargs['X']
        self.column = kwargs['Y']

        self.size = size
        self.positions = [(self.X, self.Y), (W, self.Y), (W, Z), (self.X, Z)]


    def draw(self, thickness):

        for index, wall in enumerate(self.walls):
            size = self.size
            nextIndex = 0 if index+1 == 4 else index + 1

            position = self.positions[index]
            nextPosition = self.positions[nextIndex]
            X = position[0], position[1]
            Y = nextPosition[0], nextPosition[1]

            if wall:
                pygame.draw.line(
                self.display, 
                (20, 20, 20), 
                X, Y, thickness)


# Current cell 
class CurrentCell(object):


    def __init__(self, **kwargs):

        self.cell = kwargs['cell']
        self.neighbors = self.cell.neighbors
        self.cell.state = 'current'
    

    def move(self, app):

        indexDict = \
        {'up': (0,2),
        'right': (1, 3),
        'down': (2, 0),
        'left': (3, 1)}

        if not app.stopMaze:
                
            choosenCell, direction = self.chooseNeighbor()
            currentCell = self.cell
            pathOrder = app.Maze.pathOrder
            drawOrder = app.Maze.drawOrder
            
            try:
                if choosenCell:
                    index = indexDict[direction]
                    currentCell.walls[index[0]] = 0
                    choosenCell.walls[index[1]] = 0
                        
                    pathOrder.append(choosenCell)
                    drawOrder.append(choosenCell)

                    self.cell.state = 1
                    app.currentCell = CurrentCell(
                    cell=choosenCell)

                else:
                    self.cell.state = 1
                    pathOrder.pop()
                    cell = pathOrder[-1]

                    app.currentCell = CurrentCell(
                    cell=cell)
            
            except IndexError:
                self.cell.state = 1
                app.stopMaze = True
                app.algorithm = AStar(app.Maze.maze, self.cell.size)


    def chooseNeighbor(self):
        import random

        # Check for possible neighbors
        possibleNeighbors = list()
        for key, neighbor in self.neighbors.items():
            if not neighbor.state:
                possibleNeighbors.append([neighbor, key])
        
        # Randomly choose neighbor
        if possibleNeighbors:
            return random.choice(possibleNeighbors)
        else:
            return (None, 0)