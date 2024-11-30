import os
import pygame
import random
import math
from pygame import mixer

class SpaceInvaders:
    def __init__(self):
        pygame.init()
        
        # Screen dimensions
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        # Load resources
        self.load_resources()
        
        # Game variables
        self.reset_game()
    
    def load_resources(self):
        # Background
        try:
            self.background = pygame.image.load('background.jpg')
            self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        except pygame.error:
            self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.background.fill(self.BLACK)
        
        # Background Music
        try:
            mixer.init()
            mixer.music.load('background.wav')
            mixer.music.play(-1)
        except pygame.error:
            print("Background music could not be loaded.")
        
        # Title and Icon
        pygame.display.set_caption("Space Invaders")
        try:
            icon = pygame.image.load('spaceship.png')
            pygame.display.set_icon(icon)
        except pygame.error:
            print("Icon image could not be loaded.")
        
        # Fonts
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)
        self.menu_font = pygame.font.Font('freesansbold.ttf', 48)
    
    def reset_game(self):
        # Player
        self.player_img = pygame.image.load('player.png')
        self.player_img = pygame.transform.scale(self.player_img, (64, 64))
        self.player_x = self.WIDTH // 2 - 32
        self.player_y = self.HEIGHT - 100
        self.player_x_change = 0
        
        # Enemy
        self.enemy_img = []
        self.enemy_x = []
        self.enemy_y = []
        self.enemy_x_change = []
        self.enemy_y_change = []
        self.num_of_enemies = 10  # Increased number of enemies
        
        for _ in range(self.num_of_enemies):
            enemy = pygame.image.load('enemy.png')
            enemy = pygame.transform.scale(enemy, (64, 64))
            self.enemy_img.append(enemy)
            self.enemy_x.append(random.randint(0, self.WIDTH - 64))
            self.enemy_y.append(random.randint(50, 150))
            self.enemy_x_change.append(1.5)  # Slower enemy speed
            self.enemy_y_change.append(20)
        
        # Bullet
        self.bullet_img = pygame.image.load('bullet.png')
        self.bullet_img = pygame.transform.scale(self.bullet_img, (32, 32))
        self.bullet_x = 0
        self.bullet_y = self.player_y
        self.bullet_x_change = 0
        self.bullet_y_change = 10
        self.bullet_state = "ready"
        
        # Score and Lives
        self.score_value = 0
        self.player_lives = 3
        self.high_score = self.load_high_score()
        
        # Game state
        self.game_over = False
    
    def load_high_score(self):
        try:
            with open('highscore.txt', 'r') as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0
    
    def save_high_score(self):
        if self.score_value > self.high_score:
            with open('highscore.txt', 'w') as file:
                file.write(str(self.score_value))
    
    def show_menu(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.background, (0, 0))
        
        # Game Title
        title = self.menu_font.render("SPACE INVADERS", True, self.WHITE)
        title_rect = title.get_rect(center=(self.WIDTH//2, self.HEIGHT//4))
        self.screen.blit(title, title_rect)
        
        # Menu Options
        start_text = self.font.render("Press SPACE to Start", True, self.WHITE)
        start_rect = start_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
        self.screen.blit(start_text, start_rect)
        
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, self.WHITE)
        high_score_rect = high_score_text.get_rect(center=(self.WIDTH//2, self.HEIGHT*3//4))
        self.screen.blit(high_score_text, high_score_rect)
        
        pygame.display.update()
        
        # Wait for start
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
        return True
    
    def show_game_over(self):
        # Save high score
        self.save_high_score()
        
        # Game Over screen
        self.screen.fill(self.BLACK)
        self.screen.blit(self.background, (0, 0))
        
        # Game Over Text
        over_text = self.over_font.render("GAME OVER", True, self.WHITE)
        over_rect = over_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//3))
        self.screen.blit(over_text, over_rect)
        
        # Score Display
        score_text = self.font.render(f"Your Score: {self.score_value}", True, self.WHITE)
        score_rect = score_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
        self.screen.blit(score_text, score_rect)
        
        # Options
        replay_text = self.font.render("Press SPACE to Replay", True, self.WHITE)
        replay_rect = replay_text.get_rect(center=(self.WIDTH//2, self.HEIGHT*2//3))
        self.screen.blit(replay_text, replay_rect)
        
        quit_text = self.font.render("Press Q to Quit", True, self.WHITE)
        quit_rect = quit_text.get_rect(center=(self.WIDTH//2, self.HEIGHT*3//4))
        self.screen.blit(quit_text, quit_rect)
        
        pygame.display.update()
        
        # Wait for input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return True
                    if event.key == pygame.K_q:
                        return False
    
    def run(self):
        # Main game loop
        running = True
        
        while running:
            # Show menu before starting game
            if not self.show_menu():
                break
            
            # Reset game state
            self.reset_game()
            
            # Game loop
            while not self.game_over:
                self.screen.fill(self.BLACK)
                self.screen.blit(self.background, (0, 0))
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        self.game_over = True
                        break
                    
                    # Keystroke events
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.player_x_change = -5
                        if event.key == pygame.K_RIGHT:
                            self.player_x_change = 5
                        if event.key == pygame.K_SPACE:
                            if self.bullet_state == "ready":
                                try:
                                    bullet_sound = mixer.Sound('laser.wav')
                                    bullet_sound.play()
                                except pygame.error:
                                    print("Bullet sound could not be loaded.")
                                self.bullet_x = self.player_x
                                self.fire_bullet(self.bullet_x, self.bullet_y)
                    
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self.player_x_change = 0
                
                # Player movement
                self.player_x += self.player_x_change
                if self.player_x <= 0:
                    self.player_x = 0
                elif self.player_x >= self.WIDTH - 64:
                    self.player_x = self.WIDTH - 64
                
                # Enemy movement
                for i in range(self.num_of_enemies):
                    # Game Over condition
                    if self.enemy_y[i] > self.player_y - 40:
                        self.player_lives -= 1
                        if self.player_lives <= 0:
                            for j in range(self.num_of_enemies):
                                self.enemy_y[j] = 2000
                            self.game_over = True
                            break
                        else:
                            # Reset enemy position if player has lives left
                            self.enemy_x[i] = random.randint(0, self.WIDTH - 64)
                            self.enemy_y[i] = random.randint(50, 150)
                    
                    self.enemy_x[i] += self.enemy_x_change[i]
                    if self.enemy_x[i] <= 0:
                        self.enemy_x_change[i] = 1.5
                        self.enemy_y[i] += self.enemy_y_change[i]
                    elif self.enemy_x[i] >= self.WIDTH - 64:
                        self.enemy_x_change[i] = -1.5
                        self.enemy_y[i] += self.enemy_y_change[i]
                    
                    # Collision detection
                    collision = self.is_collision(self.enemy_x[i], self.enemy_y[i], 
                                                  self.bullet_x, self.bullet_y)
                    if collision:
                        try:
                            explosion_sound = mixer.Sound('explosion.wav')
                            explosion_sound.play()
                        except pygame.error:
                            print("Explosion sound could not be loaded.")
                        
                        self.bullet_y = self.player_y
                        self.bullet_state = "ready"
                        self.score_value += 1
                        
                        # Respawn enemy
                        self.enemy_x[i] = random.randint(0, self.WIDTH - 64)
                        self.enemy_y[i] = random.randint(50, 150)
                    
                    self.enemy(self.enemy_x[i], self.enemy_y[i], i)
                
                # Bullet movement
                if self.bullet_state == "fire":
                    self.fire_bullet(self.bullet_x, self.bullet_y)
                    self.bullet_y -= self.bullet_y_change
                if self.bullet_y <= 0:
                    self.bullet_y = self.player_y
                    self.bullet_state = "ready"
                
                self.player(self.player_x, self.player_y)
                self.show_score()
                
                pygame.display.update()
                
                # Check for game over
                if self.game_over:
                    # Show game over screen and ask to replay or quit
                    replay = self.show_game_over()
                    if not replay:
                        running = False
                    break
            
            # End of game loop
        
        # Quit the game
        pygame.quit()
    
    def player(self, x, y):
        self.screen.blit(self.player_img, (x, y))
    
    def enemy(self, x, y, i):
        self.screen.blit(self.enemy_img[i], (x, y))
    
    def fire_bullet(self, x, y):
        self.bullet_state = "fire"
        self.screen.blit(self.bullet_img, (x + 16, y + 10))
    
    def is_collision(self, enemy_x, enemy_y, bullet_x, bullet_y):
        distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
        return distance < 27
    
    def show_score(self):
        # Show score and lives
        score = self.font.render(f"Score: {self.score_value}", True, self.WHITE)
        lives = self.font.render(f"Lives: {self.player_lives}", True, self.WHITE)
        self.screen.blit(score, (10, 10))
        self.screen.blit(lives, (10, 50))

# Run the game
if __name__ == "__main__":
    game = SpaceInvaders()
    game.run()