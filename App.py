# Import area
import pygame, sys, os
from win32api import GetSystemMetrics as metrics
from Objects import Maze, CurrentCell


# App class
class App:


    # Initialize methods
    def __init__(self):

        # Init pygame and display
        self.initDisplay()

        # Setup variables
        self.RESOLUTION = 20
        self.LINETHICKNESS = 2
        self.FPS = 180

        self.perRowColumn = self.WIDTH // self.RESOLUTION
        self.active = True
        self.stopAlgorithm = False
        self.Clock = pygame.time.Clock()

        # Run screen
        self.setup()
        self.runDisplay()


    def initDisplay(self):

        # Init dimensions
        self.WIDTH  = 600
        self.HEIGHT = 600
        XOFFSET = (metrics(0) -  self.WIDTH) // 2
        YOFFSET = (metrics(1) - self.HEIGHT) // 2

        # Center the display
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{XOFFSET},{YOFFSET}"

        # Init display
        pygame.init()
        pygame.display.set_caption("Maze generator")
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))


    # Setup & update objects
    def setup(self):
        
        self.stopMaze = False

        # Create Maze object
        self.Maze = Maze(
        display=self.display,
        resolution=self.RESOLUTION,
        thickness=self.LINETHICKNESS,
        amount=self.perRowColumn
        )

        # Create current cell
        cell = self.Maze.maze[0][0]
        self.Maze.pathOrder.append(cell)
        self.Maze.drawOrder.append(cell)
        self.currentCell = CurrentCell(
        cell=cell
        )

    
    def update(self):
        
        # Draw maze cells
        self.Maze.drawCells()

        # Move current cell
        self.currentCell.move(self)

        # Run search algorithm
        if self.stopMaze:
            self.Clock.tick(60)
            self.algorithm.search(self)
            self.algorithm.draw(self.display, self)

        # Draw maze wals
        self.Clock.tick(self.FPS)
        self.Maze.drawMaze()


    # Run display
    def runDisplay(self):
        
        # Run objects
        while self.active:
            
            self.display.fill((20, 20, 20))
            self.Clock.tick(self.FPS)
            self.update()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False
                    pygame.quit()
                    sys.exit()


# Execution area
App()