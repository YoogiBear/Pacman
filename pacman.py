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
colors =  ['red', 'blue', 'green', 'yellow','orange','purple','pink','white']
color = 'blue' #Color of walls
flicker = False #Used to flicker the power up dots
valid_turns = [False, False, False, False] #Used to determine if a turn is valid (right, left, up, down)

def draw_board(level):
    num1 = ((HEIGHT-50)//32) #Determines the height of each tile if 32 are on the horizontal line
    num2 = (WIDTH//30) #Determines the width of each tile with 30 on the vertical line. // ensures integer is returned.
    for i in range(len(level)): #For each map that is assigned to a level and defines the vertical placement number
        for j in range(len(level[i])): #For each tile on map[i] and defines the horizontal placement number
            if level[i][j] == 1: #Normal dot
                pg.draw.circle(screen, 'white',(j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)),4) #Finds the center of the tile
            if level[i][j] == 2 and not flicker: #Bigger dot (Power up)
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
player_y = 660
direction = 0
counter = 0

def draw_player():
    #Right = 0, Left = 1, Up = 2, Down = 3
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pg.transform.flip(player_images[counter // 5], True, False),(player_x, player_y)) #True and False determines whether or not to flip on x,y axis.
    elif direction == 2:
        screen.blit(pg.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pg.transform.rotate(player_images[counter // 5], -90), (player_x, player_y))

"""
def check_pos(x,y):
    turns = [False, False, False, False] #Left, right, up, down
    num1 = ((HEIGHT-50)//32) #Determines the height of each tile if 32 are on the horizontal line
    num2 = (WIDTH//30) #Determines the width of each tile with 30 on the vertical line. // ensures integer is returned.
    num3 = 15 
    #Check collisions behind center of player (x,y) and the buffer of 15 pixels to compensate for the player's size and the empty space between walls and the tile's edge
    if center_x // 30 < 29:
        if direction == 0:
            if level[center_y // num1][center_x-num3 // num2] < 3: #Checks if 0, 1 or 2 is behind player when direction is right (empty, dot, power up)
                turns[1] = True
        if direction == 1:
             if level[center_y // num1][center_x+num3 // num2] < 3:
                turns[0] = True

        if direction == 2:
            if level[center_y-num3 // num1][center_x // num2] < 3:
                turns[3] = True

        if direction == 3:
            if level[center_y+num3// num1][center_x // num2] < 3:
                turns[2] = True

    else:
        turns[0] = True
        turns[1] = True
    return turns
"""

ghosts = []
def draw_ghosts():
    for i in range(1,4):
        img = pg.image.load(f"assets/ghost_images/{i}.png")
        ghosts.append(img)

move_queue = ['start']
#If keypress in direction x is possible, clear the queue and append the move to the queue. While the queue is not empty, move the player in the direction of the queue.
#If the direction is not possible, append the move to the queue and wait until the player can move in that direction.

#Gameloop
run = True
num1 = ((HEIGHT-50)//32)
num2 = (WIDTH//30)
while run:
    timer.tick(fps)
    if counter < 19: #Can't exceed 19 since there are only 4 images (index 0-3). 20 would return index 4 which doesn't exist.
        counter += 1
        if counter > 15:
            flicker = False
    else:
        counter = 0
        flicker = True
    screen.fill('black')
    draw_board(level)
    draw_player()
    center_x = int(player_x + 22.5)
    center_y = int(player_y + 22.5)
    #valid_turns = check_pos(center_x, center_y)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
            elif event.key == pg.K_RIGHT:
                #if valid_turns[0]:
                move_queue.append('right')
                move_queue.pop(0)
                #else move_queue.append('right')
            elif event.key == pg.K_LEFT:
                move_queue.append('left')
                move_queue.pop(0)
            elif event.key == pg.K_UP:
                move_queue.append('up')
                move_queue.pop(0)
            elif event.key == pg.K_DOWN:
                move_queue.append('down')
                move_queue.pop(0)

    if move_queue[0] == 'start':
        pass
    elif move_queue[0] == 'right': #and is not blocked by wall: #(god pseudokode)
        player_x += 1.5
        direction = 0
    elif move_queue[0] == 'left': #and is not blocked by wall:
        player_x -= 1.5
        direction = 1
    elif move_queue[0] == 'up': #and is not blocked by wall:
        player_y -= 1.5
        direction = 2
    elif move_queue[0] == 'down': #and is not blocked by wall:
        player_y += 1.5
        direction = 3
    
        
    pg.display.flip()
pg.quit()