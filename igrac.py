import pygame
from laseri import PlayerLaser

class Player(pygame.sprite.Sprite):
    """
    Handles player input, movement, and health bar rendering[cite: 3].
    """
    SCREEN_WIDTH = 600
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    def __init__(self, x, y, speed, health):
        super().__init__()
        self.image = pygame.image.load('Grafika/Igrac.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
        self.speed = speed
        self.max_health = health
        self.current_health = health
        
        self.shoot_time = pygame.time.get_ticks()
        self.laser_sound = pygame.mixer.Sound('Grafika/laser.wav')
        self.laser_sound.set_volume(0.2)

        self.laser_group = pygame.sprite.Group()
  
    def move(self):
        """Moves player based on arrow key inputs[cite: 3]."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < self.SCREEN_WIDTH:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

    def shoot(self):
        """Creates a player laser with cooldown management[cite: 3]."""
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        cooldown = 600 # ms

        if keys[pygame.K_SPACE] and (current_time - self.shoot_time) > cooldown:
            laser = PlayerLaser(self.rect.centerx, self.rect.top, 5)
            self.laser_group.add(laser)
            self.shoot_time = current_time
            self.laser_sound.play()

    def draw_health_bar(self, screen):
        """Draws a visual health indicator below the player."""
        # Red background (base of the bar)
        pygame.draw.rect(screen, self.RED, (self.rect.x, self.rect.bottom + 10, self.rect.width, 15))
        
        if self.current_health > 0:
            # Green foreground (current health)
            health_width = self.rect.width * (self.current_health / self.max_health)
            pygame.draw.rect(screen, self.GREEN, (self.rect.x, self.rect.bottom + 10, health_width, 15))
            
    def update(self):
        """Updates player and child laser sprites[cite: 3]."""
        self.move()
        self.shoot()
        self.laser_group.update()