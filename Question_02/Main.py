import pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load and scale the floor tile
floor_tile = pygame.image.load("C:\\Users\\pgash\\Desktop\\CDU STUDY\\SEM 01\\Softwear Now\\Asigment 02\\Assignment_3\\Question_02\\assets\\backgrounds\\Floor_01.png").convert_alpha()
tile_width = floor_tile.get_width()
tile_height = floor_tile.get_height()

# Ground position (Y-axis)
ground_y = 552  # adjust depending on tile height and player standing height



# Load idle sprite sheet
idle_sheet = pygame.image.load("C:\\Users\\pgash\\Desktop\\CDU STUDY\\SEM 01\\Softwear Now\\Asigment 02\\Assignment_3\\Question_02\\assets\\player\\idle_sheet.png").convert_alpha()

FRAME_WIDTH = 80 # Width of each frame in the sprite sheet
FRAME_HEIGHT = 80 # Height of each frame in the sprite sheet
SCALE_FACTOR = 1.5 # Scale factor for the frames
NUM_FRAMES = 18  # ← This is what was missing!

idle_frames = []
for i in range(NUM_FRAMES):
    frame = idle_sheet.subsurface(pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
    scaled_frame = pygame.transform.scale(
        frame,
        (int(FRAME_WIDTH * SCALE_FACTOR), int(FRAME_HEIGHT * SCALE_FACTOR))
    )
    idle_frames.append(scaled_frame)


# Player class
class Player:
    def __init__(self):
        self.frames = idle_frames # Use the idle frames for animation
        self.current_frame = 0 
        self.animation_timer = 0 
        self.animation_speed = 100  # milliseconds
        self.image = self.frames[0] # Start with the first frame
        self.rect = self.image.get_rect(topleft=(100, 490)) # Adjusted Y position for standing height
        self.vel_y = 0 # Vertical velocity for jumping
        self.health = 100 # Player health
        self.lives = 3  # Player lives
        self.score = 0 # Player score
        self.on_ground = True   # Flag to check if player is on the ground

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.y >= 500:
            self.rect.y = 500
            self.vel_y = 0
            self.on_ground = True

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.animation_timer = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Create player
player = Player()

# Main loop
running = True
while running:
    dt = clock.tick(60)  # Time passed in milliseconds
    screen.fill((50, 200, 255))
    
    # Draw repeated floor tiles across screen width
    for x in range(0, 800, tile_width):
        screen.blit(floor_tile, (x, ground_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.apply_gravity()
    player.update_animation(dt)
    player.draw(screen)

    pygame.display.flip()

pygame.quit()
