##Pacman
import pygame as pg
from board import boards
import math

PI = math.pi

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
color = 'blue' #Color of walls

def draw_board(level):
    num1 = ((HEIGHT-50)//32) #Determines the height of each tile if 32 are on the horizontal line
    num2 = (WIDTH//30) #Determines the width of each tile with 30 on the vertical line. // ensures integer is returned.
    for i in range(len(level)): #For each map that is assigned to a level and defines the vertical placement number
        for j in range(len(level[i])): #For each tile on map[i] and defines the horizontal placement number
            if level[i][j] == 1: #Normal dot
                pg.draw.circle(screen, 'white',(j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)),4) #Finds the center of the tile
            if level[i][j] == 2: #Bigger dot (Power up)
                pg.draw.circle(screen, 'white',(j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)),10)
            if level[i][j] == 3: #Vertical wall
                pg.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4: #Horizontal wall
                pg.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5*num1)), 3)
            if level[i][j] == 9: #Ghost exit wall
                pg.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5*num1)), 3)
            if level[i][j] == 5: #Top right corner
                #pg.draw.circle(screen, color,()
                pg.draw.arc(screen, color,[(j * num2 - (0.5*num2)), (i * num1 + (0.5* num1)), num2, num1], 0, PI/2, 3)
            if level[i][j] == 6: #Top left corner
                pg.draw.arc(screen, color,[(j * num2 + (0.5*num2)), (i * num1 + (0.5* num1)), num2, num1], PI/2, PI, 3)
            if level[i][j] == 7: #Bottom left corner
                pg.draw.arc(screen, color,[(j * num2 + (0.5*num2)), (i * num1 - (0.5* num1)), num2, num1], PI, 3*PI/2, 3)
            if level[i][j] == 8: #Bottom right corner
                pg.draw.arc(screen, color,[(j * num2 - (0.5*num2)), (i * num1 - (0.5* num1)), num2, num1], 3*PI/2, 2*PI, 3)

player_images = []
for i in range(1,5):
    img = pg.image.load(f"assets/player_images/{i}.png")
    scaled = pg.transform.scale(img, (45,45))
    player_images.append(scaled)
player_x = 425
player_y = 663
direction = 0
counter = 0

def draw_player():
    if direction == 0: #Right
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1: #Left
        screen.blit(pg.transform.flip(player_images[counter // 5], True, False),(player_x, player_y)) #True and False determines whether or not to flip on x,y axis.
    elif direction == 2: #Up
        screen.blit(pg.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3: #Down
        screen.blit(pg.transform.rotate(player_images[counter // 5], -90), (player_x, player_y))
"""
ghosts = []
def draw_ghosts():
    for i in range(1,4):
        img = pg.image.load(f"assets/ghost_images/{i}.png")
        ghosts.append(img)
"""

#Gameloop
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    draw_board(level)
    draw_player()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            player_x -= 3  # Adjust speed as needed
        if keys[pg.K_RIGHT]:
            player_x += 3
        if keys[pg.K_UP]:
            player_y -= 3
        if keys[pg.K_DOWN]:
            player_y += 3

    pg.display.flip()
pg.quit()



#Implementation of shortest route to Pacman (algorithms)