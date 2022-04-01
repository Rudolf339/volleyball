import pygame
import time
import curses
import data
import json
import random

DEBUG = True
QUICK = False
carryOn = True

try:
    with open('progress_dump.json', 'r') as json_file:
        json_str = json_file.read()
        dumpfile = json.loads(json_str)
        print('Dumpfile found.')
        while True:
            ans = input('Do you want to load it? y/n (y):')
            if ans.lower().startswith('y') or ans == '':
                db = dumpfile
                break
            elif ans.lower().startswith('n'):
                db = data.data
                db['current_round'] = 0
                break
            else:
                print('Invalid answer')

except IOError:
    db = data.data
    db['current_round'] = 0

if DEBUG:
    print('teams')
    for a in db['teams']:
        print('\t', a, db['teams'][a])
    print('groups')
    for a in db['groups']:
        print('\t', a, db['groups'][a])
    print('matches')
    for a in db['matches']:
        print('\t', a)
    print('GM:', db['GM'])
    if input() == 'q':
        carryOn = False

scrn = curses.initscr()

curses.noecho()
curses.cbreak()
scrn.keypad(True)
scrn.nodelay(True)

pygame.init()

l = 0
r = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

scoreFont = pygame.font.SysFont('./font/Cousine-Regular.ttf', 300)
teamFont = pygame.font.SysFont('./font/Cousine-Regular.ttf', 60)
upcomingFont = pygame.font.SysFont('./font/Cousine-Regular.ttf', 30)
timeFont = pygame.font.SysFont('./font/Cousine-Regular.ttf', 250)

X = 1024
Y = 768

games = []
for g in range(db['current_round'], len(db['matches'])):
    games.append((db['matches'][g]['l'], db['matches'][g]['r'],
                 db['matches'][g]['t'], db['matches'][g]['st']))

screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('ponttábla')

timer = False
t = 0  # seconds
clock = pygame.time.Clock()
# -------- DEFINITIONS --------


def format(n):
    n = str(n)
    if len(n) == 1:
        n = '0' + n
    return n


