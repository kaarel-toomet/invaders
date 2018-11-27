#!/usr/bin/python3
import pygame as pg
import random as r
import sys
import subprocess

pg.init()
pic = pg.image.load("kausyarcher.png")
arw = pg.image.load("arrow.png")
ufo1 = pg.image.load("invader1.png")
ufo2 = pg.image.load("invader2.png")
ufo3 = pg.image.load("invader3.png")
ufo4 = pg.image.load("invader4.png")
ray = pg.image.load("ray.png")

## figure out the screen size
## The standard get_size() gives wrong results on multi-monitor setup
## use xrandr instead (only on linux)
xdotool = False
# did we get the data through xdotool?
if sys.platform == 'linux':
    res = subprocess.run("./activescreen", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if(res.returncode == 0):
        # success
        wh = res.stdout.split(b' ')
        screenw = int(wh[0])
        screenh = int(wh[1])
        screen = pg.display.set_mode((screenw, screenh), pg.RESIZABLE)
        xdotool = True
if not xdotool:
    screen = pg.display.set_mode((0,0), pg.RESIZABLE)
    screenw, screenh = pg.display.get_surface().get_size()
pg.display.set_caption("Space Invaders")

points = 0
u1tick = 0
u1max = 300
u2tick = 0
u2max = 600
u3tick = 0
u3max = 900
u4tick = 0
u4max = 1200
predo = True
do = True
hor_speed = screenw/250
# player horizontal speed if left/right arrow pressed
left = True
right = True
mleft = False
mright = False
timer = pg.time.Clock()
health = 1000
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
mfont = pg.font.SysFont("Times",50)
wfont = pg.font.SysFont("Times",100)
pause = False
gameover = False
gf = False
res = 10
arrows = pg.sprite.Group()
ufos1 = pg.sprite.Group()
ufos2 = pg.sprite.Group()
ufos3 = pg.sprite.Group()
ufos4 = pg.sprite.Group()
rays = pg.sprite.Group()
atick = 0
amax = 60
ammo = 0
hexp = 0
mode = 0
won = False
per = 255
peg = 0
peb = 255
options = "press I for infinite mode. Press F for finite mode"
cats = 0
level = 1
class Player(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self, mleft, mright):
        if self.rect.x <= 0:
            left = False
        else:
            left = True
        if self.rect.x >= screenw-128:
            right = False
        else:
            right = True
        if mleft and left:
            self.rect.x -= hor_speed
        if mright and right:
            self.rect.x += hor_speed
        self.rect.y = screenh-96
    def getx(self):
        return self.rect.x
class Proj(pg.sprite.Sprite):
    def __init__(self, x, y, vel, img):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.x = float(x)
        self.y = float(y)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.vel = vel
    def update(self):
        if self.y + self.vel <= screenh+64 and self.rect.y + self.vel >= -64:
            self.y += self.vel
            self.rect.y = int(self.y)
uselessvariable = 0
uselessfont = pg.font.SysFont("Times", uselessvariable)
class UFO(pg.sprite.Sprite):
    def __init__(self, x, y, vel, img, shootdelay, bpic, bspd, piw, hp, lvl):
        self.direction = r.randint(0,1)
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.x = float(x)
        self.y = float(y)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if self.direction == 0:
            self.vel = vel
        else:
            self.vel = -vel
        self.bullet = bpic
        self.bulletvel = bspd
        self.maxtick = shootdelay
        self.tick = r.randint(0,self.maxtick)
        self.piw = piw
        self.hp = hp
        self.lvl = lvl
    def update(self, harm = False):
        global points, health, res, hexp, ammo, level
        self.tick += 1
        if self.tick >= self.maxtick:
            self.tick = 0
            rays.add(Proj(self.x+((self.piw/2)-16),self.y+4,screenh/40,ray))
        if self.x + self.vel <= screenw-96 and self.x + self.vel >= 0:
            self.x += self.vel*level
            self.rect.x = int(self.x)
        else:
            self.vel = -self.vel
        if harm:
            self.hp -=1
        if self.hp <= 0:
            ufos1.remove(self)
            ufos2.remove(self)
            ufos3.remove(self)
            ufos4.remove(self)
            if self.lvl == 1:
                points += 1
            elif self.lvl == 2:
                points += 2
                health += 100 + hexp
            elif self.lvl == 3:
                points += 3
                res += 1
            elif self.lvl == 4:
                points += 4
                ammo += 50
                hexp += 10
def reset():
    global health, player, arrows, ufos1, kausy, ufos2, ufos3, res, ammo, points
    health = 1000
    player.empty()
    arrows.empty()
    ufos1.empty()
    ufos2.empty()
    ufos3.empty()
    ufos4.empty()
    ammo = 0
    kausy = Player(screenw/2,screenh-96)
    player = pg.sprite.GroupSingle(kausy)
    res = 10
    points = 0
kausy = Player(screenw/2,screenh-96)
player = pg.sprite.GroupSingle(kausy)
while predo:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            predo = False
            do = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_i:
                mode = 0
                predo = False
            if event.key == pg.K_f:
                mode = 1
                predo  = False
            if event.key == pg.K_RSHIFT:
                #per = 255-per
                peg = 128-peg
                peb = 255-peb
                options += "hi"
                if cats == 0:
                    options = "pres i 4 infnit moed pres f 4 finit mod"
                cats += 1
    screen.fill((128,128,128))
    mtext = mfont.render(options, True, (per,peg,peb))
    mtext_rect = mtext.get_rect()
    mtext_rect.centerx = screenw/2
    mtext_rect.y = screenh/2
    screen.blit(mtext,mtext_rect)
    pg.display.update()
pfont = pg.font.SysFont("Times", 50+cats)
while do:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            do = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                mleft = True
            elif event.key == pg.K_RIGHT:
                mright = True
            elif event.key == pg.K_p:
                pause = True
            elif event.key == pg.K_r:
                reset()
            elif event.key == pg.K_UP:
                gf = True
            elif event.key == pg.K_SPACE:
                if ammo > 0:
                    ammo -= 1
                    arrows.add(Proj(kausy.getx()+28, screenh-96,-screenh/60,arw))
            elif event.key == pg.K_F7:
                uselessvariable += 30
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                mleft = False
            elif event.key == pg.K_RIGHT:
                mright = False
            elif event.key == pg.K_UP:
                gf = False
        elif event.type == pg.VIDEORESIZE:
            screenw = event.w
            screenh = event.h
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pause = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause = False
        pd = "PAUSED"
        ptext = pfont.render(pd, True, (0,0,0))
        ptext_rect = ptext.get_rect()
        ptext_rect.centerx = screen.get_rect().centerx
        ptext_rect.y = 50+cats
        screen.blit(ptext,ptext_rect)
        screen.blit(text,text_rect)
        pg.display.update()
    if health <= 0:
        uded = "GAME OVER"
        dtext = dfont.render(uded, True, (255,0,0))
        dtext_rect = dtext.get_rect()
        dtext_rect.centerx = screen.get_rect().centerx
        dtext_rect.y = 30
        screen.blit(dtext,dtext_rect)
        screen.blit(text,text_rect)
        pg.display.update()
        gameover = True
    while gameover:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameover = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    gameover = False
                    reset()
    if mode == 1 and points >= 250:
        won = True
    while won:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                won = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    won = False
                    reset()
        uwon = "YOU WON!"
        wtext = wfont.render(uwon, True, (0,255,0))
        wtext_rect = wtext.get_rect()
        wtext_rect.centerx = screen.get_rect().centerx
        wtext_rect.y = screenh/2
        screen.blit(wtext,wtext_rect)
        screen.blit(text,text_rect)
        pg.display.update()
    col1 = pg.sprite.groupcollide(arrows, ufos1, True, False)
    if len(col1.values()) > 0:
        for ufo in col1.values():
            ufo[0].update(True)
    col2 = pg.sprite.groupcollide(arrows, ufos2, True, False)
    if len(col2.values()) > 0:
        for ufo in col2.values():
            ufo[0].update(True)
    col3 = pg.sprite.groupcollide(arrows, ufos3, True, False)
    if len(col3.values()) > 0:
        for ufo in col3.values():
            ufo[0].update(True)
    col4 = pg.sprite.groupcollide(arrows, ufos4, True, False)
    if len(col4.values()) > 0:
        for ufo in col4.values():
            ufo[0].update(True)
    rcol = pg.sprite.spritecollide(kausy, rays,True)
    if len(rcol) > 0:
        health -= (1000/res)
    uselesswords = "i like potatoes"
    screen.fill((128,128,128))
    score = ("Health: " + str(round(health)) + " Score: " + str(points) +
             " Resistance: " + str(res) + " Arrows: " + str(ammo)+
             " Extra Health Gain: " + str(hexp) + " Level: " + str(level))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screenw/2
    text_rect.y = 10
    screen.blit(text,text_rect)
    player.update(mleft, mright)
    player.draw(screen)
    arrows.update()
    arrows.draw(screen)
    rays.update()
    rays.draw(screen)
    ufos1.update()
    ufos1.draw(screen)
    ufos2.update()
    ufos2.draw(screen)
    ufos3.update()
    ufos3.draw(screen)
    ufos4.update()
    ufos4.draw(screen)
    uselessfont = pg.font.SysFont("Times", uselessvariable)
    uselesstext = uselessfont.render(uselesswords, True, (0,0,255))
    uselesstext_rect = uselesstext.get_rect()
    uselesstext_rect.centerx = screenw/2
    uselesstext_rect.y = 30
    screen.blit(uselesstext,uselesstext_rect)
    pg.display.update()
    u1tick += 1
    level = int(points/3)
    if u1tick >= u1max:
        u1tick = 0
        ufos1.add(UFO(r.randint(0,screenw-96),r.randint(0, 256), 1, ufo1,
                      60, ray, 16, 64, 1, 1))
        u1max = r.randint(0,600)
    u2tick += 1
    if u2tick >= u2max:
        u2tick = 0
        ufos2.add(UFO(r.randint(0,screenw-96),r.randint(0, 256), 2, ufo2,
                      30, ray, 16, 48, 2, 2))
        u2max = r.randint(0,1200)
    u3tick += 1
    if u3tick >= u3max:
        u3tick = 0
        ufos3.add(UFO(r.randint(0,screenw-96),r.randint(0, 256), 1, ufo3,
                      20, ray, 16, 64, 3, 3))
        u3max = r.randint(0,1800)
    u4tick += 1
    if u4tick >= u4max:
        u4tick = 0
        ufos4.add(UFO(r.randint(0,screenw-96),r.randint(0, 256), 4, ufo4,
                      10, ray, 16, 128, 3, 4))
        u4max = r.randint(0,2400)
    atick += 1
    if atick >= amax:
        atick = 0
        ammo += 1
    if uselessvariable > 0:
        uselessvariable -= 1
    if not gf:
        timer.tick(60)

pg.quit()
