import pygame
import time
import curses

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

scoreFont = pygame.font.SysFont('./font/Cousine-Regular.ttf', 500)
teamFont = pygame.font.SysFont('./font/Cousine-Regular.ttf', 120)
upcomingFont = pygame.font.SysFont('./font/Cousine-Regular.ttf', 50)
timeFont = pygame.font.SysFont('./font/Cousine-Regular.ttf', 400)

X = 1920
Y = 1080

games = [('Legyen Sánc!', 'Gucci Gang'),
         ('Next', 'Putty, ezt is lecsaptuk'),
         ('Csáki lehozza', 'Nutellák')
         ]

screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('ponttábla')


carryOn = True
timer = False
t = 585  # seconds
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


c = time.time()
# -------- Main Program Loop -----------
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not event.mod & pygame.KMOD_SHIFT:
                l += 1
            elif event.key == pygame.K_RIGHT:
                l += -1
            elif event.key == pygame.K_LEFT and not event.mod & pygame.KMOD_SHIFT:
                r += 1
            elif event.key == pygame.K_LEFT:
                r += -1
            elif event.key == pygame.K_SPACE:
                timer = not timer
            elif event.key == pygame.K_r and event.mod & pygame.KMOD_SHIFT:
                t = 0
            elif event.key == pygame.K_UP and not event.mod & pygame.KMOD_SHIFT:
                t += 1
            elif event.key == pygame.K_UP:
                t += 60
            elif event.key == pygame.K_DOWN and not event.mod & pygame.KMOD_SHIFT:
                t += -1
            elif event.key == pygame.K_DOWN:
                t += -60
            elif event.key == pygame.K_RETURN and event.mod & pygame.KMOD_CTRL:
                next_round()

    try:
        k = scrn.getkey()
    except:
        k = ''

    if k != '':
        if k == 'Q':
            break
        elif k == ' ':
            timer = not timer
        elif k == 'R':
            t = 0
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
        
    if timer:
        ct = time.time()
        t += (ct - c)
        c = ct
    else:
        c = time.time()
        ct = c

    if t >= 600:
        timer = False

    # ----- pygame write -----
    cl = timeFormat(t)
    team_l = teamFont.render(games[0][0], 1, WHITE)
    team_r = teamFont.render(games[0][1], 1, WHITE)
    next_l = upcomingFont.render(games[1][0], 1, WHITE)
    next_r = upcomingFont.render(games[1][1], 1, WHITE)
    score_l = scoreFont.render(format(l), 1, WHITE)
    score_r = scoreFont.render(format(r), 1, WHITE)
    dot = scoreFont.render(':', 1, WHITE)

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

    screen.blit(team_l, (X / 2 - team_l.get_width() - 100, 70))
    screen.blit(team_r, (X / 2 + 100, 70))
    
    screen.blit(score_l, (X / 2 - score_l.get_width() - 150, 200))
    screen.blit(score_r, (X / 2 + 150, 200))
    screen.blit(dot, (X / 2 - dot.get_width() / 2, 180))
    
    screen.blit(minutes, (X / 2 - minutes.get_width() - 40, 500))
    screen.blit(seconds, (X / 2 + 50, 500))
    screen.blit(dot2, (X / 2 - dot2.get_width() / 2, 500))

    # upcoming matches
    uy = 500
    for i in range(len(games)):
        if i > 3:
            break
        elif i != 0:
            left = upcomingFont.render(games[i][0], 1, WHITE)
            right = upcomingFont.render(games[i][1], 1, WHITE)
            screen.blit(left, (X / 2 - left.get_width() - 500, uy + i * 70))
            screen.blit(right, (X / 2 + 500, uy + i * 70))

    # ----- curses write -----
    score_txt = str(r) + ' : ' + str(l)
    time_txt = str(cl[0]) + ':' + str(cl[1])
    scrn.addstr(4, 4, score_txt)
    scrn.addstr(5, 4, time_txt)
    # scrn.addstr(6, 4, k)
    scrn.addstr(4, 12, games[0][0] + ' : ' + games[0][1])
    
    # Refresh screens
    scrn.refresh()
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
curses.echo()
curses.nocbreak()
scrn.keypad(False)

curses.endwin()
