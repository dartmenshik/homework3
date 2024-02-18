from random import randint
from pygame import *

lost = 0
hits = 0

image_background = "galaxy.jpg"
image_hero = "rocket.png"
image_enemy = "ufo.png"
image_bullet = "bullet.png"
image_special_bullet = "special_bullet.png"

window_width = 700
window_height = 500

window = display.set_mode((window_width, window_height))
display.set_caption("Shooter")

FPS = 30
clock = time.Clock()

background = transform.scale(image.load(image_background), (window_width, window_height))

font.init()
sysfont = font.Font(None, 36)
font2 = font.Font(None, 80)
# Тексти для перемоги та програшу
text_win = font2.render('YOU WIN!', True, (255, 255, 255))
text_lose = font2.render('YOU LOSE!', True, (180, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_position_x, sprite_position_y, sprite_width, sprite_height, sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (sprite_width, sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_position_x
        self.rect.y = sprite_position_y
        self.width = sprite_width
        self.height = sprite_height
        self.speed = sprite_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] and self.rect.x < window_width - 100:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 20:
            self.rect.x -= self.speed
        if keys[K_UP] and self.rect.y > window_height - 200:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < window_height - 100:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet(image_bullet, self.rect.x + self.width / 2, self.rect.y, 10, 30, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > window_height:
            self.rect.x = randint(50, window_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 or self.rect.y > window_height:
            self.kill()
        enemies_hit = sprite.groupcollide(monsters, bullets, True, True)
        for enemy in enemies_hit:
            global hits
            hits += 1
            monster = Enemy(image_enemy, randint(50, window_width - 80), 0, 80, 50, randint(1, 4))
            monsters.add(monster)


bullets = sprite.Group()
special_bullets = sprite.Group()
monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy(image_enemy, randint(50, window_width - 80), 0, 80, 50, randint(1, 5))
    monsters.add(monster)

player = Player(image_hero, window_width / 2, window_height - 100, 80, 100, 10)

run = True
finish = False
special_bullet_cooldown = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
 

    if not finish:
        window.blit(background, (0, 0))
        # Тут об'єкти створюємо на екрані вперше
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        special_bullets.draw(window)
        # Тут оновлюємо кожен раз при циклі
        player.update()
        monsters.update()
        bullets.update()
        special_bullets.update() 

        text_missed = sysfont.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        text_shot = sysfont.render('Збито:' + str(hits), 1, (255, 255, 255))
        window.blit(text_missed, (10, 50))
        window.blit(text_shot, (10, 80))

        # Це вказуємо тут, тут відстежуються умови зіткнення кожен раз при проходженні циклу
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            hits += 1
            monster = Enemy(image_enemy, randint(50, window_width - 80), 0, 80, 50, randint(1, 5))
            monsters.add(monster)
        # Умови програшу
        if sprite.spritecollide(player, monsters, False) or lost >= 5:
            finish = True
            window.blit(text_lose, (200, 200))
        # Умови перемоги
        if hits >= 10:
            finish = True
            window.blit(text_win, (200, 200))
        # Оновити дісплей кожен раз як буде проходити цикл
        display.update()
    # Швидкість оновлення кадрів
    clock.tick(30)