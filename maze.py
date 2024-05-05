from pygame import *
from random import randint

def getRandomColor():
    return(randint(0, 255), randint(0, 255), randint(0, 255))

class Wall(sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        self.w = w 
        self.h = h 
        self.color = color
        self.img = Surface((self.w, self.h))
        self.img.fill(color)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw_wall(self):
        window.blit(self.img, (self.rect.x, self.rect.y))
class GameSprite(sprite.Sprite):
    def __init__(self, image_, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_), (80, 80))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)
    def update(self):
        keys = key.get_pressed()
        self.oldPos = (self.rect.x, self.rect.y)
        if keys[K_w] and self.rect.y > self.speed:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 800 - self.rect.height - self.speed:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > self.speed:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 1120 - self.rect.width - self.speed:
            self.rect.x += self.speed 
    def goBack(self):
        self.rect.x, self.rect.y = self.oldPos
    def goStart(self):
        self.rect.x, self.rect.y = (0, 0)
class Enemy(GameSprite):
    def __init__(self, image, x, y, speed, x1, x2):
        super().__init__(image, x, y, speed)  
        if x1 < x2:
            self.xLeft = x1
            self.xRight = x2
        else:
            self.xLeft = x2
            self.xRight = x1      
        self.dir = 'left'
        self.rect.x = self.xRight      
    def update(self):
        if self.dir == 'left':
            if self.rect.x > self.xLeft:
                self.rect.x -= self.speed
            else:
                self.dir = 'right'
        else:
            if self.rect.x < self.xRight:
                self.rect.x += self.speed
            else:
                self.dir = 'left'
#создай окно игры
window = display.set_mode((1120, 800))
display.set_caption('Лабиринт')
#задай фон сцены
background = transform.scale(image.load('background.jpg'), (1120, 800))
#создай 2 спрайта и размести их на сцене
player = Player('hero.png', 0, 0, 5)
enemy1 = Enemy('cyborg.png', 600, 292, 5, 300, 900)
enemy2 = Enemy('cyborg.png', 600, 564, 4, 0, 600)
#добовляем сокровищя 
treasure = GameSprite('treasure.png', 1040, 720, 0)
#сoздаём стены
wallList = list()
wallList.append(Wall(0, 120, 1000, 16, getRandomColor()))
wallList.append(Wall(900, 256, 220, 16, getRandomColor()))
wallList.append(Wall(0, 256, 780, 16, getRandomColor()))
wallList.append(Wall(0, 392, 500, 16, getRandomColor()))
wallList.append(Wall(620, 392, 500, 16, getRandomColor()))
wallList.append(Wall(120, 528, 1000, 16, getRandomColor()))
wallList.append(Wall(0, 664, 450, 16, getRandomColor()))
wallList.append(Wall(570, 664, 550, 16, getRandomColor()))
#работа со звуками
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')
#обработай событие «клик по кнопке "Закрыть окно"»
gameOver = False
finish = 0 #0-играем 1-выйграли 2-проиграли 
clock = time.Clock()
FPS = 60
font.init()
fnt = font.Font(None, 170)
win = fnt.render('YOU WIN', True, (80, 200, 120))
lose = fnt.render('YOU LOSE', True, (220, 20, 60))
while not gameOver:
    window.blit(background, (0, 0))
    events = event.get()
    for ev in events:
        if ev.type == QUIT:
            gameOver = True
    if not finish:
        player.update()
        player.reset()
        if sprite.collide_rect(player, treasure):
            finish = 1
            money.play()
        enemy1.update()
        enemy2.update()
        enemy1.reset()
        enemy2.reset()
        if sprite.collide_rect(player, enemy1) or sprite.collide_rect(player, enemy2):
            finish = 2 
        treasure.reset()
        for wall in wallList: 
            wall.draw_wall()
            if sprite.collide_rect(player, wall): 
                player.goBack()
                player.reset()
                kick.play()
    else:
        keys = key.get_pressed()
        if keys[K_r]:
            player.goStart()
            finish = 0
    if finish == 1:
        window.blit(win, (300, 350))
    elif finish == 2:
        window.blit(lose, (250, 350))
    display.update()
    clock.tick(FPS)