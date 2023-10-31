import math,random
import mcschematic as mc
import pygame as pg
pg.init()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]


    def get_neighbors(self, cell):
        neighbors = []
        if cell.x > 0 and not self.grid[cell.y][cell.x - 1].visited:
            neighbors.append(self.grid[cell.y][cell.x - 1])
        if cell.x < self.width - 1 and not self.grid[cell.y][cell.x + 1].visited:
            neighbors.append(self.grid[cell.y][cell.x + 1])

        if cell.y > 0 and not self.grid[cell.y - 1][cell.x].visited:
            neighbors.append(self.grid[cell.y - 1][cell.x])
        if cell.y < self.height - 1 and not self.grid[cell.y + 1][cell.x].visited:
            neighbors.append(self.grid[cell.y + 1][cell.x])

        return neighbors



def remove_walls(current_cell, neighbor_cell):
    x_diff = current_cell.x - neighbor_cell.x
    y_diff = current_cell.y - neighbor_cell.y

    if x_diff == 1:
        current_cell.walls["left"] = False
        neighbor_cell.walls["right"] = False
    elif x_diff == -1:
        current_cell.walls["right"] = False
        neighbor_cell.walls["left"] = False
    elif y_diff == 1:
        current_cell.walls["top"] = False
        neighbor_cell.walls["bottom"] = False
    elif y_diff == -1:
        current_cell.walls["bottom"] = False
        neighbor_cell.walls["top"] = False


def generate_maze(width,height):
    maze = Maze(width,height)

    stack = []
    start_cell = maze.grid[0][0]
    start_cell.visited = True
    stack.append(start_cell)

    while stack:
        cell = stack.pop()
        neighbors = maze.get_neighbors(cell)
        if neighbors:
            neighbor = random.choice(neighbors)
            remove_walls(cell, neighbor)
            stack.append(cell)
            cell = neighbor
            cell.visited = True
            stack.append(cell)
    return maze




def draw_maze(maze,cellsize):
    displaysize = (cellsize*maze.width,cellsize*maze.height)

    display = pg.display.set_mode(displaysize)
    
    for b,row in enumerate(maze.grid):
        for g,col in enumerate(row):
            cell = maze.grid[b][g]
            relx,rely = cellsize*cell.x,cellsize*cell.y

            pg.draw.rect(display,(0,0,0),(relx,rely,cellsize,cellsize))

            if cell.walls["top"]:
                pg.draw.line(display,(255,255,255),(relx,rely),(relx+cellsize,rely),3)
            if cell.walls["right"]:
                pg.draw.line(display, (255, 255, 255), (relx + cellsize, rely), (relx + cellsize, rely + cellsize),3)
            if cell.walls["bottom"]:
                pg.draw.line(display, (255, 255, 255), (relx + cellsize, rely + cellsize), (relx, rely + cellsize),3)
            if cell.walls["left"]:
                pg.draw.line(display, (255, 255, 255), (relx, rely + cellsize), (relx, rely),3)            

    pg.display.flip()

def generate_schematic(maze, corridor_size, wall_height,floor_block="minecraft:stone",wall_block="minecraft:stone",roof_block="minecraft:air"):
    schem = mc.MCSchematic()
    corridor_size += 2
    wall_height += 2

    for elevation in range(1, wall_height + 1):
        for n1, row in enumerate(maze.grid):
            for n2, cell in enumerate(row):
                relx = (corridor_size - 1) * n2
                rely = (corridor_size - 1) * n1

                if elevation == 1:
                    # Place the floor at the bottom elevation
                    for i in range(corridor_size):
                        for j in range(corridor_size):
                            schem.setBlock((relx + i, elevation, rely + j),floor_block)

                # Place walls according to the maze structure
                if cell.walls["top"]:
                    for i in range(corridor_size):
                        schem.setBlock((relx + i, elevation, rely), wall_block)
                if cell.walls["bottom"]:
                    for i in range(corridor_size):
                        schem.setBlock((relx + i, elevation, rely + (corridor_size - 1)), wall_block)
                if cell.walls["left"]:
                    for i in range(corridor_size):
                        schem.setBlock((relx, elevation, rely + i), wall_block)
                if cell.walls["right"]:
                    for i in range(corridor_size):
                        schem.setBlock((relx + (corridor_size - 1), elevation, rely + i), wall_block)


                if elevation == wall_height:
                    # Place the floor at the bottom elevation
                    for i in range(corridor_size):
                        for j in range(corridor_size):
                            schem.setBlock((relx + i, elevation, rely + j),roof_block)




    return schem



X = int(input("insert the x size of the maze > "))
Z = int(input("insert the z size of the maze > "))
Y = int(input("insert the wall height of the maze > "))
W = int(input("insert the width of the corridoors > "))
B1 = input("insert the block for the floor (ex minecraft:stone) > ")
B2 = input("insert the block for the walls (ex minecraft:stone) > ")
B3 = input("insert the block for the roof (ex minecraft:stone) > ")


maze = generate_maze(X,Z)
draw_maze(maze,20)
schematic = generate_schematic(maze,W,Y,floor_block=B1,wall_block=B2,roof_block=B3)

schematic.save(  "", "palle", mc.Version.JE_1_18_2)
print("schematic saved as palle.schem")