def timeFormat(t):
    t = int(t)
    minutes = str(t // 60)
    sec = str(t % 60)
    if len(minutes) < 2:
        minutes = "0" + minutes
    if len(sec) < 2:
        sec = "0" + sec
    return (minutes, sec)


def next_round():
    games.remove(games[0])

nxt = False
cmd = ''
cmd_mode = False
out = ''
c = time.time()
# -------- Main Program Loop -----------
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
            
    try:
        k = scrn.getkey()
    except curses.error:
        k = ''

    if cmd_mode:
        if k == 'KEY_DC':
            cmd_mode = False
        elif k == 'KEY_BACKSPACE':
            cmd = cmd[:-1]
            scrn.clear()
        else:
            cmd += k
    
    elif k != '':
        if k == 's':
            QUICK = False
        if k == 'Q':
            break
        elif k == ' ':
            timer = not timer
        elif k == 'r':
            scrn.clear()
        elif k == 'R':
            t = 0
        elif k == 'N':
            nxt = True
        elif k == 'KEY_LEFT':
            r += 1
        elif k == 'KEY_SLEFT':
            r += -1
        elif k == 'KEY_RIGHT':
            l += 1
        elif k == 'KEY_SRIGHT':
            l += -1
        elif k == 'KEY_UP':
            t += 1
        elif k == 'KEY_SF':
            t += 60
        elif k == 'KEY_DOWN':
            t += -1
        elif k == 'KEY_SR':
            t += -60
        elif k == 'KEY_HOME':
            cmd_mode = True
    if timer:
        ct = time.time()
        t += (ct - c)
        c = ct
    else:
        c = time.time()
        ct = c

    if t >= 600:
        timer = False

    # ----- command execution -----
    if not cmd_mode:
        if cmd == ('ls teams'):
            out = ''
            for te in db['teams']:
                out += te + ' ' + str(db['teams'][te]) + '\n'
        elif cmd == ('ls groups'):
            out = ''
            for gr in db['groups']:
                out += gr + ' ' + str(db['groups'][gr]) + '\n'
        elif cmd.startswith('K_D '):
            if cmd[4:] in db['teams'].keys():
                for m in range(db['current_round'], len(db['matches'])):
                    if db['matches'][m]['r'] == 'K_D':
                        db['matches'][m]['r'] = cmd[4:]
                        out = 'Done.'
                    elif db['matches'][m]['l'] == 'K_D':
                        db['matches'][m]['l'] = cmd[4:]
                        out = 'Done.'
                
                with open('progress_dump.json', 'w') as dumpfile:
                    json.dump(db, dumpfile)
            else:
                out = 'FAILED: no team of the given name'
        else:
            out = 'unkown command'
    
    # ----- pygame write -----
    
    cl = timeFormat(t)
    try:
        team_l = teamFont.render(games[0][0], 1, WHITE)
        team_r = teamFont.render(games[0][1], 1, WHITE)
    except IndexError:
        break
    try:
        next_l = upcomingFont.render(games[1][0], 1, WHITE)
        next_r = upcomingFont.render(games[1][1], 1, WHITE)
    except IndexError:
        next_l = upcomingFont.render('', 1, WHITE)
        next_r = upcomingFont.render('', 1, WHITE)
        
    score_l = scoreFont.render(format(l), 1, WHITE)
    score_r = scoreFont.render(format(r), 1, WHITE)
    dot = scoreFont.render(':', 1, WHITE)
    mtype = teamFont.render(games[0][2], 1, WHITE)

    # timer
    if t < 590 or int(t) % 2 == 1:
        minutes = timeFont.render(cl[0], 1, WHITE)
        seconds = timeFont.render(cl[1], 1, WHITE)
        dot2 = timeFont.render(':', 1, WHITE)
    else:
        minutes = timeFont.render(cl[0], 1, RED)
        seconds = timeFont.render(cl[1], 1, RED)
        dot2 = timeFont.render(':', 1, RED)
    
    screen.fill(BLACK)

    screen.blit(team_l, (X / 2 - team_l.get_width() - 60, 40))
    screen.blit(team_r, (X / 2 + 60, 40))
    
    screen.blit(score_l, (X / 2 - score_l.get_width() - 80, 150))
    screen.blit(score_r, (X / 2 + 80, 150))
    screen.blit(dot, (X / 2 - dot.get_width() / 2, 150))
    
    screen.blit(minutes, (X / 2 - minutes.get_width() - 40, 350))
    screen.blit(seconds, (X / 2 + 50, 350))
    screen.blit(dot2, (X / 2 - dot2.get_width() / 2, 350))

    screen.blit(mtype, (X/2 - mtype.get_width() / 2, 530))
    
    # upcoming matches
    uy = 500
    for i in range(len(games)):
        if i > 3:
            break
        elif i != 0:
            if games[i][0].startswith('#'):
                left = upcomingFont.render('?????', 1, WHITE)
            else:
                left = upcomingFont.render(games[i][0], 1, WHITE)
            if games[i][1].startswith('#'):
                right = upcomingFont.render('?????', 1, WHITE)
            else:
                right = upcomingFont.render(games[i][1], 1, WHITE)
            screen.blit(left, (X / 2 - left.get_width() - 200, uy + i * 70))
            screen.blit(right, (X / 2 + 200, uy + i * 70))

    if db['current_round'] > 60:
        QUICK = False
    if db['current_round'] < db['GM'] and QUICK:
        if random.random() > 0.5:
            l = 1
        else:
            r = 1
        nxt = True
        t = 601
        
    if (t >= 600 and l != r) and nxt:  # There's a winner
        if l > r and games[0][2] != 'tanári':
            db['teams'][games[0][0]]['wins'] += 1
            db['matches'][db['current_round']]['w'] = games[0][0]
            db['matches'][db['current_round']]['loser'] = games[0][1]
            db['teams'][games[0][0]]['points'] += l
            db['teams'][games[0][1]]['points'] += r
        elif l < r and games[0][2] != 'tanári':
            db['teams'][games[0][1]]['wins'] += 1
            db['matches'][db['current_round']]['w'] = games[0][1]
            db['matches'][db['current_round']]['loser'] = games[0][0]
            db['teams'][games[0][0]]['points'] += l
            db['teams'][games[0][1]]['points'] += r
        t = 0
        l = 0
        r = 0
        timer = False
        db['current_round'] += 1
        next_round()
        scrn.clear()
        data.export(db)
        with open('progress_dump.json', 'w') as dumpfile:
            json.dump(db, dumpfile)
            
    if db['current_round'] >= db['GM']:
        db = data.order(db)
        games = []
        for g in range(db['current_round'], len(db['matches'])):
            games.append((db['matches'][g]['l'], db['matches'][g]['r'],
                          db['matches'][g]['t'], db['matches'][g]['st']))

    # ----- curses write -----
    score_txt = str(r) + ' : ' + str(l) + '  '
    time_txt = str(cl[0]) + ':' + str(cl[1])
    scrn.addstr(4, 4, score_txt)
    scrn.addstr(5, 4, time_txt)
    scrn.addstr(7, 4, db['matches'][db['current_round']]['st'])
    try:
        scrn.addstr(4, 12, games[0][1] + ' : ' + games[0][0] + ' ' * 5)
    except IndexError:
        pass
    try:
        scrn.addstr(6, 12, games[1][1] + ' : ' + games[1][0] + ' ' * 5)
    except IndexError:
        pass
    try:
        scrn.addstr(7, 12, games[2][1] + ' : ' + games[2][0] + ' ' * 5)
    except IndexError:
        pass
    try:
        scrn.addstr(8, 12, games[3][1] + ' : ' + games[3][0] + ' ' * 5)
    except IndexError:
        pass
    try:
        scrn.addstr(5, 12, games[0][2] + ' ' * 5)
        scrn.addstr(9, 4, str(db['current_round']) + ' ' + str(db['GM']))
    except IndexError:
        pass
    if cmd_mode:
        scrn.addstr(10, 4, str(cmd))
    scrn.addstr(10, 4, out)
    nxt = False
    # Refresh screens
    scrn.refresh()
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
curses.echo()
curses.nocbreak()
scrn.keypad(False)

curses.endwin()
