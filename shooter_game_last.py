from pygame import *
from random import randint
from time import time as get_time


font.init()
# Переменные, задающие размеры игровой сцены, спрайтов и цвет
SCREEN_SIZE = (920, 980)
SPRITE_SIZE = 70
WHITE = (255, 255, 255)

def show_label(text: str, x: int, y: int, font_name: str ='Arial', font_size: int = 40, color: tuple = WHITE) -> None:
    '''
    Фунция выводит надпись на игровую сцену window.
    
    Аргументы:
    x, y - координаты выводимого текста
    text - выводимый текст
    font_name - имя шрифта, которым будет написан текст
    font_size - размер шрифта
    color - цвет текста (RGB) 
    '''
    font1 = font.SysFont(font_name, font_size)
    text = font1.render(text, True, color)
    window.blit(text, (x, y))

class Live:
    ''' Жизни для игрока '''
    def __init__(self, x: int, y: int, image_name: str, lives: int) -> None:
        ''' Аргументы:
        x, y - координаты, от которой начинается отрисовка жизней
        image_name - имя файла-картинки, который отображает жизнь
        lives - количество жизней
        '''
        self.lives = lives
        self.image = transform.scale(image.load(image_name), (SPRITE_SIZE//2, SPRITE_SIZE//2))
        self.x = x
        self.y = y

    def update(self) -> None:
        ''' Отрисовывает жизни на экране '''
        for i in range(self.lives):
            window.blit(self.image, (self.x - i*40, self.y))


class GameSprite(sprite.Sprite):
    ''' Родительский класс для всех игровых объектов (спрайтов) '''
    def __init__(self, image_name: str, speed: int, x: int, y: int) -> None:
        ''' Аргументы:        
        image_name - имя файла-картинки, который отображает жизнь
        speed - скорость движения спрайта
        x, y - координаты, от которой начинается отрисовка жизней
        '''
        super().__init__()
        self.image = image.load(image_name)
        self.image = transform.scale(self.image, (SPRITE_SIZE, SPRITE_SIZE))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def reset(self) -> None:
        ''' Отрисовывает сам спрайт на экране '''
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    ''' Класс для игрока '''
    def update(self) -> None:
        '''
        Обрабатывает нажатия клавиш:
        a, d - движение влево/право
        пробел - выстрел
        '''
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < SCREEN_SIZE[0]-SPRITE_SIZE:
            self.rect.x += self.speed
        if keys_pressed[K_SPACE] and get_time() - self.last_shoot_time > .2:
            self.shoot()
            self.last_shoot_time = get_time()
    
    def shoot(self) -> None:
        '''
        Метод для выстрела
        '''
        new_bullet = Bullet('bullet.png', 7, self.rect.centerx-3, self.rect.y)
        new_bullet.image = transform.scale(new_bullet.image, (10, 30))
        bullets.add(new_bullet)
        if killed_counter.counter >= 10:
            new_bullet = Bullet('bullet.png', 7, self.rect.centerx-3, self.rect.y, 1)
            new_bullet.image = transform.scale(new_bullet.image, (10, 30))
            bullets.add(new_bullet)
            new_bullet = Bullet('bullet.png', 7, self.rect.centerx-3, self.rect.y, 2)
            new_bullet.image = transform.scale(new_bullet.image, (10, 30))
            bullets.add(new_bullet)
    

class Enemy(GameSprite):
    ''' Класс для врагов (НЛО) '''
    def __init__(self, image_name: str, speed: int, x: int, y: int) -> None:
        ''' Аргументы:        
        image_name - имя файла-картинки, который отображает жизнь
        speed - скорость движения спрайта
        x, y - координаты, от которой начинается отрисовка жизней
        '''
        super().__init__(image_name, speed, x, y)
        self.hp = randint(1, 3)
    
    def update(self) -> None:
        '''
        Движение врагов вниз.
        Если враг долетает до низа игровой сцены, то переставляем его наверх и увеличиваем счетчик пропущенных врагов.
        '''
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
            missed_counter.counter += 1
            missed_counter.render_text(24, WHITE)


class Asteroid(GameSprite):
    ''' Класс для астероидов '''
    def update(self) -> None:
        ''' Движение астероидов вниз '''
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)

class Heart(GameSprite):
    ''' Бонус - жизнь для игрока '''
    def update(self) -> None:
        ''' Движение бонуса и его случайное появление'''
        self.rect.y += self.speed
        if self.rect.y < SCREEN_SIZE[1]:
            self.reset()
        else:
            if randint(1, 100) == 1:
                self.rect.y = 0
                self.rect.x = randint(1, SCREEN_SIZE[0] - SPRITE_SIZE)


class Bullet(GameSprite):
    ''' Класс для пуль '''
    def __init__(self, image_name, speed, x, y, direction=0) -> None:
        ''' Аргументы:        
        image_name - имя файла-картинки, который отображает жизнь
        speed - скорость движения спрайта
        x, y - координаты, от которой начинается отрисовка жизней
        direction - направление движения пули:
            0 - вертикально вверх
            1 - вверх и влево
            2 - вверх и вправо
        '''
        super().__init__(image_name, speed, x, y)
        self.direction = direction
    
    def update(self) -> None:
        ''' Движение пули вверх '''
        self.rect.y -= self.speed
        if self.direction == 1:
            self.rect.x -= self.speed
        if self.direction == 2:
            self.rect.x += self.speed

class Counter:
    ''' Класс-счетчик в виде надписи на экране '''
    def __init__(self, text: str, x: int, y: int) -> None:
        ''' Аргументы:
        text - выводимый текст
        x, y - координаты, где будет выведен текст
        '''
        self.counter = 0
        self.text = text 
        self.pos = (x,y)
    
    def render_text(self, font_size: int, text_color: tuple) -> None:
        ''' Рендерит текст в картинку (свойство image) 
        font_size - размер шрифта
        text_color - цвет текста
        '''
        f = font.SysFont('Arial', font_size)
        self.image = f.render(self.text + str(self.counter),True,text_color)

    def draw(self) -> None:
        ''' Отрисовывает текст на экран '''
        window.blit(self.image, self.pos)
        
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(2):
    asteroids.add(Asteroid('asteroid.png', randint(1,2), randint(0, 635), 0))

lives = Live(SCREEN_SIZE[0] - SPRITE_SIZE//2, 20, 'rocket.png', 5)


heart = Heart('rocket.png', 2, randint(1,SCREEN_SIZE[0] - SPRITE_SIZE), SCREEN_SIZE[1]*2)


player = Player('rocket.png', 7, 10, SCREEN_SIZE[1] - SPRITE_SIZE - 5)
player.last_shoot_time = 0

ufos = sprite.Group()
for i in range(5):
    ufos.add(Enemy('ufo.png', randint(1, 3), randint(0, 635), 0))

window = display.set_mode(SCREEN_SIZE)
display.set_caption('Shooter')

missed_counter = Counter('Счетчик пропущенных:',10,10)
missed_counter.render_text(24,(255,255,255))

killed_counter = Counter('Счетчик уничтоженных:',10,50)
killed_counter.render_text(24,(255,255,255))

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
    show_label(str(int(end - get_time())), SCREEN_SIZE[0]//2 - 20, SCREEN_SIZE[1]//2 - 20)
    
    display.update()
    if get_time() > end:
        break
    
while game:
    clock.tick(FPS)
    if finish == False:
        # Перерисовка всех объектов в игре
        window.blit(pic, (0,0))
        ufos.update()
        ufos.draw(window)
        player.reset()
        player.update()
        missed_counter.draw()
        killed_counter.draw()    
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.draw(window)
        heart.update()
        if sprite.collide_rect(player, heart):
            lives.lives += 1
            heart.rect.y = SCREEN_SIZE[1]*2
        lives.update()
        if killed_counter.counter >= 50:
            show_label('Победа', SCREEN_SIZE[0]//2-40, SCREEN_SIZE[1]//2-20)
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
            show_label('Поражение...', SCREEN_SIZE[0]//2-40, SCREEN_SIZE[1]//2-20)
            finish = True
        display.update()    
        
        list_monsters = sprite.groupcollide(ufos, bullets, False, True)
        for monster in list_monsters:
            monster.hp -= 1
            if monster.hp <= 0:
                monster.hp = randint(1, 3)
                monster.rect.y = 0
                monster.rect.x = randint(1, SCREEN_SIZE[0]-SPRITE_SIZE)
                killed_counter.counter += 1
                killed_counter.render_text(24, (255,255,255))
                if killed_counter.counter == 20:
                    ufos.add(Enemy('ufo.png', randint(1, 3), randint(0, SCREEN_SIZE[0]-SPRITE_SIZE), 0))
                    ufos.add(Enemy('ufo.png', randint(1, 3), randint(0, SCREEN_SIZE[0]-SPRITE_SIZE), 0))
        
    for e in event.get():
        if e.type == QUIT:
            game = False
