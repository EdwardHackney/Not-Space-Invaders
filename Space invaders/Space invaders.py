import pygame
import random
import math
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() == 0 :
    print("No joystick connected.")
    joystick = False
else :
    print("Joystick detected.")
    gamepad = pygame.joystick.Joystick(0)
    joystick = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

alienImage = pygame.image.load("Alien.png").convert_alpha()
alien2Image = pygame.image.load("Alien2.png").convert_alpha()
shipImage = pygame.image.load("Ship.png").convert_alpha()
laserImage = pygame.image.load("Laser.png").convert_alpha()

class Alien :
    def __init__(self, pos) :
        self.pos = pos
        self.image = alienImage
        self.speed = 5 #pixels per update
        self.dir = 1   #1 = right and -1 = left
        self.vert_dir = 1
        self.radius = 8
        self.deleted = False

    def update(self) :
        newX = self.pos[0] + self.speed*self.dir
        newY = self.pos[1]
        
        if newX < 0 :
            newX = 0
            self.dir = 1
            newY += 10*self.vert_dir
        if newX > SCREEN_WIDTH - self.image.get_width() - 1 :
            newX = SCREEN_WIDTH - self.image.get_width() - 1
            self.dir = -1
            newY += 10*self.vert_dir
        if newY > SCREEN_HEIGHT - self.image.get_height() :
            self.vert_dir = -1
        if newY < 0 :
            self.vert_dir = 1

        self.pos = (newX, newY)

    def draw(self) :
        screen.blit(self.image, self.pos)

    def get_center(self) :
        x = self.pos[0]
        y = self.pos[1]
        cx = x + self.image.get_width()/2
        cy = y + self.image.get_height()/2
        return (cx, cy)

class Alien2 :
    def __init__(self, pos) :
        self.pos = pos
        self.image = alien2Image
        self.dir = 1
        self.radius = 8
        self.deleted = False
        self.state = "move down"
        self.speed = 5
        self.target_y = random.randint(0, SCREEN_HEIGHT / 2)
        self.last_swoop = time.time()
        self.swoop_delay = random.randint(3, 8)
        self.swoop_center = (0, 0)
        self.swoop_angle = 0
        self.swoop_radius = 0

    def update(self) :
        x_pos = self.pos[0]
        y_pos = self.pos[1]
        
        if self.state == "move down" :
            y_pos += self.speed
            if y_pos >= self.target_y :
                self.state = "move sideways"
                self.last_swoop = time.time()
        elif self.state == "move sideways" :
            x_pos += self.speed*self.dir
            if x_pos > SCREEN_WIDTH - self.image.get_width() :
                self.dir = -1
            if x_pos < 0 :
                self.dir = 1
            if time.time() - self.last_swoop >= self.swoop_delay :
                self.state = "swoop"
                self.swoop_radius = (SCREEN_HEIGHT - 50 - y_pos) / 2
                self.swoop_center = (x_pos, self.swoop_radius + y_pos)
        elif self.state == "swoop" :
            x_pos = self.swoop_radius*math.cos(self.swoop_angle - math.pi/2) + self.swoop_center[0]
            y_pos = self.swoop_radius*math.sin(self.swoop_angle - math.pi/2) + self.swoop_center[1]
            self.swoop_angle += 0.02
            if self.swoop_angle >= 2*math.pi :
                self.state = "move sideways"
                self.last_swoop = time.time()
        self.pos = (x_pos, y_pos)

    def draw(self) :
        screen.blit(self.image, self.pos)

    def get_center(self) :
        x = self.pos[0]
        y = self.pos[1]
        cx = x + self.image.get_width()/2
        cy = y + self.image.get_height()/2
        return (cx, cy)

class Ship :
    def __init__(self) :
        x = SCREEN_WIDTH/2 - shipImage.get_width()/2
        y = SCREEN_HEIGHT - 2*shipImage.get_height()
        self.pos = (x, y)
        self.speed = 4
        self.lives = 3
        self.image = shipImage
        self.radius = 8

    def draw(self) :
        screen.blit(shipImage, self.pos)

    def move_x(self, value) :
        newX = self.pos[0] + self.speed*value
        if newX < 0 :
            newX = 0
        if newX > SCREEN_WIDTH - shipImage.get_width() :
            newX = SCREEN_WIDTH - shipImage.get_width()
        y = self.pos[1]
        self.pos = (newX, y)

    def move_y(self, value) :
        x = self.pos[0]
        newY = self.pos[1] + self.speed*value
        if newY < 0 :
            newY = 0
        if newY > SCREEN_HEIGHT - shipImage.get_height() :
            newY = SCREEN_HEIGHT - shipImage.get_height()
        self.pos = (x, newY)

    def update(self) :
        if joystick :
            x_axis = gamepad.get_axis(0)
            y_axis = gamepad.get_axis(1)
        else :
            x_axis = 0
            y_axis = 0
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_UP]) :
                y_axis = -1
            if (keys[pygame.K_DOWN]) :
                y_axis = 1
            if (keys[pygame.K_RIGHT]) :
                x_axis = 1
            if (keys[pygame.K_LEFT]) :
                x_axis = -1
            
        self.move_x(x_axis)
        self.move_y(y_axis)
        if self.lives == 0 :
            game_over()

    def get_center(self) :
        x = self.pos[0]
        y = self.pos[1]
        cx = x + self.image.get_width()/2
        cy = y + self.image.get_height()/2
        return (cx, cy)

