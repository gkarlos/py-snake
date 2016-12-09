from Tkinter import *
import time
from random import randint

WIDTH = 30
HEIGHT = 30
SQUARE_WIDTH = 12
SQUARE_HEIGHT = 12
WINDOW_WIDTH = SQUARE_WIDTH * WIDTH + SQUARE_WIDTH*2
WINDOW_HEIGHT = SQUARE_HEIGHT * HEIGHT + SQUARE_HEIGHT*2
DELAY = 100
CELL_SNAKE = "OliveDrab1"
CELL_EMPTY = "snow3"
CELL_FOOD = "red"

class Direction(object):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def copy(self):
        return Cell(self.x, self.y)
    
    def equals(self, cell):
        return self.x == cell.x and self.y == cell.y
    
    def __repr__(self):
        return str(self.x) + ", " + str(self.y)


class Snake(object):
    def __init__(self, initHead, direction):
        self.originalHead = initHead
        self.originalDirection = direction
        self.body = [initHead]
        self.direction = direction
        #self.boardWidth = boardWidth
        #self.boardHeight = boardHeight
    
    def __moveDirection(self, direction):
        newHead = self.body[0].copy()
        if direction == Direction.RIGHT:
            newHead.x = (newHead.x + 1) % WIDTH
        elif direction == Direction.LEFT:
            newHead.x = (newHead.x - 1) % WIDTH
        elif direction == Direction.UP:
            newHead.y = (newHead.y - 1) % HEIGHT
        elif direction == Direction.DOWN:
            newHead.y = (newHead.y + 1) % HEIGHT
        #print newHead
        return newHead
    
    def containsCell(self, cell):
        for c in self.body:
            if cell.equals(c):
                return True
        return False
    
    def init(self):
        self.body = [self.originalHead]
        self.direction = self.originalDirection
        
    def head(self):
        return self.body[0]
    
    def moveNormal(self, direction):
        self.body.insert(0, self.__moveDirection(direction))
        return self.body.pop()
        
    def moveIncrease(self, direction):
        self.body.insert(0, self.__moveDirection(direction))
    

class SnakeGame(object):
    def __init__(self):
        self.root = Tk()
        self.root.resizable(0,0)
        self.snake = Snake(Cell(0,0), Direction.RIGHT)
        self.keepRunning = False
        self.gameOverColor = CELL_FOOD
        self.food = self.newApple()
        self.__init()
    
    def __init(self):
        self.root.title("Snake")
        self.frame = Frame(self.root, width = WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.frame.pack()
        self.canvas = Canvas(self.frame, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()
        self.__grid()
    
    def newApple(self):
        newApple = Cell(randint(0,WIDTH-1), randint(0,HEIGHT-1))
        while self.snake.containsCell(newApple):
            newApple = Cell(randint(0,WIDTH), randint(0,HEIGHT))
        return newApple
        
    def __grid(self):
        x,y = SQUARE_WIDTH,SQUARE_HEIGHT
        xs = [x+SQUARE_WIDTH*i for i in range( WIDTH + 1)]
        ys = [y+SQUARE_HEIGHT*i for i in range( HEIGHT + 1)]
        self.rectangles = [[self.canvas.create_rectangle(xs[j], ys[i], xs[j+1], ys[i+1], fill=CELL_EMPTY) for j in range(WIDTH)] for i in range(HEIGHT)]
        self.cells = [[Cell(x,y) for y in range(HEIGHT)] for x in range(WIDTH)]
    
    def initDraw(self):
        self.canvas.itemconfig(self.rectangles[self.food.y][self.food.x], fill = CELL_FOOD)
        for cell in self.snake.body:
            self.canvas.itemconfig(self.rectangles[cell.y][cell.x], fill=CELL_SNAKE)
            
    def draw(self):
        stillAlive = True
        self.canvas.itemconfig(self.rectangles[self.food.y][self.food.x], fill = CELL_FOOD)
        if self.snake.head().equals(self.food):
            self.snake.moveIncrease(self.snake.direction)
            self.food = self.newApple()
        else:
            
            delete = self.snake.moveNormal(self.snake.direction)
            oldBody = [delete] + self.snake.body[1:]
            for cell in oldBody:
                if cell.equals(self.snake.head()):
                    stillAlive = False
            self.canvas.itemconfig(self.rectangles[delete.y][delete.x], fill = CELL_EMPTY)
        for cell in self.snake.body:
            self.canvas.itemconfig(self.rectangles[cell.y][cell.x], fill=CELL_SNAKE)
        if not stillAlive:
            self.gameOver()
            
    def game(self):
        if self.keepRunning:
            self.draw()
            self.root.after(DELAY, lambda: self.game())
    
    def pauseUnpause(self, event):
        if self.keepRunning:
            self.keepRunning = False
        else:
            self.keepRunning = True
            self.game()
        
    def leftArrow(self, event):
        self.snake.direction = Direction.LEFT if self.snake.direction != Direction.RIGHT else Direction.RIGHT
        if not self.keepRunning:
            self.keepRunning = True
            self.game()

    def rightArrow(self, event):
        self.snake.direction =  Direction.RIGHT if self.snake.direction != Direction.LEFT else Direction.LEFT
        if not self.keepRunning:
            self.keepRunning = True
            self.game()
            
    def upArrow(self, event):
        self.snake.direction = Direction.UP if self.snake.direction != Direction.DOWN else Direction.DOWN
        if not self.keepRunning:
            self.keepRunning = True
            self.game()
            
    def downArrow(self, event):
        self.snake.direction = Direction.DOWN if self.snake.direction != Direction.UP else Direction.UP
        if not self.keepRunning:
            self.keepRunning = True
            self.game()
    
    def gameOver(self):
        self.keepRunning = False
        self.restart()
    
    def clearBoard(self):
        for cell in self.snake.body:
            self.canvas.itemconfig(self.rectangles[cell.y][cell.x], fill=CELL_EMPTY)
            
    def restart(self):
        self.clearBoard()
        self.snake.init()
        self.initDraw()
        #self.game()
        
    def start(self):
        self.root.bind("<Left>", self.leftArrow)
        self.root.bind("<Right>", self.rightArrow)
        self.root.bind("<Up>", self.upArrow)
        self.root.bind("<Down>", self.downArrow)
        self.root.bind("<space>", self.pauseUnpause)
        self.initDraw()
        self.game()
        self.root.mainloop()



game= SnakeGame().start()
        
            