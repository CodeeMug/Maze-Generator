# Algorithmn object
class AStarAlgorithm:


    def __init__(self, maze, size):
        
        self.maze = maze
        self.size = size
        self.grid = list()
        self.transformList()

        self.columnsRows = len(self.grid[0])
        self.startPoint = self.grid[0][0]
        self.endPoint = self.grid[self.columnsRows-1][self.columnsRows-1]
        self.thickness = self.size - int(self.size*0.8)

        self.path = list()
        self.closedSet = list()
        self.openSet = list()
        self.openSet.append(self.startPoint)

    
    # Transform maze
    def transformList(self):
        
        indexList = \
        [(-1,  0),
         ( 0,  1),
         ( 1,  0),
         ( 0, -1)]

        # Complete grid
        columnsRow = len(self.maze)
        for rowIndex, row in enumerate(range(columnsRow)):
            gridRow = list()

            for columnIndex, cell in enumerate(range(columnsRow)):
                square = Cell(
                row=rowIndex,
                column=columnIndex,
                size=self.size,
                amount=columnsRow, 
                state=1)

                gridRow.append(square)
                
            self.grid.append(gridRow)

        # Transform 
        for row, rowObjects in enumerate(self.maze):
            for column, cell in enumerate(rowObjects):

                square = self.grid[row][column]
                square.state = 0
                position = (row, column)

                for index, wall in enumerate(cell.walls):
                    
                    adjust = indexList[index]
                    gridRow = position[0] + adjust[0]
                    gridColumn = position[1] + adjust[1]

                    if not wall:
                        neighbor = self.grid[gridRow][gridColumn]
                        square.neighbors.append(neighbor)


    # Draw path
    def draw(self, surface, app):
        import pygame
        
        # Draw optimal path
        coordinates = list()
        shadowCoordinates = list()

        for cell in self.path:
            size = cell.size
            X = (cell.column * size) + (size / 2)
            Y = (cell.row    * size) + (size / 2)

            vector = pygame.math.Vector2()
            vector.x = X
            vector.y = Y
            coordinates.append(vector)

            vector = pygame.math.Vector2()
            vector.x = X + (self.thickness - 1)
            vector.y = Y + (self.thickness - 1)
            shadowCoordinates.append(vector)

        if len(coordinates) != 1:
            
            pygame.draw.lines(
            surface, 
            (150, 150, 175),
            False, 
            shadowCoordinates,
            self.thickness + 1)

            pygame.draw.lines(
            surface, 
            (50, 100, 235),
            False, 
            coordinates,
            self.thickness)



    def createPath(self, final):
        
        currentCell = final
        self.path = list()
        self.path.append(currentCell)

        while currentCell.previous:
            currentCell = currentCell.previous
            self.path.append(currentCell)
    

    # Try to find optimal path
    def search(self, app):
        
        if not app.stopAlgorithm:
            if self.openSet:
                
                lowestPoint = self.openSet[0]
                for point in self.openSet:
                    if point.F < lowestPoint.F:
                        lowestPoint = point

                if lowestPoint == self.endPoint:
                    app.stopAlgorithm = True
                
                self.createPath(lowestPoint)
                self.openSet.remove(lowestPoint)
                self.closedSet.append(lowestPoint)

                for neighbor in lowestPoint.neighbors:
                    if neighbor not in self.closedSet:
                        temporaryG = lowestPoint.G + 1

                        if neighbor in self.openSet and temporaryG < neighbor.G:
                            neighbor.G = temporaryG

                        elif neighbor not in self.openSet:
                            neighbor.G = temporaryG                   
                            self.openSet.append(neighbor)
                        
                        neighbor.previous = lowestPoint
                        neighbor.H = manhattanDistance((neighbor.row, neighbor.column), (self.endPoint.row, self.endPoint.column))
                        neighbor.F = neighbor.G + neighbor.H

            else:
                app.stopAlgorithm = True


# Cell class
class Cell(object):


    def __init__(self, **kwargs):
        
        self.size = kwargs['size']
        self.state = kwargs['state']
        self.neighbors = list()
        self.previous = None

        self.direction = 'center'
        self.row = kwargs['row']
        self.column = kwargs['column']

        self.F = 0
        self.G = 0
        self.H = 0


# Calcule euclidean distance
def manhattanDistance(X, Y):

    # Calcule X      
    anwserX = 0
    add = 0

    for index, point in enumerate(X): 
        anwserX += (point * index) - add 
        add     +=  point 
    
    # Calcule Y
    anwserY = 0
    add = 0

    for index, point in enumerate(Y): 
        anwserY += (point * index) - add
        add     +=  point 

    return anwserX + anwserY 
      