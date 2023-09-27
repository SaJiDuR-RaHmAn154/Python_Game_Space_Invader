import pygame
import random
import math
import os
from pygame import mixer

pygame.init()  # Including Pygame Features

# Creating Screen(width,height)
screen = pygame.display.set_mode((800, 600))

# Background Image
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('bg_music.MP3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
logo = pygame.image.load('SpaceShip.png')
pygame.display.set_icon(logo)

# Spaceship Image
spaceship = pygame.image.load('shooter.png')
spaceshipX = 370
spaceshipY = 515
changeX = 0

# Enemy Image
enemyImg = []
enemyX = []
enemyY = []
enemy_changeX = []
enemy_changeY = []
numberOfEnemies = 8
for i in range(numberOfEnemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemy_changeX.append(2.5)
    enemy_changeY.append(40)

# Bullete Image
bulleteImg = pygame.image.load('bullet.png')
bulleteX = 0
bulleteY = 570
bullete_changeY = 10
bullete_state = "ready"
# ready-->In this state,no bullete is on the screen
# fire-->The bullete is currently moving

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf',32)

clock = pygame.time.Clock()


def displayScore(x, y, HiScore):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    Hiscore_value = font.render(
        "Highest Score :" + str(HiScore), True, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(Hiscore_value, (520, 10))


def player(x, y):
    # This blit function drawn the image in the screen
    screen.blit(spaceship, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullete(x, y):
    global bullete_state
    bullete_state = "fire"
    screen.blit(bulleteImg, (x + 16, y + 16))


def isCollision(enemyX, enemyY, bulleteX, bulleteY):
    distance = math.sqrt(math.pow(enemyX - bulleteX, 2) +
                         math.pow(enemyY - bulleteY, 2))
    return True if distance < 30 else False


run = True
ok = 0
# Game loop
while run:
    if ok == 0:
        home_screen = pygame.image.load('home1.jpg')
        screen.fill((0, 0, 0))
        screen.blit(home_screen, (0, 0))
        score = font.render("Welcome",
                            True, (255, 255, 255))
        screen.blit(score, (350, 245))
        score = font.render("Press Enter to Play",
                            True, (255, 255, 255))
        screen.blit(score, (265, 285))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ok = 1
        pygame.display.update()
    else:
        if (not os.path.exists("HiScore.txt")):
            with open("HiScore.txt", "w") as file:
                file.write("0")

        with open("HiScore.txt", "r") as file:
            HiScore = file.read()

        # RGB values are passed as the element of the tuple
        screen.fill((0, 0, 0))

        # Background image is drawn
        screen.blit(background, (0, 0))

        # Looping through all the events in the screen
        for event in pygame.event.get():

            # Quits the infinite loop when the cross sign is clicked
            if event.type == pygame.QUIT:
                run = False

            # if keystroke is pressed,this checks whether it's right or left
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    changeX = -4.5
                if (event.key == pygame.K_RIGHT):
                    changeX = 4.5
                if (event.key == pygame.K_SPACE):
                    if (bullete_state == "ready"):
                        bullete_sound = mixer.Sound('laser.wav')
                        bullete_sound.play()
                        # Gets the current x co-ordinate of spaceship
                        bulleteX = spaceshipX
                        fire_bullete(bulleteX, bulleteY)

            # After releasing the keystroke,it stpped updating the value x
            if (event.type == pygame.KEYUP):
                if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    changeX = 0

    # Updating the x co-ordinate value after the event
        spaceshipX += changeX

        # Creating Boundaries for spaceship
        if (spaceshipX <= 0):
            spaceshipX = 0
        # 800-64=736(64px size spaceship image)
        elif (spaceshipX >= 736):
            spaceshipX = 736

        # Enemy Movement
        for i in range(numberOfEnemies):

            # Game Over
            if enemyY[i] > 492:
                for j in range(numberOfEnemies):
                    enemyY[j] = 1000
                spaceshipX = 1000
                g_o = pygame.image.load('game_over.jpg')
                screen.fill((0, 0, 0))
                screen.blit(g_o, (0, 0))

                score = font.render("Press Enter to Play Again",
                                    True, (255, 255, 255))
                screen.blit(score, (210, 430))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            ok = 0
                            
            enemyX[i] += enemy_changeX[i]

            # Creating Boundaries for enemy
            if (enemyX[i] <= 0):
                enemy_changeX[i] = 5
                enemyY[i] += enemy_changeY[i]
            elif (enemyX[i] >= 736):
                enemy_changeX[i] = -5
                enemyY[i] += enemy_changeY[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulleteX, bulleteY)
            if (collision):
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bulleteY = 570
                bullete_state = "ready"
                score_value += 1
                if score_value > int(HiScore):
                    HiScore = score_value
                # Respawn of enemy after being hit by bullete
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)
            with open("HiScore.txt", "w") as file:
                file.write(str(HiScore))
        displayScore(textX, textY, HiScore)

        # Bullete Movement
        if (bulleteY <= 0):
            bulleteY = 480
            bullete_state = "ready"
        if (bullete_state == "fire"):
            fire_bullete(bulleteX, bulleteY)
            bulleteY -= bullete_changeY

        player(spaceshipX, spaceshipY)

        # Updating the display window
        pygame.display.update()
            
pygame.quit()
quit()