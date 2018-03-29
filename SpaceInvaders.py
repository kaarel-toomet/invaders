#!/usr/bin/python3
import pygame as pg
import random as r
pg.init()
pic = pg.image.load("kausyarcher.png")
arw = pg.image.load("arrow.png")
ufo1 = pg.image.load("invader1.png")
ufo2 = pg.image.load("invader2.png")
ray = pg.image.load("ray.png")
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw, screenh = pg.display.get_surface().get_size()
pg.display.set_caption("Space Invaders")
points = 0
u1tick = 0
u1max = 300
u2tick = 0
u2max = 1200
do = True
spd = 6
left = True
right = True
mleft = False
mright = False
timer = pg.time.Clock()
lifes = 1000
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
gameover = False
gf = False
arrows = pg.sprite.Group()
ufos1 = pg.sprite.Group()
ufos2 = pg.sprite.Group()
rays = pg.sprite.Group()
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
            self.rect.x -= spd
        if mright and right:
            self.rect.x += spd
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
        if self.y + self.vel <= screenh and self.rect.y + self.vel >= -64:
            self.y += self.vel
            self.rect.y = int(self.y)
uselessvariable = 0
uselessfont = pg.font.SysFont("Times", uselessvariable)
class UFO(pg.sprite.Sprite):
    def __init__(self, x, y, vel, img, shootdelay, bpic, bspd, hp, val):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.x = float(x)
        self.y = float(y)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.vel = vel
        self.bullet = bpic
        self.bulletvel = bspd
        self.maxtick = shootdelay
        self.tick = r.randint(0,self.maxtick)
        self.health = hp
        self.value = val
        self.wek = False
    def update(self, col):
        global points
        self.tick += 1
        if self.tick >= self.maxtick:
            self.tick = 0
            rays.add(Proj(self.x+8,self.y+4,16,ray))
        if self.x + self.vel <= screenw-96 and self.x + self.vel >= 0:
            self.x += self.vel
            self.rect.x = int(self.x)
        else:
            self.vel = -self.vel
def reset():
    global lifes, player, arrows, ufos1, kausy
    lifes = 10
    player.empty()
    arrows.empty()
    ufos1.empty
    kausy = Player(screenw/2,screenh-96)
    player = pg.sprite.GroupSingle(kausy)
kausy = Player(screenw/2,screenh-96)
player = pg.sprite.GroupSingle(kausy)
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
                arrows.add(Proj(kausy.getx()+28, screenh-96,-10,arw))
            elif event.key == pg.K_F7:
                uselessvariable += 30
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                mleft = False
            elif event.key == pg.K_RIGHT:
                mright = False
            elif event.key == pg.K_UP:
                gf = False
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pause = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause = False
        pd = "PAUSED"
        ptext = dfont.render(pd, True, (0,0,0))
        ptext_rect = ptext.get_rect()
        ptext_rect.centerx = screen.get_rect().centerx
        ptext_rect.y = 50
        screen.blit(ptext,ptext_rect)
        screen.blit(text,text_rect)
        pg.display.update()
    if lifes == 0:
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
    
    col1 = pg.sprite.groupcollide(arrows, ufos1, True, True)
    for s in col1.keys():
        if len(col1[s]) > 0:
            points += 1
    col2 = pg.sprite.groupcollide(arrows, ufos2, True, True)
    for s in col2.keys():
        if len(col2[s]) > 0:
            points += 2
    rcol = pg.sprite.spritecollide(kausy, rays,True)
    if len(rcol) > 0:
        lifes -= 100
    uselesswords = "i like ducks"
    screen.fill((127,127,127))
    score = ("Health: " + str(lifes) + " Score: " + str(points))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    player.update(mleft, mright)
    player.draw(screen)
    arrows.update()
    arrows.draw(screen)
    rays.update()
    rays.draw(screen)
    ufos1.update(col1)
    ufos1.draw(screen)
    ufos2.update(col2)
    ufos2.draw(screen)
    uselessfont = pg.font.SysFont("Times", uselessvariable)
    uselesstext = uselessfont.render(uselesswords, True, (0,0,255))
    uselesstext_rect = uselesstext.get_rect()
    uselesstext_rect.centerx = screen.get_rect().centerx
    uselesstext_rect.y = 30
    screen.blit(uselesstext,uselesstext_rect)
    pg.display.update()
    u1tick += 1
    if u1tick >= u1max:
        u1tick = 0
        ufos1.add(UFO(r.randint(0,screenw-96),r.randint(0, 256), 1, ufo1,
                      60, ray, 16, 1, 1))
        u1max = r.randint(0,600)
    u2tick += 1
    if u2tick >= u2max:
        u2tick = 0
        ufos2.add(UFO(r.randint(0,screenw-96),r.randint(0, 256), 2, ufo2,
                      30, ray, 16, 1, 2))
        u2max = r.randint(0,2400)
    if uselessvariable > 0:
        uselessvariable -= 1
    if not gf:
        timer.tick(60)

pg.quit()
