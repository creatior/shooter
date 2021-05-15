from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x >= 20:
            self.rect.x -= (self.speed-5)
        if keys_pressed[K_RIGHT] and self.rect.x <= 615:
            self.rect.x += (self.speed-5)
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)
lose = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        global lose
        if self.rect.y > 500:
            lose += 1
            self.rect.y = 0
            self.rect.x = randint(80,620)
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

window = display.set_mode((700,500))
display.set_caption("Шутер")
background = transform.scale(image.load('galaxy.jpg'),(700,500))
clock = time.Clock()
FPS = 60

player = Player('rocket.png',350,420,65,65,10)
monsters = sprite.Group()
bullets = sprite.Group()

for i in range(6):
    monsters.add(Enemy('enemy'+str(randint(1,2))+'.png',randint(80,620),0,65,65,randint(1,2)))


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
shot = mixer.Sound('fire.ogg')
score = 0
font.init()
font1 = font.SysFont('Arial.ttf',30)
font2 = font.SysFont('Arial.ttf',30)

text_lose = font1.render('Пропущено: ' + str(lose),1,(255,255,255))
text_score = font2.render('Счёт: '+ str(score),1,(255,255,255))

game = True
while game:      
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                shot.play()
                player.fire()
    sprites_list = sprite.groupcollide(monsters,bullets,True,True)
    for s in sprites_list:
        score += 1
        monsters.add(Enemy('enemy'+str(randint(1,3))+'.png',randint(80,620),0,65,65,randint(1,2)))
    if lose > 3 or sprite.spritecollide(player,monsters,False):
        game = False
    window.blit(background,(0,0))
    clock.tick(FPS)
    player.reset()
    player.update()
    bullets.draw(window)
    bullets.update()
    monsters.update()
    monsters.draw(window)
    text_lose = font1.render('Пропущено: ' + str(lose),1,(255,255,255))
    text_score = font2.render('Счёт: ' + str(score),1,(255,255,255))
    window.blit(text_lose,(10,10))
    window.blit(text_score,(10,50))
    display.update()