from collections import deque
from blessings import Terminal
from functools import partial
import time, random, socket
import keyboard
import threading

s = socket.socket()    
host = socket.gethostname()
port = 3000
try:
    s.connect((host, port))
except:
    pass

def debug(message):
    global s
    s.send(message.encode('utf-8'))

print = partial(print, end="", flush=True)

t = Terminal()

x_shift = 10
y_shift = 10
score = 0
bait_pos = None

snake_cords = deque()
snake_cords.extend([
    (x_shift+7, t.height - y_shift + 4),
    (x_shift+8, t.height - y_shift + 4),
    (x_shift+9, t.height - y_shift + 4),
    (x_shift+10, t.height - y_shift + 4)
    ])
l = snake_cords.pop()
snake_set = set(snake_cords)
snake_cords.append(l)

heading = 'E' #E W N S

def draw_boundary():
    with t.location(x_shift, t.height - y_shift):
        print('╔' + '═'*16 + '╗')
    with t.location(x_shift, t.height):
        print('╚' + '═'*16 + '╝')
    for i in range(9,1,-1):
        with t.location(x_shift, t.height-i):
            print('║')
        with t.location(x_shift+17, t.height-i):
            print('║')

def print_score():
    s = f'▒ score: {score} ▒'
    with t.location(x_shift + (9 - len(s)//2), t.height-y_shift-2):
            print(t.black_on_yellow(s))

def get_next_cords(x,y):
    if(heading == 'E'):
        return (x+1, y)
    elif(heading == 'W'):
        return (x-1, y)
    elif(heading == 'N'):
        return (x, y-1)
    else:
        return (x, y+1)

def move_and_draw_snake():
    global snake_set, bait_pos, score
    if(snake_cords[-1] == bait_pos):
        snake_cords.append(bait_pos)
        bait_pos = None
        score += 100
    for x,y in snake_cords:
        with t.location(x,y):
            print('●')
    next_cor = get_next_cords(*snake_cords[-1])
    snake_cords.append(next_cor)
    snake_cords.popleft()
    l = snake_cords.pop()
    snake_set = set(snake_cords)
    snake_cords.append(l)

def clear_screen():
    print(t.clear_eos, end="", flush=True)

def check_for_collision(cord, snake_himself = True):
    #debug(str(cord) + "||" + str(snake_set.difference({cord,})))
    x,y = cord
    if(snake_himself and (cord in snake_set)):
        return True
    elif(not snake_himself and (cord in snake_set)):
        return True
    if(not ((x>x_shift and x<x_shift+17) and (y>t.height-y_shift and y<t.height-1))):
        return True
    return False

def randim_bait_pos():
    x_rand = random.randint(x_shift+1, x_shift+15)
    y_rand = random.randint(t.height-y_shift + 1 , t.height - 1)
    while(check_for_collision((x_rand, y_rand), False)):
        x_rand = random.randint(x_shift+1, x_shift+16)
        y_rand = random.randint(t.height-y_shift + 1 , t.height - 1)
    return (x_rand, y_rand)

def main_loop():
    global bait_pos
    while(1):
        if(check_for_collision(snake_cords[-1])):
            print(t.blink)
            for x,y in snake_cords:
                with t.location(x,y):
                    print('●')
            print(t.normal)
            break

        clear_screen()
        draw_boundary()
        print_score()
        move_and_draw_snake()

        if(not bait_pos):
            bait_pos = randim_bait_pos()

        with t.location(*bait_pos):
            print('◌')

        with t.location():
            print()
        time.sleep(0.3)

def handle_user_control():
    global heading
    while(1):
        if(keyboard.is_pressed('up') and (heading != 'N' and heading != 'S')):
            heading = 'N'
        elif(keyboard.is_pressed('down') and (heading != 'N' and heading != 'S')):
            heading = 'S'
        elif(keyboard.is_pressed('left') and (heading != 'E' and heading != 'W')):
            heading = 'W'
        elif(keyboard.is_pressed('right') and (heading != 'E' and heading != 'W')):
            heading = 'E'
        time.sleep(0.005)

threading.Thread(target=main_loop).start()
threading.Thread(target=handle_user_control).start()