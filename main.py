import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load("images/background.png")

mixer.music.load("sounds/background.wav")
mixer.music.play(-1)

pygame.display.set_caption("Turtle Invader")
icon = pygame.image.load('images/turtle64.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load("images/turtle64.png")
playerX = 370
playerY = 435
playerX_change = 0

# Enemy
enemyImgList = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numEnemy = 4

enemyImg = pygame.image.load("images/enemy.png")
enemyImg = pygame.transform.scale(enemyImg, (50, 50))
enemyLeft = enemyImg
enemyRight = pygame.transform.flip(enemyImg, True, False)

for i in range(numEnemy):

    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    change = random.choice([-0.2, -0.1, 0.1, 0.2])
    enemyX_change.append(change)
    if change <= 0:
        enemyImgList.append(enemyLeft)
    elif change >= 0:
        enemyImgList.append(enemyRight)
    enemyY_change.append(30)

bulletImg = pygame.transform.flip(pygame.image.load("images/raindrop.png"), False, True)
bulletImg = pygame.transform.scale(bulletImg, (20, 20))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

explosionIMG = pygame.image.load("images/fireworks.png")
explosion_state = "off"

over_font = pygame.font.Font('freesansbold.ttf', 70)

def show_score(x, y):
    score = font.render(f"Score : {score_value}", True, (0, 0, 0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImgList[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y - 20))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def explosion(x, y):
    global explosion_state
    explosion_state = "on"


    """for i in range(20, 60):
        screen.blit((pygame.transform.scale(explosionIMG, (i, i))), x, y)"""

    screen.blit(explosionIMG, x, y)


difficulty = "easy"
increase = 2

running = True
while running:
    screen.fill((0, 130, 50))
    screen.blit(background, (0, 0))

    if score_value >= 40:
        difficulty = "hard"
        numEnemy = 8
        for i in range(increase):
            enemyX.append(random.randint(0, 735))
            enemyY.append(random.randint(50, 150))
            change = random.choice([-0.2, -0.1, 0.1, 0.2])
            enemyX_change.append(change)
            if change <= 0:
                enemyImgList.append(enemyLeft)
            elif change >= 0:
                enemyImgList.append(enemyRight)
            enemyY_change.append(30)

    elif score_value >= 20:
        difficulty = "med"
        numEnemy = 6
        for i in range(increase):
            enemyX.append(random.randint(0, 735))
            enemyY.append(random.randint(50, 150))
            change = random.choice([-0.2, -0.1, 0.1, 0.2])
            enemyX_change.append(change)
            if change <= 0:
                enemyImgList.append(enemyLeft)
            elif change >= 0:
                enemyImgList.append(enemyRight)
            enemyY_change.append(30)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if difficulty == "med":
                    playerX_change = -0.6
                elif difficulty == "hard":
                    playerX_change = -0.8
                else:
                    playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                if difficulty == "med":
                    playerX_change = 0.6
                elif difficulty == "hard":
                    playerX_change = 0.8
                else:
                    playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("sounds/bullet.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    playerX += playerX_change

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    for i in range(numEnemy):
        if enemyY[i] > 400:
            for j in range(numEnemy):
                enemyY[j] = 2000
            game_over_text()
            break

        if enemyX[i] >= 736:
            enemyX_change[i] = -enemyX_change[i]
            enemyImgList[i] = pygame.transform.flip(enemyImgList[i], True, False)
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = -enemyX_change[i]
            enemyImgList[i] = pygame.transform.flip(enemyImgList[i], True, False)
            enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("sounds/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            #explosion(30, 30)
            #explosion_state = "off"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

            if difficulty == "easy":
                change = random.choice([-0.2, -0.1, 0.1, 0.2])
                enemyX_change[i] = change
            elif difficulty == "med":
                change = random.choice([-0.27, -0.2, 0.2, 0.27])
                enemyX_change[i] = change
            elif difficulty == "hard":
                change = random.choice([-0.4, -0.3, 0.3, 0.4])
                enemyX_change[i] = change
            if enemyX_change[i] <= 0:
                enemyImgList[i] = enemyLeft
            elif enemyX_change[i] >= 0:
                enemyImgList[i] = enemyRight

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
