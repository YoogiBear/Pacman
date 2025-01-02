##Pacman
import pygame as pg
from board import boards

## Window setup
pg.init()
WIDTH = 900
HEIGHT = 950
screen = pg.display.set_mode((WIDTH,HEIGHT))
timer = pg.time.Clock()
fps = 60 #Sets an fps limit
font = pg.font.Font('freesansbold.ttf',20)
pg.display.set_caption("Pacman")
level = boards #Used if there are more levels with different boards (maps)

def draw_board(level):
    num1 = ((HEIGHT-50)//32) #Determines the height of each tile if 32 are on the horizontal line
    num2 = (WIDTH//30) #Determines the width of each tile with 30 on the vertical line. // ensures integer is returned.
    for i in range(len(level)): #For each map that is assigned to a level
        for j in range(len(level[i])): #For each "tile" on map i (level i)
            if level[i][j] == 1: #Normal dot
                pg.draw.circle(screen, 'white',(j*num2 + (0.5*num2), i*num1 + (0.5*num1)),4)
            if level[i][j] == 2: #Bigger dot (Power up)
                pg.draw.circle(screen, 'white',(j*num2 + (0.5*num2), i*num1 + (0.5*num1)),10)


#Gameloop
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    draw_board(level)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    pg.display.flip()
pg.quit()



#Implementation of shortest route to Pacman (algorithms)