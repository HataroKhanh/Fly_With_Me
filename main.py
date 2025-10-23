import pygame
import random

pygame.init()

screen_width, screen_height = 1280 // 2, 720 // 2
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fly With Me =)")
pygame.display.set_icon(pygame.image.load('icon.ico'))

clock = pygame.time.Clock()
cooldown_tracker = 0

bg = pygame.image.load(r'bg.png')
bg = pygame.transform.scale(bg, (1280 // 2, 720 // 2))

font_size = 36
font = pygame.font.SysFont(None, font_size)
text = ''
text_color = (255, 255, 255)
score = 0

check_game_over = False

class Monster:
    def __init__(self):
        self.x = random.randint(700, 5000)
        self.y = random.randint(1, 300)
        self.monster = pygame.image.load("monster.png")
        self.monster_rect = self.monster.get_rect()
        self.monster_rect.x = self.x
        self.monster_rect.y = self.y
    def Check_screen(self):
            if self.monster_rect.x<0:
                return True
            return False
    def draw(self):
        screen.blit(self.monster, (self.monster_rect.x, self.monster_rect.y))

    def update_pos_x_monster(self):
        self.monster_rect.x -= 3


class Dan:
    def __init__(self, rectx, recty):
        self.image_dan = pygame.Surface((10, 10))
        self.rect_dan = self.image_dan.get_rect()
        self.rect_dan.x = rectx+65
        self.rect_dan.y = recty+40

    def update_pos_x_dan(self):
        self.rect_dan.x += 20

    def check_collision(self, monsters):
        for monster in monsters:
            if self.rect_dan.colliderect(monster.monster_rect):
                monsters.remove(monster)
                return True
        return False
    def check_pos_to_del(self):
        if self.rect_dan.x > 590:
            return True
    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.rect_dan.x, self.rect_dan.y), 5)


class Player:
    def __init__(self):
        self.playerimg = pygame.image.load(r'player.png')
        self.player_rect = pygame.Rect(10,10,40,40)
        self.player_rect.x = self.player_rect.x
        self.player_rect.y = self.player_rect.y

    def check_screen(self,check_game_over):
        if not check_game_over:
            if self.player_rect.x < 0:
                self.player_rect.x = 0
            if self.player_rect.y < 0:
                self.player_rect.y = 0
            if self.player_rect.right > screen_width:
                self.player_rect.right = screen_width
            if self.player_rect.bottom > screen_height:
                self.player_rect.bottom = screen_height

    def shot(self, cooldown_tracker, monsters):
        if cooldown_tracker == 0:
            bullet = Dan(self.player_rect.x, self.player_rect.y)
            bullets.append(bullet)
            
    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_rect.x -= 5
        elif keys[pygame.K_RIGHT]  | keys[pygame.K_d]:
            self.player_rect.x += 5
        elif keys[pygame.K_UP] | keys[pygame.K_w]:
            self.player_rect.y -= 5
        elif keys[pygame.K_DOWN] | keys[pygame.K_s]:
            self.player_rect.y += 5
        if keys[pygame.K_SPACE]:
            self.shot(cooldown_tracker, monsters)
        if keys[pygame.K_p]:
            clock.tick(30)
    def draw(self):
        screen.blit(self.playerimg, (self.player_rect.x, self.player_rect.y))
def Check_game_over(check_game_over):
    if check_game_over:
        return True
    return False
player = Player()
bullets = []
monsters = []
def spawn():
    for i in range(10):  
        monster = Monster()
        monsters.append(monster)
running = True
while running:
    clock.tick(60)
    text_surface = font.render(text, True, text_color)
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if len(monsters)==0:
        spawn()

    cooldown_tracker += clock.get_time()
    if cooldown_tracker > 400:
        cooldown_tracker = 0

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.check_screen(check_game_over)
    for monster in monsters:
        monster.draw()
        monster.update_pos_x_monster()
        monster.Check_screen()
        if monster.monster_rect.colliderect(player.player_rect):
            check_game_over = True
        if monster.Check_screen():
            monsters.remove(monster)

    for bullet in bullets:
        bullet.update_pos_x_dan()
        bullet.draw()
        if bullet.check_pos_to_del():
            bullets.remove(bullet)
        if bullet.check_collision(monsters):
            bullets.remove(bullet)
            text = ''
            score += 1
            text += str(score)
    if Check_game_over(check_game_over):
        running = False
    screen.blit(text_surface,(1,1))
    player.draw()
    pygame.display.flip()

pygame.quit()
