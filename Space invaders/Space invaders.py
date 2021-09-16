import pygame
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
pygame.joystick.init()
gamepad = pygame.joystick.Joystick(0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

alienSprite = pygame.image.load("Space invaders/Alien.png").convert_alpha()
shipImage = pygame.image.load("Space invaders/Ship.png").convert_alpha()
laserSprite = pygame.image.load("Space invaders/Laser.png").convert_alpha()

class Alien:
    def __init__(self, pos,) :
        self.pos = pos
        self.sprite = alienSprite
        self.speed = 5 #pixels per update
        self.dir = 1 #1 = right and -1 = left
        self.radius = 8
        self.deleted = False

    def update(self):
        newX = self.pos[0] + self.speed*self.dir
        newY = self.pos[1]
        if newX < 0:
            newX = 0
            self.dir = 1
        if newX > SCREEN_WIDTH - self.sprite.get_width() - 1 :
            newX = SCREEN_WIDTH - self.sprite.get_width() - 1
            self.dir = -1
            
        self.pos = (newX, newY)

    def draw(self):
        screen.blit(self.sprite, self.pos)

    def get_center(self):
        x = self.pos[0]
        y = self.pos[1]
        cx = x + self.image.get_width()/2
        cy = y + self.image.get_height()/2
        return (cx, cy)

class Ship:
    def __init__(self):
        self.speed = 5
        global shipImage
        x = SCREEN_WIDTH/2 - shipImage.get_width()/2
        y = SCREEN_HEIGHT - 2*shipImage.get_height()
        self.pos = (x,y)


    def draw(self):
        screen.blit(shipImage, self.pos)

    def move_x(self, value):
        newX = self.pos[0] + self.speed*value
        if newX < 0:
            newX = 0
        if newX > SCREEN_WIDTH - shipImage.get_width():
            newX = SCREEN_WIDTH - shipImage.get_width()
        y = self.pos[1]
        self.pos = (newX, y)

    def move_y(self, value):
        x = self.pos[0]
        newY = self.pos[1] + self.speed*value
        if newY < 0:
            newY = 0
        if newY > SCREEN_HEIGHT - shipImage.get_height():
            newY = SCREEN_HEIGHT - shipImage.get_height()
        self.pos = (x, newY)

    def update(self):
        x_axis = gamepad.get_axis(0)
        y_axis = gamepad.get_axis(1)
        self.move_x(x_axis)
        self.move_y(y_axis)

class Laser:
    def __init__(self, pos):
        self.pos = pos
        self.speed = 6
        self.image = laserSprite
        self.deleted = False
        self.radius = 4

    def update(self):
        x = self.pos[0]
        newY = self.pos[1] - self.speed
        self.pos = (x, newY)
        if newY < 0 - self.image.get_height():
            self.deleted = True

    def draw(self):
        screen.blit(self.image, self.pos)

    def get_center(self):
        x = self.pos[0]
        y = self.pos[1]
        cx = x + self.image.get_width()/2
        cy = y + self.image.get_height()/2
        return (cx, cy)

def is_colliding(obj1, obj2):
    dx = obj1.pos[0] - obj2.pos[0]
    dy = obj1.pos[1] - obj2.pos[1]
    dist = math.sqrt(dx*dx + dy*dy)
    overlapping = dist < obj1.radius + obj2.radius
    return overlapping

running = True

aliens = []
lasers = []
deletedLasers = []
deletedAliens = []

for i in range(15):
    newAlien = Alien((random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT / 2)))
    newAlien.dir = random.choice([-1,1])
    newAlien.speed = random.randint(2, 5)
    aliens.append(newAlien)

playerShip = Ship()

while running:
    #Handle event
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1:
                newLaser = Laser(playerShip.pos)
                lasers.append(newLaser)

    #Update entities
    for alien in aliens:
        alien.update()
    
    playerShip.update()

    for laser in lasers:
        laser.update()

    #detect and handle collisions
    for laser in lasers:
        for alien in aliens:
            if is_colliding(laser, alien):
                laser.deleted = True
                alien.deleted = True

    #delete entities
    for laser in lasers:
        if laser.deleted:
            deletedLasers.append(laser)

    for laser  in deletedLasers:
        lasers.remove(laser)

        deletedLasers = []

    for alien in aliens:
        if alien.deleted:
            deletedAliens.append(alien)

    for alien in deletedAliens:
        aliens.remove(alien)

        deletedAliens = []

    #Clear screen
    screen.fill(pygame.Color(0, 0, 35))
    
    #Draw entities
    for alien in aliens:
        alien.draw()

    playerShip.draw()

    for laser in lasers:
        laser.draw()

    pygame.display.update()
    pygame.time.delay(10)

pygame.quit()
