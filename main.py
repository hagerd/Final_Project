import random
import math
import sys
import pygame
from pygame import mixer

# Inialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((1920, 1080))

# Background
background = pygame.image.load('background.png')

# Background
mixer.music.load('eft.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Tarkov Rat")
icon = pygame.image.load('rat.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 50
playerY = 500
playerY_change = 0

# Enemey
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
enemyX_change = []
num_of_enemies = 6

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(500, 1730))
    enemyY.append(random.randint(0, 880))
    enemyY_change.append(10)
    enemyX_change.append(-100)

# Bullet
# Ready - You cannot see the bullet
# Fire - the bullet fires
bulletImg = pygame.image.load('bullet.png')
bulletX = 50
bulletY = 0
bulletY_change = 0
bulletX_change = 40
bullet_state = "ready"  

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# High score text
high_score_value = 0

highscore_textX = 200
highscore_textY = 10

# Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def read_high_score():
    """Open score_list.txt and return score value."""
    high_score_value = []
    with open("score_list.txt", "r") as score_list:
        for line in score_list:
            high_score_value = line.strip()
            return high_score_value


def show_high_score(x, y):
    """Render high score."""
    high_score_value = read_high_score() 
    high_score = font.render("High Score: " + str(high_score_value), True, (255, 255, 255))
    screen.blit(high_score, (x, y))


def write_high_score(score_value):
    """Write high score to score_list.txt."""
    new_score = []
    with open("score_list.txt", "w") as new_score:
        new_score.write(str(score_value))
        new_score.close()


def show_score(x, y):
    """Render Score."""
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    """Render Game Over and quit."""
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    esc_text = over_font.render("Press Esc to Quit", True, (255, 255, 255))
    screen.blit(over_text, (750, 500))
    screen.blit(esc_text, (680, 600))


def player(x, y):
    """Render Player Sprite."""
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    """Render Enemy sprite."""
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    """Render bullet and it's state."""
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 110, y + 140))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    """Check for bullet collision with enemy."""
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 100:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -10
            if event.key == pygame.K_DOWN: 
                playerY_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('ak.wav')
                    bullet_sound.play()
                    # Current x cordinate of the player
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Check boundries of player
    playerY += playerY_change

    if playerY <= 0:
        playerY = 0
    elif playerY >= 900:
        playerY = 900

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyX[i] < 300:
            for j in range(num_of_enemies):
                enemyX[j] = -500
            game_over_text()
            if score_value > high_score_value:
                write_high_score(score_value)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)

        enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 0:
            enemyY_change[i] = 10
            enemyX[i] += enemyX_change[i]
        elif enemyY[i] >= 850:
            enemyY_change[i] = -10
            enemyX[i] += enemyX_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            cheekibreeki = mixer.Sound('cheekibreeki.wav')
            cheekibreeki.play()            
            bulletX = 50
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(900, 1730)
            enemyY[i] = random.randint(0, 880)


        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletX >= 1920:
        bulletX = 250
        bullet_state = "ready"
        
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletX += bulletX_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_high_score(highscore_textX, highscore_textY)
    pygame.display.update()
