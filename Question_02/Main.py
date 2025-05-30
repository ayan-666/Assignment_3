# Kindly make sure to pull the latest updates from Git 🙏

import os
import pygame
import random


pygame.init()

base = r"C:\Users\pgash\Desktop\CDU STUDY\SEM 01\Softwear Now\Asigment 02\Assignment_3\Question_02\assets"

# ————————————————————— Setup —————————————————————
pygame.display.set_caption("Blade of the Fallen")
SCREEN_W, SCREEN_H = 800, 400
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()

# Ground tile  
floor_tile = pygame.image.load(
    os.path.join(base, "backgrounds", "Floor_01.png")
).convert_alpha()

tile_width  = floor_tile.get_width()
tile_height = floor_tile.get_height()
ground_y    = SCREEN_H - tile_height   # position floor at the bottom



# ————————————————————— Helpers —————————————————————
FRAME_W, FRAME_H = 80, 80
SCALE = 1.5

def load_animation(path, num_frames):
    """Load & slice a horizontal spritesheet into scaled frames."""
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(num_frames):
        rect = pygame.Rect(i * FRAME_W, 0, FRAME_W, FRAME_H)
        frame = sheet.subsurface(rect)
        frame = pygame.transform.scale(frame,
            (int(FRAME_W * SCALE), int(FRAME_H * SCALE))
        )
        frames.append(frame)
    return frames

# ———————————————————— Load Assets ————————————————————

tree_img = pygame.image.load(os.path.join(base, "backgrounds", "Tree_01.png")).convert_alpha()


# ———————————————————— Load Animations ————————————————————

idle_frames   = load_animation(os.path.join(base, "player", "idle_sheet.png"),    18)
run_frames    = load_animation(os.path.join(base, "player", "run_sheet.png"),      8)
jump_frames   = load_animation(os.path.join(base, "player", "jump_sheet.png"),     4)
attack_frames = load_animation(os.path.join(base, "player", "light_atk_sheet.png"), 6)
death_frames   = load_animation(os.path.join(base, "player", "death.png"),     3)

# Load Flying Enemy Animations
flying_base = os.path.join(base, "enemies", "Flying_eye")
flying_fly_frames    = load_animation(os.path.join(flying_base, "Flight.png"), 8)
flying_attack_frames = load_animation(os.path.join(flying_base, "Attack.png"), 2)
flying_death_frames  = load_animation(os.path.join(flying_base, "Death.png"),  2)

# ———————————————————— Player Class ————————————————————
class Player:
    def __init__(self):
        self.max_health = 100 # Player max health
        self.current_health = 100 # Player health
        self.dead = False

        # All animation frame lists already loaded elsewhere
        self.anims = {
            "idle":   idle_frames,
            "run":    run_frames,
            "jump":   jump_frames,
            "attack": attack_frames,
            "death":  death_frames
        }

        # Milliseconds per frame for each state
        self.state_speeds = {
            "idle":   150,
            "run":     40,
            "jump":   100,
            "attack":  80,
            "death":   100
        }

        # Initial state
        self.state = "idle"
        self.speed = self.state_speeds[self.state]
        self.frames = self.anims[self.state]
        self.idx = 0
        self.timer = 0
        

        

        # Starting image and position
        PLAYER_START_X = 100
        PLAYER_START_Y = 520   # ← tweak this value until she sits where you want
        self.image = self.frames[self.idx]
        self.rect = self.image.get_rect(topleft=(PLAYER_START_X, PLAYER_START_Y)

        )


        # Physics
        self.vel_y = 0
        self.on_ground = True

        # Direction
        self.facing_right = True

    def handle_input(self, keys):
        moving = False

        # Left / Right movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            moving = True
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            moving = True
            self.facing_right = True

        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15  # Adjust this value for jump height
            self.on_ground = False
            self.state = "jump"

        # Attack or Hurt
        elif keys[pygame.K_f]:
            self.state = "attack"
            self.frames = self.anims["attack"]
            self.idx = 0
            self.timer = 0

        # Fallback to run or idle
        else:
            if self.state not in ("jump", "attack", "hurt"):
                self.state = "run" if moving else "idle"

        # Update speed & frames for the new state
        self.speed = self.state_speeds[self.state]
        self.frames = self.anims[self.state]
        # ensure current frame index is within new frame list
        self.idx %= len(self.frames)
        
        # Prevent going out of the screen horizontally
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_W:
            self.rect.right = SCREEN_W


    def apply_gravity(self):
        self.vel_y += 1
        self.rect.y += self.vel_y

        # Land on the floor
        if self.rect.bottom >= (ground_y + 45):
            self.rect.bottom = ground_y + 45# Adjust this value to match the floor tile height
            self.vel_y = 0
            self.on_ground = True

            if self.state == "jump":
                self.state = "idle"
                self.speed = self.state_speeds["idle"]
                self.frames = self.anims["idle"]
                self.idx = 0
                

    def update_animation(self, dt):
        self.timer += dt
        if self.timer >= self.speed:
            self.timer = 0
            self.idx += 1

            # If we ran past the last frame...
            if self.idx >= len(self.frames):
                if self.state == "attack" or self.state == "hurt":
                    # go back to idle (or you could pick run based on input)
                    self.state = "idle"
                    self.frames = self.anims["idle"]
                    self.speed = self.state_speeds["idle"]
                    self.idx = 0
                else:
                    # loop normally for idle/run/jump
                    self.idx = 0

            self.image = self.frames[self.idx]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)


    def draw(self, surf):
        surf.blit(self.image, self.rect)
        
    def draw_health_bar(self, surface):
        bar_width = 150
        bar_height = 20
        fill = (self.current_health / self.max_health) * bar_width
        border_rect = pygame.Rect(10, 10, bar_width, bar_height)
        fill_rect = pygame.Rect(10, 10, fill, bar_height)

        pygame.draw.rect(surface, (255, 0, 0), fill_rect)       # Red fill
        pygame.draw.rect(surface, (255, 255, 255), border_rect, 2)  # White border

        
        
        
