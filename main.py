import pygame
from sys import exit


BAT_WIDTH = 50
BAT_HEIGHT = 10
BALL_RADIUS = 7
BALL_SPEED = 5
ball_extra_speed = 0
brick_scores = {
    'yellow': 1,
    'green': 3,
    'orange': 5,
    'red': 7
}


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = BAT_WIDTH
        surf = pygame.Surface((self.width, BAT_HEIGHT))
        surf.fill('Blue')
        self.image = surf
        self.rect = surf.get_rect(center=(200, 750))
        self.movement = 0
        self.halved = False

    def player_input(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0] and mouse[2]:
            self.movement = 0
        elif mouse[0]:
            self.movement = -10
        elif mouse[2]:
            self.movement = 10
        else:
            self.movement = 0

    def update(self):
        self.player_input()
        self.rect.left += self.movement
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 400:
            self.rect.right = 400


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS*2, BALL_RADIUS*2))
        self.image.fill('Black')
        self.image.set_colorkey('Black')
        pygame.draw.circle(self.image, 'White', (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect(center=(200, 500))
        self.x_speed = 1
        self.y_speed = 1
        self.speed = BALL_SPEED + ball_extra_speed
        self.strike_counter = 0
        self.hits = 0
        self.orange_hit = False
        self.red_hit = False
        self.lives = 2

    def update(self):
        self.rect.left += self.x_speed
        self.rect.top += self.y_speed
        self.strike_counter -= 1
        if self.rect.top < 0:
            if not player.sprite.halved:
                player.sprite.halved = True
                player.sprite.width /= 2
                player.sprite.image = pygame.Surface((player.sprite.width, BAT_HEIGHT))
                player.sprite.image.fill('Blue')
                player.sprite.rect = player.sprite.image.get_rect(center=player.sprite.rect.center)

            self.rect.top = 0
            self.y_speed *= -1
        elif self.rect.left < 0:
            self.rect.left = 0
            self.x_speed *= -1
        elif self.rect.right > 400:
            self.rect.right = 400
            self.x_speed *= -1
        elif self.rect.top > 800:
            death_sound.play()
            self.lives -= 1
            self.rect.center = (200, 500)
            self.x_speed = 1
            self.y_speed = 1


class Brick(pygame.sprite.Sprite):
    def __init__(self, colour, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 20))
        self.image.fill(colour)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.score = brick_scores[colour]
        self.colour = colour


def rescale_speed(x, speed):
    if ball.sprite.speed**2 < x**2:
        x = ball.sprite.speed * 0.95
        ball.sprite.x_speed = x
    new_y_speed = (ball.sprite.speed**2 - x**2)**(1/2)
    return new_y_speed * -1


def detect_collisions():
    global score
    if pygame.sprite.spritecollideany(player.sprite, ball):
        bat_sound.play()
        struck_ball = pygame.sprite.spritecollideany(player.sprite, ball)
        if struck_ball.strike_counter < 0:
            struck_ball.strike_counter = 10
            struck_ball.y_speed *= -1
            impact = struck_ball.rect.center[0] - player.sprite.rect.center[0]
            struck_ball.x_speed += (impact * struck_ball.speed) / (player.sprite.width * 0.5 + BALL_RADIUS)
            struck_ball.y_speed = rescale_speed(struck_ball.x_speed, struck_ball.speed)
            struck_ball.hits += 1
            if struck_ball.hits == 4:
                struck_ball.speed += 2
            elif struck_ball.hits == 12:
                struck_ball.speed += 2
    hit_list = pygame.sprite.spritecollide(ball.sprite, bricks, True)
    if hit_list:
        brick_sound.play()
        h, v = 0, False
        for brick in hit_list:
            if not ball.sprite.orange_hit and brick.colour == 'orange':
                ball.sprite.orange_hit = True
                ball.sprite.speed += 2
            if not ball.sprite.red_hit and brick.colour == 'red':
                ball.sprite.red_hit = True
                ball.sprite.speed += 2
            if brick.rect.left - BALL_RADIUS < ball.sprite.rect.center[0] < brick.rect.right + BALL_RADIUS:
                v = True
            if brick.rect.right < ball.sprite.rect.right:
                h += 1
            elif brick.rect.left > ball.sprite.rect.left:
                h -= 1
            if h > 0:
                ball.sprite.x_speed = abs(ball.sprite.x_speed)
            elif h < 0:
                ball.sprite.x_speed = -abs(ball.sprite.x_speed)
            if v:
                ball.sprite.y_speed *= -1
            score += brick.score


def display_score():
    global score
    score_surf = font.render(str(score), False, 'white')
    score_rect = score_surf.get_rect(midtop=(100, 50))
    lives_surf = font.render(str(ball.sprite.lives), False, 'white')
    lives_rect = lives_surf.get_rect(midtop=(300, 50))
    screen.blit(score_surf, score_rect)
    screen.blit(lives_surf, lives_rect)


def populate_bricks():
    for i in range(7):
        for j in range(2):
            bricks.add(Brick('yellow', 10 + i * 55, 300 + j * 25))
    for i in range(7):
        for j in range(2):
            bricks.add(Brick('green', 10 + i * 55, 250 + j * 25))
    for i in range(7):
        for j in range(2):
            bricks.add(Brick('orange', 10 + i * 55, 200 + j * 25))
    for i in range(7):
        for j in range(2):
            bricks.add(Brick('red', 10 + i * 55, 150 + j * 25))


pygame.init()
game_active = True
font = pygame.font.Font('font/Pixeltype.ttf', 100)
bat_sound = pygame.mixer.Sound('sounds/ping_pong_8bit_beeep.ogg')
brick_sound = pygame.mixer.Sound('sounds/ping_pong_8bit_plop.ogg')
death_sound = pygame.mixer.Sound('sounds/ping_pong_8bit_peeeeeep.ogg')
screen = pygame.display.set_mode((400, 800))
pygame.display.set_caption('Breakout')
clock = pygame.time.Clock()
score = 0
player = pygame.sprite.GroupSingle()
player.add(Player())

ball = pygame.sprite.GroupSingle()
ball.add(Ball())

bricks = pygame.sprite.Group()
# for i in range(7):
#     for j in range(2):
#         bricks.add(Brick('yellow', 10 + i * 55, 300 + j * 25))
# for i in range(7):
#     for j in range(2):
#         bricks.add(Brick('green', 10 + i * 55, 250 + j * 25))
# for i in range(7):
#     for j in range(2):
#         bricks.add(Brick('orange', 10 + i * 55, 200 + j * 25))
# for i in range(7):
#     for j in range(2):
#         bricks.add(Brick('red', 10 + i * 55, 150 + j * 25))
populate_bricks()
bg = pygame.Surface((400, 800))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.empty()
                ball.empty()
                bricks.empty()
                score = 0
                player.add(Player())
                ball.add(Ball())
                populate_bricks()
                game_active = True
    if game_active:
        if len(bricks) == 0:
            player.empty()
            ball_extra_speed += 5
            player.add(Player())
            ball.sprite.rect.center = (200, 500)
            ball.sprite.x_speed = 1
            ball.sprite.y_speed = 1
            populate_bricks()
        player.update()
        ball.update()
        detect_collisions()
        screen.blit(bg, (0, 0))
        display_score()
        bricks.draw(screen)
        player.draw(screen)
        ball.draw(screen)

        if ball.sprite.lives < 0:
            game_active = False
    else:
        screen.fill('black')
        game_over = font.render(f'Game Over.', False, 'white')
        game_over_rect = game_over.get_rect(center=(200, 400))
        message = font.render(f'Score: {score}', False, 'white')
        message_rect = message.get_rect(center=(200, 480))
        click = font.render(f'Click to play', False, 'white')
        click_rect = click.get_rect(center=(200, 560))
        screen.blit(game_over, game_over_rect)
        screen.blit(message, message_rect)
        screen.blit(click, click_rect)
    pygame.display.update()
    clock.tick(60)
