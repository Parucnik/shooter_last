from pygame import *
from random import randint
from time import time as get_time


SCREEN_SIZE = (700, 500)
SPRITE_SIZE = 65

def show_label(text, x, y, font_name='Arial', color=(255, 255, 255)):
    font.init()
    font1 = font.SysFont(font_name, 40)
    text = font1.render(text, True, color)
    window.blit(text, (x, y))

class Live:
    def __init__(self, x,y, image_name, lives):
        self.lives = lives
        self.image = transform.scale(image.load(image_name), (30, 30))
        self.x = x
        self.y = y

    def update(self):
        for i in range(self.lives):
            window.blit(self.image, (self.x-i*40, self.y))

lives = Live(650, 20, 'rocket.png', 5)

class GameSprite(sprite.Sprite):
    def __init__(self, image_name, speed, x, y):
        super().__init__()
        self.image = image.load(image_name)
        self.image = transform.scale(self.image, (SPRITE_SIZE, SPRITE_SIZE))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < SCREEN_SIZE[0]-SPRITE_SIZE:
            self.rect.x += self.speed
        if keys_pressed[K_SPACE] and get_time() - self.last_shoot > .2:
            self.shoot()
            self.last_shoot = get_time()
    
    def shoot(self):
        new_bullet = Bullet('bullet.png', 7, self.rect.centerx-3, self.rect.y)
        new_bullet.image = transform.scale(new_bullet.image, (10, 30))
        bullets.add(new_bullet)
        if chetchik2.counter >= 10:
            new_bullet = Bullet('bullet.png', 7, self.rect.centerx-3, self.rect.y, 1)
            new_bullet.image = transform.scale(new_bullet.image, (10, 30))
            bullets.add(new_bullet)
            new_bullet = Bullet('bullet.png', 7, self.rect.centerx-3, self.rect.y, 2)
            new_bullet.image = transform.scale(new_bullet.image, (10, 30))
            bullets.add(new_bullet)
    

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 635)
            missed_counter.counter += 1
            missed_counter.set_text(24,(255,255,255))
        self.reset()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 635)
        self.reset()

class Heart(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 500:
            self.reset()
        else:
            if randint(1, 100) == 1:
                self.rect.y = 0
                self.rect.x = randint(1,635)
                
heart = Heart('rocket.png', 2, randint(1,635), 600)

class Bullet(GameSprite):
    def __init__(self, image_name, speed, x, y, direction=0):
        super().__init__(image_name, speed, x, y)
        self.direction = direction
    
    def update(self):
        self.rect.y -= self.speed
        if self.direction == 1:
            self.rect.x -= self.speed
        if self.direction == 2:
            self.rect.x += self.speed
        self.reset()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(2):
    asteroids.add(Asteroid('asteroid.png', randint(1,2), randint(0, 635), 0))


font.init()

class Counter:
    def __init__(self,text,x,y):
        self.counter = 0
        self.text = text 
        self.pos = (x,y)
    
    def set_text(self,font_size,text_color):
        f = font.SysFont('Arial',font_size)
        self.image = f.render(self.text + str(self.counter),True,text_color)

    def draw(self):
        window.blit(self.image, self.pos)





player = Player('rocket.png', 7, 10, 435)
player.last_shoot = 0

ufos = sprite.Group()
for i in range(5):
    ufos.add(Enemy('ufo.png', 1, randint(0, 635), 0))

window = display.set_mode(SCREEN_SIZE)
display.set_caption('Shooter')

missed_counter = Counter('Счетчик пропущенных:',10,10)
missed_counter.set_text(24,(255,255,255))

chetchik2 = Counter('Счетчик уничтоженных:',10,50)
chetchik2.set_text(24,(255,255,255))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()


pic = image.load('galaxy.jpg')
pic = transform.scale(pic, SCREEN_SIZE)

clock = time.Clock()
FPS = 60
game = True
finish = False

end = get_time()+4
while True:
    clock.tick(FPS)
    window.blit(pic, (0,0))
    show_label(str(int(end - get_time())), 340, 250)
    
    display.update()
    if get_time() > end:
        break
    
while game:
    clock.tick(FPS)
    if finish == False:
        window.blit(pic, (0,0))
        ufos.update()
        player.reset()
        player.update()
        missed_counter.draw()
        chetchik2.draw()    
        bullets.update()
        asteroids.update()
        bullets.draw(window)
        heart.update()
        if sprite.collide_rect(player, heart):
            lives.lives += 1
            heart.rect.y = 600
        lives.update()
        if chetchik2.counter >= 50:
            show_label('Победа', 270, 200)
            finish = True
        if missed_counter.counter >= 3:
            lives.lives -= 1
            missed_counter.counter = 0
            
        if sprite.spritecollide(player, ufos, False) or sprite.spritecollide(player, asteroids, False):
            for s in sprite.spritecollide(player, ufos, False) + sprite.spritecollide(player,asteroids, False):
                s.rect.y = 0
                s.rect.x = randint(1,635)
                lives.lives -= 1
            
        if lives.lives <= 0:    
            show_label('Поражение...', 250, 200)
            finish = True
        display.update()    
        
        list_monsters = sprite.groupcollide(ufos, bullets, False, True)
        for monster in list_monsters:
            monster.rect.y = 0
            monster.rect.x = randint(1, 635)
            chetchik2.counter += 1
            chetchik2.set_text(24,(255,255,255))
        
    for e in event.get():
        if e.type == QUIT:
            game = False