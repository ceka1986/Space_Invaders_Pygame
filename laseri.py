import pygame

class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load('Grafika/Laser_igraca.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Grafika/Laser_neprijatelja.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 800:
            self.kill()