class Laser :
    def __init__(self, pos) :
        self.pos = pos
        self.speed = 6
        self.image = laserImage
        self.deleted = False
        self.radius = 6

    def update(self) :
        x = self.pos[0]
        newY = self.pos[1] - self.speed
        self.pos = (x, newY)
        if newY < 0 - self.image.get_height() :
            self.deleted = True

    def draw(self) :
        screen.blit(self.image, self.pos)

    def get_center(self) :
        x = self.pos[0]
        y = self.pos[1]
        cx = x + self.image.get_width()/2
        cy = y + self.image.get_height()/2
        return (cx, cy)

class Message :
    def __init__(self, text) :
        self.text = text
        self.pos = (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 20)
        self.font = pygame.font.SysFont("Comic Sans MS", 24)
        self.disp = self.font.render(text, False, pygame.Color(255, 255, 255))

    def draw(self) :
        screen.blit(self.disp, self.pos)

class Alien_Spawner :
    def __init__(self) :
        self.delay = 3
        self.last_spawn = time.time()

    def update(self) :
        global aliens
        elapsed = time.time() - self.last_spawn
        if elapsed >= self.delay :
            x = random.randint(0, SCREEN_WIDTH)
            newAlien = Alien2((x, 1))
            aliens.append(newAlien)
            self.last_spawn = time.time()

class Star :
    def __init__(self) :
        self.pos = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.speed = random.randint(2, 8)
        self.radius = random.randint(1, 2)
        self.brightness = random.randint(50, 150)

    def update(self) :
        x_pos = self.pos[0]
        y_pos = self.pos[1]

        y_pos += self.speed

        if y_pos > SCREEN_HEIGHT :
            self.pos = (random.randint(0, SCREEN_WIDTH), 0)
            self.speed = random.randint(2, 10)
            self.radius = random.randint(1, 3)
            self.brightness = random.randint(50, 150)
        else :
            self.pos = (x_pos, y_pos)

    def draw(self) :
        color = pygame.Color(self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, self.pos, self.radius)

def is_colliding(obj1, obj2) :
    center1 = obj1.get_center()
    center2 = obj2.get_center()
    
    dx = center1[0] - center2[0]
    dy = center1[1] - center2[1]
    
    dist = math.sqrt(dx*dx + dy*dy)
    overlapping = dist < obj1.radius + obj2.radius
    return overlapping

def spawn_aliens() :
    for i in range(15) :
        newAlien = Alien((random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT / 2)))
        newAlien.dir = random.choice([-1, 1])
        newAlien.speed = random.randint(2, 5)
        aliens.append(newAlien)

def game_over() :
    global paused
    global message
    paused = True
    message = Message("Game Over!")

def restart() :
    global aliens, lasers, paused, playerShip, message
    playerShip = Ship()
    paused = False
    aliens = []
    lasers = []
    spawn_aliens()
    message = Message("")

running = True
paused = False

font = pygame.font.SysFont("Comic Sans MS", 24)
aliens = []
lasers = []
deleted_lasers = []
deleted_aliens = []
message = Message("")
spawner = Alien_Spawner()

playerShip = Ship()

spawn_aliens()

stars = []
for i in range(50) :
    stars.append(Star())

while running :
    #Handle Event
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        if event.type == pygame.JOYBUTTONDOWN :
            if event.button == 1 :
                newLaser = Laser(playerShip.pos)
                lasers.append(newLaser)
            if event.button == 9 :
                restart()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE :
                newLaser = Laser(playerShip.pos)
                lasers.append(newLaser)
            if event.key == pygame.K_RETURN :
                restart()
            
    #Update entities
    if not paused :
        for alien in aliens :
            alien.update()

        playerShip.update()

        for laser in lasers :
            laser.update()

        spawner.update()

        for star in stars :
            star.update()


    #detect and handle collisions
    for laser in lasers :
        for alien in aliens :
            if is_colliding(laser, alien) :
                laser.deleted = True
                alien.deleted = True

    for alien in aliens :
        if is_colliding(alien, playerShip) :
            playerShip.lives -= 1
            alien.deleted = True

    #remove delted entities
    for laser in lasers :
        if laser.deleted :
            deleted_lasers.append(laser)

    for laser in deleted_lasers :
        lasers.remove(laser)

    deleted_lasers = []

    for alien in aliens :
        if alien.deleted :
            deleted_aliens.append(alien)

    for alien in deleted_aliens :
        aliens.remove(alien)

    deleted_aliens = []
    
    #Clear screen
    screen.fill(pygame.Color(0, 0, 0))

    #Draw entities
    for star in stars :
        star.draw()
    
    for alien in aliens :
        alien.draw()

    playerShip.draw()

    for laser in lasers :
        laser.draw()

    message.draw()

    livesDisplay = font.render("Lives: " + str(playerShip.lives), True, (255, 255, 255))
    screen.blit(livesDisplay, (25, 15))
    
    pygame.display.update()
    pygame.time.delay(10)

    
pygame.quit() 
