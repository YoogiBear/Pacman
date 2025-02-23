## Pacman
import pygame as pg
from board import boards
import math

## Window setup
pg.init()
WIDTH = 900
HEIGHT = 950
screen = pg.display.set_mode((WIDTH,HEIGHT))
timer = pg.time.Clock()
fps = 60
pg.display.set_caption("Pacman")
score_font = pg.font.Font('assets/fonts/BalAstaral-2Ox7o.ttf', 32)

## Game variables
level = boards #Used if there are more levels with different boards (maps)
color = 'blue' #Color of walls
flicker = False #Used to flicker the power up dots
valid_turns = [False, False, False, False] #right, left, up, down
temp = 0
direction = 0
PI = math.pi
player_x = 425
player_y = 661
counter = 0
power_counter = 0
player_speed = 2
score = 0
powerup = False
eaten_ghosts = [False, False, False, False]
start_count = 0 #Used to delay the start of the game
moving = False
hp = 3

##Load player and ghost images
player_images = []
for i in range(1,5):
    img = pg.image.load(f"assets/player_images/{i}.png")
    scaled = pg.transform.scale(img, (45,45))
    player_images.append(scaled)

blinky = pg.image.load("assets/ghost_images/red.png")
blinky_scaled = pg.transform.scale(blinky, (45,45))
blink_spawnx = (WIDTH//30)*15-25
blinky_spawny = (HEIGHT-50)//32*13-35
blinky_direction = 0
eaten_ghost = [False, False, False, False] #Blinky, Pinky, Inky, Clyde
ghost_speed = player_speed - 0.25
target = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)] #Will eventually be the box if they die.
blinky_dead = False
blinky_box = False #If Blinky is in the box
spooked = pg.image.load("assets/ghost_images/powerup.png")
spooked_img = pg.transform.scale(spooked, (45,45))
eyes = pg.image.load("assets/ghost_images/dead.png")
eyes_img = pg.transform.scale(eyes, (45,45))

