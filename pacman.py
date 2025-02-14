##Pacman
import pygame as pg
from board import boards
import math

## Window setup
pg.init()
WIDTH = 900
HEIGHT = 950
screen = pg.display.set_mode((WIDTH,HEIGHT))
timer = pg.time.Clock()
fps = 60 #Sets an fps limit
font = pg.font.Font('freesansbold.ttf',20)
pg.display.set_caption("Pacman")

## Game variables
level = boards #Used if there are more levels with different boards (maps)
color = 'blue' #Color of walls
flicker = False #Used to flicker the power up dots
valid_turns = [False, False, False, False] #(right, left, up, down)
temp = []
move_queue = []
direction = 0
PI = math.pi
player_x = 425
player_y = 660
counter = 0

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

def check_pos(center_x,center_y):
    turns = [False, False, False, False] #Left, right, up, down
    num1 = (HEIGHT-50)//32 #Determines the height of each tile if 32 are on the horizontal line
    num2 = (WIDTH//30) #Determines the width of each tile with 30 on the vertical line. // ensures integer is returned.
    num3 = 15 #used to check a little ahead instead of a whole tile which can cause Pacman to stop too early

    #Check if it is possible to turn around 180 degrees from current direction
    if center_x // 30 < 29:
        if direction == 0:
            if level[center_y // num1][(center_x-num3) // num2] < 3: #Checks if 0, 1 or 2 is behind player when direction is right (empty, dot, power up)
                turns[1] = True

        if direction == 1:
            if level[center_y // num1][(center_x+num3) // num2] < 3:
                turns[0] = True

        if direction == 2:
            if level[(center_y-num3) // num1][center_x // num2] < 3:
                turns[3] = True

        if direction == 3:
            if level[(center_y+num3)// num1][center_x // num2] < 3:
                turns[2] = True

    #Check if it is possible to continue in the same direction and/or turn at any given position
        if direction == 2 or direction == 3:
            if 12 <= center_x % num2 <= 18: #Determines if the center of the player is approx. in the middle of a tile
                if level[(center_y+num3)// num1][center_x // num2] < 3: #Checks down
                    turns[3] = True
                if level[(center_y-num3)// num1][center_x // num2] < 3: #Checks up
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x-num2) // num2] < 3: #Checks left side
                    turns[0] = True
                if level[center_y // num1][(center_x+num2) // num2] < 3: #Checks right side
                    turns[1] = True

        if direction == 0 or direction == 1:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y+num1) // num1][center_x // num2] < 3: #Checks down
                    turns[3] = True
                if level[(center_y-num1) // num1][center_x // num2] < 3: #Checks up
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x+num3) // num2] < 3: #Checks right
                    turns[1] = True
                if level[(center_y+num1) // num1][(center_x-num3) // num2] < 3: #Checks left
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True
    return turns

def move_player(player_x, player_y, direction):
    speed = 2
    if direction == 0 and valid_turns[0]:
        player_x += speed
    if direction == 1 and valid_turns[1]:
        player_x -= speed
    if direction == 2 and valid_turns[2]:
        player_y -= speed
    if direction == 3 and valid_turns[3]:
        player_y += speed

#Gameloop
run = True
num1 = ((HEIGHT-50)//32)
num2 = (WIDTH//30)
while run:
    timer.tick(fps)
    if counter < 19: #Can't exceed 19 since there are only 4 images (index 0-3). 20 would return index 4 which doesn't exist.
        counter += 1
        if counter > 15:
            pass
            flicker = False
    else:
        counter = 0
        flicker = True
    screen.fill('black')
    draw_board(level)
    draw_player()
    center_x = int(player_x + 22.5)
    center_y = int(player_y + 22.5)
    valid_turns = check_pos(center_x, center_y) #Returns a list
    print(valid_turns)
    #print(direction)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
            elif event.key == pg.K_RIGHT:
                temp.append('right')
            elif event.key == pg.K_LEFT:
                temp.append('left')
            elif event.key == pg.K_UP:
                temp.append('up')
            elif event.key == pg.K_DOWN:
                temp.append('down')

    if temp:
        intended_move = temp[0]
        direction_map = {'right':0, 'left':1, 'up':2, 'down':3}
        move_index = direction_map.get(intended_move)
        print(intended_move)

        if valid_turns[move_index]:
            move_queue.clear()
            direction = move_index
            move_queue.append(intended_move)
            temp.clear()
        else:
            temp.clear() #Move-queueing-function not made yet. This is a placeholder.

    player_x, player_y = move_player(player_x, player_y, direction)

    """    
    if player_x > WIDTH and (HEIGHT//2-50) <= player_y <= (HEIGHT//2+50): #If player goes off screen, teleport to the other side.
        player_x = -50
    elif player_x < -50 and (HEIGHT//2-50) <= player_y <= (HEIGHT//2+50):
        player_x = WIDTH
    """
    pg.display.flip()
pg.quit()