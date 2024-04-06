from pygame import *
from random import *
from time import time as timer


font.init()
font = font.SysFont('Arial', 35)
lose = font.render("YOU LOSE", True, (255,0,0))
win = font.render("YOU WIN", True, (0,255,0))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
        def update(self):
            keys_pressed = key.get_pressed()

            if keys_pressed[K_LEFT] and self.rect.x > 10:
                self.rect.x -= self.speed
            if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
                self.rect.x += self.speed

        def fire(self):
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 555, 514, 100)
            bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Aster(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost = lost + 1


        

win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("shooter")

clock = time.Clock()
FPS = 60

img_back = 'galaxy.jpg'

background = transform.scale(image.load(img_back),(win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

player = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

enemys = sprite.Group()
bullets = sprite.Group()
asts = sprite.Group()


for i in range(1, 6):
    enemy = Enemy('ufo.png', randint(80,win_width - 80), 0, 80, 50, randint(1, 5))
    enemys.add(enemy)


for i in range(1, 3):
    ast = Aster('asteroid.png',randint(80,win_width - 80), 0, 80, 80, randint(1, 2))
    asts.add(ast)

#игровой цикл
run = True
finish = False
rel_time = False
num_fire = 0
score = 0
goal = 10
lost = 0
max_lost = 555
life = 3


while run:
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            run = False


        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire( )
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    


    if finish == False:

            

    


        window.blit(background, (0,0))

        text_score = font.render("stchot:" + str(score), 1, (255,255,255))
        window.blit(text_score, (10,20))
        text_lost = font.render("propuscheno:" + str(lost), 1, (255,255,255))
        window.blit(text_lost, (10,50))
        
        enemys.update()
        player.update()
        bullets.update()
        asts.update()

        player.reset()
        enemys.draw(window)
        bullets.draw(window)
        asts.draw(window)


        if rel_time == True:
            now_time = timer()


            if now_time - last_time < 3:
                reload = font.render("Идёт перезарядка", 1, (180,0,0))
                window.blit(reload, (win_width / 2, win_height - 50))
            else:
                num_fire = 0
                rel_time = False

        sprites_list = sprite.groupcollide(enemys, bullets, True, True)


        for c in sprites_list:
            score += 1
            enemy = Enemy('ufo.png', randint(80,win_width - 80), 0, 80, 50, randint(1, 10))
            enemys.add(enemy)

        if sprite.spritecollide(player, enemys, False) or sprite.spritecollide(player, asts, False):
            sprite.spritecollide(player, enemys, True)
            sprite.spritecollide(player, asts, True)
            life -= 1

        if life <= 0 or lost >= max_lost:
            window.blit(lose ,(300,300))
            finish = True

        


        if score >= goal:
            window.blit(win ,(300,300))
            finish = True

        if life == 3:
            life_color = (0,150,0)
        elif life == 2:
            life_color = (150,150,0)
        elif life == 1:
            life_color = (150,0,0)
        
        text_life = font.render(str(life),1,life_color)
        window.blit(text_life, (win_width - 10,10))



    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        num_fire = 0
        rel_time = False

        for b in bullets:
            b.kill()

        for e in enemys:
            e.kill()

            for a in asts:
                a.kill()


        time.delay(5000)

        for i in range(1, 6):
            enemy = Enemy('ufo.png', randint(80,win_width - 80), 0, 80, 50, randint(1, 10))
            enemys.add(enemy)

        for i in range(1, 3):
            ast = Aster('asteroid.png',randint(80,win_width - 80), 0, 80, 80, randint(1, 2))
            asts.add(ast)

            

        

    display.update()