class Ghost:
    def __init__(self, x, y, target, speed, img, direction, dead, box, id):
        self.x = x
        self.y = y
        self.center_x = self.x+22
        self.center_y = self.y+22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direction
        self.dead = dead #Used to determine if the ghost is dead
        self.box = box #Used to determine if the ghost is in the box
        self.id = id #Used to easily identify and change the ghosts' behavior
        self.turns, self.box = self.check_col()
        self.rect = self.draw()
    
    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead): #If you have already been eaten during a powerup and not in eye-state.
            screen.blit(self.img, (self.x, self.y))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x, self.y))
        else:
            screen.blit(eyes_img, (self.x, self.y))
        ghost_rect = pg.rect.Rect((self.center_x-18, self.center_y - 18), (36,36)) #Defining a hitbox rectangle around the ghost to detect collision
        return ghost_rect

    def check_col(self):
        num1 = ((HEIGHT-50)//32)
        num2 = (WIDTH//30)
        num3 = 15
        self.turns = [False, False, False, False] #right, left, up, down
        self.box = True
        if self.center_x // 30 < 29:
            if self.direction == 0:
                if level[self.center_y // num1][(self.center_x-num3) // num2] < 3: #Checks if 0, 1 or 2 is behind player when direction is right (empty, dot, power up)
                    self.turns[1] = True
            if self.direction == 1:
                if level[self.center_y // num1][(self.center_x+num3) // num2] < 3:
                    self.turns[0] = True
            if self.direction == 2:
                if level[(self.center_y+num3) // num1][self.center_x // num2] < 3:
                    self.turns[3] = True
            if self.direction == 3:
                if level[(self.center_y-num3)// num1][self.center_x // num2] < 3:
                    self.turns[2] = True

        #Check if it is possible to continue in the same direction and/or turn at any given position
            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18: #Determines if the center of the player is approx. in the middle of a tile
                    if level[(center_y+num3)// num1][center_x // num2] < 3: #Checks down
                        self.turns[3] = True
                    if level[(self.center_y-num3)// num1][self.center_x // num2] < 3: #Checks up
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x-num2) // num2] < 3: #Checks left side
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x+num2) // num2] < 3: #Checks right side
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y+num1) // num1][self.center_x // num2] < 3: #Checks down
                        self.turns[3] = True
                    if level[(self.center_y-num1) // num1][self.center_x // num2] < 3: #Checks up
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x+num3) // num2] < 3: #Checks right
                        self.turns[0] = True
                    if level[self.center_y // num1][(self.center_x-num3) // num2] < 3: #Checks left
                        self.turns[1] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        return self.turns, self.box
    

## Draw and logic functions
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
    turns = [False, False, False, False] #right, left, up, down
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
            if level[(center_y+num3) // num1][center_x // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(center_y-num3)// num1][center_x // num2] < 3:
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
                    turns[1] = True
                if level[center_y // num1][(center_x+num2) // num2] < 3: #Checks right side
                    turns[0] = True

        if direction == 0 or direction == 1:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y+num1) // num1][center_x // num2] < 3: #Checks down
                    turns[3] = True
                if level[(center_y-num1) // num1][center_x // num2] < 3: #Checks up
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x+num3) // num2] < 3: #Checks right
                    turns[0] = True
                if level[center_y // num1][(center_x-num3) // num2] < 3: #Checks left
                    turns[1] = True
    else:
        turns[0] = True
        turns[1] = True
    return turns

def move_player(player_x, player_y):
    if direction == 0 and valid_turns[0]:
        player_x += player_speed
    if direction == 1 and valid_turns[1]:
        player_x -= player_speed
    if direction == 2 and valid_turns[2]:
        player_y -= player_speed
    if direction == 3 and valid_turns[3]:
        player_y += player_speed
    return player_x, player_y

def check_point(score, powerup, power_counter, eaten_ghosts):
    num1 = (HEIGHT-50)//32
    num2 = (WIDTH//30)
    if 0 < player_x < 870: #If player is within the screen. Can't check a tile outside the screen.
        if level[center_y // num1][center_x // num2] == 1: #Normal dot
            level[center_y // num1][center_x // num2] = 0
            score += 10
        elif level[center_y // num1][center_x // num2] == 2: #Power up
            level[center_y // num1][center_x // num2] = 0
            score += 50
            powerup = True
            power_counter = 0 #Reset counter if you already had a powerup
            eaten_ghosts = [False, False, False, False] #The same ghost can't be eaten twice during the same powerup
    return score, powerup, power_counter, eaten_ghosts

## Gameloop
run = True

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
    if power_counter < 480 and powerup: #Powerup lasts for 8 seconds
        power_counter += 1
    elif power_counter >= 480 and powerup: #Reset when powerup is over
        print("Powerup over")
        powerup = False
        power_counter = 0
        eaten_ghosts = [False, False, False, False]
    if start_count < 180:
        start_count += 1
        moving = False
    elif start_count >= 180:
        moving = True


    screen.fill('black')
    draw_board(level)
    draw_player()
    blinky = Ghost(blink_spawnx, blinky_spawny, target[0], ghost_speed, blinky_scaled, blinky_direction, blinky_dead, blinky_box, 0)
    blinky.draw()
    center_x = int(player_x + 23)
    center_y = int(player_y + 23)
    valid_turns = check_pos(center_x, center_y) #Returns a list
    if moving:
        player_x, player_y = move_player(player_x, player_y)
    score, powerup, power_counter, eaten_ghost = check_point(score, powerup, power_counter, eaten_ghosts)


    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
            elif event.key == pg.K_RIGHT:
                temp = 0
            elif event.key == pg.K_LEFT:
                temp = 1
            elif event.key == pg.K_UP:
                temp = 2
            elif event.key == pg.K_DOWN:
                temp = 3
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT and temp == 0:
                temp = direction
            elif event.key == pg.K_LEFT and temp == 1:
                temp = direction
            elif event.key == pg.K_UP and temp == 2:
                temp = direction
            elif event.key == pg.K_DOWN and temp == 3:
                temp = direction

    if temp == 0 and valid_turns[0]:
        direction = 0
    if temp == 1 and valid_turns[1]:
        direction = 1
    if temp == 2 and valid_turns[2]:
        direction = 2
    if temp == 3 and valid_turns[3]:
        direction = 3
    
    #If player goes off screen, teleport to the other side.
    if player_x > WIDTH:
        player_x = -50
    elif player_x < -50:
        player_x = WIDTH
    score_text = score_font.render(f"Score: {score}", True, 'white')
    screen.blit(score_text, (10, 10))
    hp_text = score_font.render(f"HP: {hp}", True, 'white')
    screen.blit(hp_text, (10, 40))
        
    pg.display.flip()
pg.quit()