class FlyingEnemy:
    def __init__(self, x, y, target):
        self.image = pygame.image.load(os.path.join(base, "enemies", "Flying_eye", "Flight2.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.target = target
        self.dead = False
        self.vel_x = -3

    def update(self, dt):
        self.rect.x += self.vel_x

        # Track player vertically
        if self.target.rect.centery > self.rect.centery:
            self.rect.y += 1
        elif self.target.rect.centery < self.rect.centery:
            self.rect.y -= 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_collision_with_player(self):
        return self.rect.colliderect(self.target.rect)

    def hit(self):
        self.dead = True




player = Player()
enemies = []  # List to hold multiple enemies
spawn_timer = 0
spawn_interval = 2000  # Spawn every 2000 milliseconds (2 seconds)
game_over = False

# ————————————————————— Main Loop —————————————————————
running = True

while running:
    dt = clock.tick(60)
    screen.fill((50, 200, 255))
    
    # Example: draw 3 trees at fixed positions
    screen.blit(tree_img, (-150, ground_y - tree_img.get_height()+ 10))  # Off-screen left
    screen.blit(tree_img, (250, ground_y - tree_img.get_height()+ 10))
    screen.blit(tree_img, (600, ground_y - tree_img.get_height()+ 10))

    # Draw floor
    for x in range(0, SCREEN_W, tile_width):
        screen.blit(floor_tile, (x, ground_y))
        
    


    # Event handling
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    
    spawn_timer += dt
    if not player.dead and spawn_timer >= spawn_interval:
        spawn_timer = 0
        spawn_x = SCREEN_W + 50  # Start just off the right edge
        spawn_y = random.randint(50, 200)  # Random vertical position
        enemies.append(FlyingEnemy(spawn_x, spawn_y, player))


    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    player.apply_gravity()
    player.update_animation(dt)
    player.draw(screen)
    player.draw_health_bar(screen)  # Draw health bar

    # Update & draw enemy
    for enemy in enemies[:]:
        enemy.update(dt)
        
        if enemy.check_collision_with_player() and not enemy.dead:
            enemy.hit()
            player.current_health -= 10  # Deal damage
            if player.current_health <= 0:
                player.current_health = 0
                player.dead = True
                player.state = "death"
                player.frames = player.anims["death"]
                player.speed  = player.state_speeds["death"]
                player.idx    = 0
                # Stop further enemy spawns:
                game_over = True

        enemy.draw(screen)

        # Remove enemy if it's off screen or dead + finished anim
        if enemy.rect.right < 0 or enemy.dead:
            enemies.remove(enemy)

    if player.dead:
        # draw Game Over text
        font = pygame.font.SysFont("Arial", 150, bold=True)
        text = font.render("GAME OVER", True, (255,0,0))
        r = text.get_rect(center=(SCREEN_W//2, SCREEN_H//2))
        screen.blit(text, r)

        pygame.display.flip()
        continue  # skips the rest of the loop, no more spawns or movement


    pygame.display.flip()

pygame.quit()
