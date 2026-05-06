import pygame
from random import randint

class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy sprite with randomized appearance and patrolling behavior[cite: 2].
    """
    def __init__(self, x, y):
        super().__init__()
        # Load a random enemy variant[cite: 2]
        self.image = pygame.image.load(f'Grafika/Neprijatelj{randint(1, 5)}.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
        self.direction = 1
        self.move_counter = 0
    
    def move(self):
        """Updates the enemy's horizontal position[cite: 2]."""
        self.rect.x += self.direction
        self.move_counter += 1

        if abs(self.move_counter) > 70:
            self.direction *= -1
            self.move_counter *= self.direction
    
    def update(self):
        """Executes frame-by-frame updates[cite: 2]."""
        self.move()