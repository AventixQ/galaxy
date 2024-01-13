import pygame
import random


class Sprite:
    def __init__(self, x, y, width, height, vx, vy):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = vx
        self.vy = vy

    def bounceX(self):
        self.vx = -self.vx

    def bounceY(self):
        self.vy = -self.vy

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def edgeCollision(self, size):
        if self.x < 0 or self.y < 0 or \
                (self.x + self.width) > size[0] or \
                (self.y + self.height) > size[1]:
            return True
        else:
            return False

    def objectCollision(self, object_col):
        A = [self.x, self.x + self.width, self.y, self.y + self.height]
        B = [object_col.x, object_col.x + object_col.width, object_col.y, object_col.y + object_col.height]

        collisionX = 0
        collisionY = 0

        if B[0] < A[0] < B[1]:
            collisionX += 1
        if B[0] < A[1] < B[1]:
            collisionX += 1
        if B[2] < A[2] < B[3]:
            collisionY += 1
        if B[2] < A[3] < B[3]:
            collisionY += 1

        if collisionX >= 1 and collisionY >= 1:
            return True
        else:
            return False


class Player(Sprite):
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0, 0)
        self.costume = pygame.image.load("/home/raspbian/Desktop/galaxy/photos/playerShip1_blue.png")
        self.width = self.costume.get_width()
        self.height = self.costume.get_height()

    def draw(self, screen):
        screen.blit(self.costume, [self.x, self.y])


class Bullet(Sprite):
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0, 0)
        self.costume = pygame.image.load("/home/raspbian/Desktop/galaxy/photos/laserGreen10.png")
        self.width = self.costume.get_width()
        self.height = self.costume.get_height()

    def draw(self, screen):
        screen.blit(self.costume, [self.x, self.y])


class Enemies(Sprite):
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0, 0)
        enemies = ["/home/raspbian/Desktop/galaxy/photos/enemyGreen1.png", "/home/raspbian/Desktop/galaxy/photos/enemyBlue1.png", "/home/raspbian/Desktop/galaxy/photos/enemyRed1.png"]
        self.costume = pygame.image.load(enemies[random.randrange(0, 3)])
        self.width = self.costume.get_width()
        self.height = self.costume.get_height()

    def draw(self, screen):
        screen.blit(self.costume, [self.x, self.y])
