import pygame
import sys
from random import choice
from igrac import Player
from laseri import EnemyLaser
from neprijatelj import Enemy

class SpaceInvadersGame:
    """
    Main class to manage game assets, logic, and rendering.
    """
    def __init__(self, screen):
        self.screen = screen
        
        # Player setup
        self.player = Player(300, 750, 6, 5)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        
        # Enemies setup
        self.enemies_group = pygame.sprite.Group()
        self.enemy_lasers_group = pygame.sprite.Group()
        self.last_enemy_shot_time = pygame.time.get_ticks()
        self.enemy_shot_cooldown = 1000  # milliseconds
        self.create_enemies(4, 5)

        # UI setup
        self.main_font = pygame.font.SysFont('Grafika/font1.ttf', 50)
        self.white_color = (255, 255, 255)
        
        # Game state
        self.countdown = 5
        self.last_countdown_update = pygame.time.get_ticks()

        # Sound effects
        self.explosion_sound = pygame.mixer.Sound('Grafika/eksplozija.wav')
        self.explosion_sound.set_volume(0.2)

    def create_enemies(self, rows, cols):
        """Generates a grid of enemy sprites[cite: 1]."""
        for row in range(rows):
            for col in range(cols):
                x = 100 + col * 100
                y = 50 + row * 80
                self.enemies_group.add(Enemy(x, y))
 
    def handle_enemy_shooting(self):
        """Manages enemy AI shooting logic[cite: 1]."""
        current_time = pygame.time.get_ticks()
        if (current_time - self.last_enemy_shot_time > self.enemy_shot_cooldown and 
                len(self.enemy_lasers_group) < 5):
            if self.enemies_group:
                shooter = choice(self.enemies_group.sprites())
                laser = EnemyLaser(shooter.rect.centerx, shooter.rect.bottom)
                self.enemy_lasers_group.add(laser)
                self.last_enemy_shot_time = current_time
                
    def check_collisions(self):
        """Handles all sprite collision logic[cite: 1]."""
        # Player lasers hitting enemies
        if self.player.laser_group:
            for laser in self.player.laser_group: 
                if pygame.sprite.spritecollide(laser, self.enemies_group, True):
                    laser.kill()
                    self.explosion_sound.play()
    
        # Enemy lasers hitting player
        if self.enemy_lasers_group:
            for laser in self.enemy_lasers_group:
                if pygame.sprite.spritecollide(laser, self.player_group, False):
                    laser.kill()
                    self.player.current_health -= 1
                    
    def render_text(self, text, font, color, x, y):
        """Utility method to draw text on screen[cite: 1]."""
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def run(self):
        """Updates and draws game elements[cite: 1]."""
        self.enemies_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.player.laser_group.draw(self.screen)
        self.enemy_lasers_group.draw(self.screen)
        self.player.draw_health_bar(self.screen)

        self.handle_enemy_shooting()
        self.check_collisions()

def main():
    """Main execution loop[cite: 1]."""
    pygame.init()
    screen_width, screen_height = 600, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('SPACE INVADERS')
    
    background = pygame.image.load('Grafika/Svemir.png')
    clock = pygame.time.Clock()
    game = SpaceInvadersGame(screen)

    while True:
        clock.tick(60)
        screen.blit(background, (0, 0))

        if game.countdown > 0:
            game.render_text('GET READY!', game.main_font, game.white_color, 200, 400)
            game.render_text(str(game.countdown), game.main_font, game.white_color, 300, 460)
            
            if pygame.time.get_ticks() - game.last_countdown_update > 1000:
                game.countdown -= 1
                game.last_countdown_update = pygame.time.get_ticks()

        if game.countdown == 0:
            game.player_group.update()
            game.enemies_group.update()
            game.enemy_lasers_group.update()
            
            if not game.enemies_group:
                game.render_text('YOU WIN!', game.main_font, game.white_color, 200, 400)
            elif game.player.current_health <= 0:
                game.player.kill()
                game.render_text('GAME OVER!', game.main_font, game.white_color, 200, 400)

        game.run()
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()

if __name__ == '__main__':
    main()