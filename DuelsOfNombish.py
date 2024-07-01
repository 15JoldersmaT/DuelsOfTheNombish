import pygame
import sys
import random
import time
import math
import os

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption('Duels of the Nombish')
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PALE_ORANGE = (255, 200, 150)
RED_DUST_COLOR = (255, 69, 0)
PALE_ORANGE_DUST_COLOR = (255, 165, 0)
SAND_DUST_COLOR = (245, 222, 179)
GRAY = (169, 169, 169)
YELLOW = (195, 85, 110)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CACTUS_GREEN = (0, 128, 0)
CACTUS_PINK = (255, 105, 180)
BUSH_BROWN = (139, 69, 19)
LEAF_GREEN = (34, 139, 34)
FIRE_ORANGE = (255, 69, 0)
ROCK_COLOR = (169, 169, 169)
PLANT_COLOR = (34, 139, 34)
Z_COLOR = (163, 155, 36)
WAVE_COLOR = (255, 255, 255)

cat2_image = pygame.image.load('cat2.png')
cat3_image = pygame.image.load('cat3.png')
# Animation variables
animation_timer = 0
current_cat_image = cat2_image

win_counter = 0
# Load images
zan_nri_pistol_image = pygame.image.load('oldNombish.png')
zan_nri_shotgun_image = pygame.image.load('oldNombish.png')  # Placeholder, replace with actual image
min_zchel_pistol_image = pygame.image.load('MinZchel.png')
min_zchel_shotgun_image = pygame.image.load('MinZchel.png')  # Placeholder, replace with actual image
opponent_images = [
    (pygame.image.load('newNombish.png'), 1),
    (pygame.image.load('gatocatstalker.png'), 1),
    (pygame.image.load('gatocatstalker2.png'), 1),
    (pygame.image.load('RDFRanger.png'), 3),  # RDF Ranger appears after 3 wins
    (pygame.image.load('Warden.png'), 5)     # Warden appears after 5 wins
]
background_image = pygame.image.load('nombishnorth.png')
target = pygame.image.load('target.png')

# Scale images and flip opponent images
zan_nri_pistol_image = pygame.transform.scale(zan_nri_pistol_image, (zan_nri_pistol_image.get_width() // 5, zan_nri_pistol_image.get_height() // 5))
zan_nri_shotgun_image = pygame.transform.scale(zan_nri_shotgun_image, (zan_nri_shotgun_image.get_width() // 5, zan_nri_shotgun_image.get_height() // 5))
min_zchel_pistol_image = pygame.transform.scale(min_zchel_pistol_image, (min_zchel_pistol_image.get_width() // 5, min_zchel_pistol_image.get_height() // 5))
min_zchel_shotgun_image = pygame.transform.scale(min_zchel_shotgun_image, (min_zchel_shotgun_image.get_width() // 5, min_zchel_shotgun_image.get_height() // 5))
opponent_images = [(pygame.transform.flip(pygame.transform.scale(img, (img.get_width() // 5, img.get_height() // 5)), True, False), level) for img, level in opponent_images]
pygame.display.set_icon(target)

# Hide the default mouse cursor
pygame.mouse.set_visible(False)

# Font
font_path = "CherryBombOne-Regular.ttf"  # Update with the path to Cherry Bomb One font file
font = pygame.font.Font(font_path, 36)

# Load sound effects
shooting = pygame.mixer.Sound('shootAndy.mp4')
shooting.set_volume(0.5)  # Adjust volume to ensure it does not overwhelm the player

# Game states
SELECT_SCREEN = 0
READY = 1
DRAW = 2
AIM = 3
RESULT = 4
game_state = SELECT_SCREEN

# Player variables
player_ready = False
player_shot = False
player_reaction_time = 0
shooting_window = 3  # Time window to shoot
player_bullets = []
player_max_bullets = 6
player_fired_bullets = 0
player_y = HEIGHT // 2
hit_target = False
player_movement = 0  # To track player movement
player_hit = False  # New flag for player hit
player_bullet_speed = 15  # Player bullet speed
char_skill = 0.5  # Character skill level for aiming line movement
selected_gun = None
selected_character = "Zan Nri"  # Default character
player_image = zan_nri_pistol_image  # Default image

# Opponent variables
opponent_ready = False
opponent_shot = False
opponent_reaction_time = 0
opponent_draw_time = random.uniform(15, 20)  # Slowed down significantly
opponent_bullets = []
opponent_max_bullets = 6
opponent_fired_bullets = 0
opponent_y = HEIGHT // 2
opponent_move_time = time.time()
opponent_move_direction = random.choice([-1, 1])
opponent_accuracy = 0.8  # 80% chance to hit
opponent_fire_delay = 1  # Delay before opponent fires again
opponent_hit_target = False
opponent_hit = False  # New flag for opponent hit
opponent_bullet_speed = 17  # Opponent bullet speed
opponent_shoot_in_clusters = False
opponent_cluster_shots_remaining = 0
current_opponent_image, current_opponent_level = random.choice(opponent_images)
current_opponent_name = ""

# Function to determine opponent name
def set_opponent_name(image):
    global current_opponent_name
    if image == opponent_images[0][0]:
        current_opponent_name = "Time Dancer"
    elif image in (opponent_images[1][0], opponent_images[2][0]):
        current_opponent_name = "Gato-Cat Stalker"
    elif image == opponent_images[3][0]:
        current_opponent_name = "RDF Ranger"
    elif image == opponent_images[4][0]:
        current_opponent_name = "City Warden"

# Function to set opponent ammo based on type
def set_opponent_ammo(image):
    global opponent_max_bullets
    if image == opponent_images[3][0]:  # RDF Ranger
        opponent_max_bullets = 9
    else:
        opponent_max_bullets = 6

# Initial opponent name and ammo setup
set_opponent_name(current_opponent_image)
set_opponent_ammo(current_opponent_image)

# Timing mechanism variables
slider_width = 400
slider_height = 20
slider_x = (WIDTH - slider_width) // 2
slider_y = HEIGHT - 100
highlight_width = 100
highlight_x = (WIDTH - highlight_width) // 2
indicator_x = slider_x
indicator_speed = 12
accurate_shot = False

# Counter for wins
win_counter = 0

# Flag to prevent multiple wins in the same round
win_recorded = False

# Timer variables
draw_start_time = 0

# Movement flags
move_up = False
move_down = False
moving = False

# Aiming line
line_x = WIDTH // 2

# Dust particles
dust_particles = []

# Blood spray particles
blood_particles = []

# Delay timer for blood spray
hit_timer = 0
hit_delay = 1  # 1 second delay after a hit

# Gun mode variables
mode = None  # Starting without a gun mode selected

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def get_player_image():
    if selected_character == "Zan Nri":
        return zan_nri_pistol_image if selected_gun == "pistol" else zan_nri_shotgun_image
    else:
        return min_zchel_pistol_image if selected_gun == "pistol" else min_zchel_shotgun_image

def draw_player(x, y):
    player_rect = player_image.get_rect(center=(x, y))
    screen.blit(player_image, player_rect.topleft)
    return player_rect

def draw_opponent(x, y):
    opponent_rect = current_opponent_image.get_rect(center=(x, y))
    screen.blit(current_opponent_image, opponent_rect.topleft)
    return opponent_rect

def draw_bullet(x, y):
    pygame.draw.circle(screen, BLACK, (int(x), int(y)), 3)  # Draw the bullet

def draw_slider():
    pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.rect(screen, CACTUS_PINK, (highlight_x, slider_y, highlight_width, slider_height))
    pygame.draw.rect(screen, BLACK, (indicator_x, slider_y, 10, slider_height))

# Reset game function should be extended to reset character and gun selection
def reset_game(reset_wins=False):
    global player_ready, opponent_ready, player_shot, opponent_shot, player_reaction_time, opponent_reaction_time
    global opponent_draw_time, draw_start_time, game_state, indicator_x, accurate_shot
    global player_bullets, opponent_bullets, player_fired_bullets, opponent_fired_bullets
    global player_y, opponent_y, hit_target, opponent_hit_target, player_movement, blood_particles, hit_timer
    global player_hit, opponent_hit, win_recorded, current_opponent_image, current_opponent_level
    global character_selected, gun_selected, selected_gun, win_counter, selected_character, player_image

    player_ready = False
    opponent_ready = False
    player_shot = False
    opponent_shot = False
    player_reaction_time = 0
    opponent_reaction_time = 0
    opponent_draw_time = random.uniform(15, 20) - win_counter * 0.3  # Opponent gets slightly faster with each win
    draw_start_time = time.time()
    game_state = READY
    indicator_x = slider_x
    accurate_shot = False
    player_bullets = []
    opponent_bullets = []
    player_fired_bullets = 0
    opponent_fired_bullets = 0
    player_y = HEIGHT // 2
    opponent_y = HEIGHT // 2
    hit_target = False
    opponent_hit_target = False
    player_movement = 0
    blood_particles = []  # Clear blood particles
    hit_timer = 0  # Reset hit timer
    player_hit = False  # Reset player hit flag
    opponent_hit = False  # Reset opponent hit flag
    win_recorded = False  # Reset win recorded flag
    valid_opponents = [img for img in opponent_images if img[1] <= win_counter]
    if valid_opponents:
        current_opponent_image, current_opponent_level = random.choice(valid_opponents)
        set_opponent_name(current_opponent_image)  # Update the opponent name
        set_opponent_ammo(current_opponent_image)  # Update the opponent ammo
    character_selected = False  # Reset character selection
    gun_selected = False  # Reset gun selection
    selected_gun = None  # Reset selected gun
    #selected_character = "Zan Nri"  # Reset selected character
    player_image = get_player_image()  # Update player image
    if reset_wins:
        win_counter = 0  # Reset win counter

def opponent_fire():
    global opponent_shot, opponent_bullets, opponent_fired_bullets, opponent_shoot_in_clusters, opponent_cluster_shots_remaining

    if opponent_fired_bullets < opponent_max_bullets:
        if opponent_shoot_in_clusters:
            if opponent_cluster_shots_remaining > 0:
                opponent_cluster_shots_remaining -= 1
            else:
                opponent_shoot_in_clusters = False
        else:
            if opponent_fired_bullets % 2 == 0:
                opponent_shoot_in_clusters = random.choice([True, False])
                if opponent_shoot_in_clusters:
                    opponent_cluster_shots_remaining = random.randint(1, 3)

        opponent_shot = True
        opponent_fired_bullets += 1
        shooting.play()

        opponent_bullet_x, opponent_bullet_y = WIDTH - 100 - 20, opponent_y + 20  # Start from opponent's adjusted position
        angle = math.atan2(player_y - opponent_bullet_y, 100 - opponent_bullet_x)
        if random.random() < opponent_accuracy:
            opponent_bullet_dx = math.cos(angle) * opponent_bullet_speed
            opponent_bullet_dy = math.sin(angle) * opponent_bullet_speed
        else:
            angle_offset = random.uniform(-0.1, 0.1)
            opponent_bullet_dx = math.cos(angle + angle_offset) * opponent_bullet_speed
            opponent_bullet_dy = math.sin(angle + angle_offset) * opponent_bullet_speed
        opponent_bullets.append((opponent_bullet_x, opponent_bullet_y, opponent_bullet_dx, opponent_bullet_dy))

def bullets_collide(bullet1_x, bullet1_y, bullet2_x, bullet2_y):
    return math.hypot(bullet1_x - bullet2_x, bullet1_y - bullet2_y) < 10

def all_bullets_off_screen():
    for bx, by, _, _ in player_bullets + opponent_bullets:
        if -20 <= bx <= WIDTH + 20 and -20 <= by <= HEIGHT + 20:
            return False
    return True

def remove_off_screen_bullets():
    global player_bullets, opponent_bullets
    player_bullets = [b for b in player_bullets if 50 <= b[0] <= WIDTH - 50 and 50 <= b[1] <= HEIGHT - 50]
    opponent_bullets = [b for b in opponent_bullets if 50 <= b[0] <= WIDTH - 50 and 50 <= b[1] <= HEIGHT - 50]

def create_dust_particles():
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        radius = random.randint(1, 3)
        speed = random.uniform(0.5, 1.5)
        angle = random.uniform(0, 2 * math.pi)
        color = random.choice([RED_DUST_COLOR, PALE_ORANGE_DUST_COLOR])
        dust_particles.append({'x': x, 'y': y, 'radius': radius, 'speed': speed, 'angle': angle, 'color': color})

def draw_dust_particles():
    for particle in dust_particles:
        particle['x'] += particle['speed'] * math.cos(particle['angle'])
        particle['y'] += particle['speed'] * math.sin(particle['angle'])
        if particle['x'] < 0 or particle['x'] > WIDTH or particle['y'] < 0 or particle['y'] > HEIGHT:
            particle['x'] = random.randint(0, WIDTH)
            particle['y'] = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), particle['radius'])

# Initialize dust particles
create_dust_particles()

def draw_wavy_line():
    waviness = player_movement / 5  # Increase waviness with player movement
    points = []
    for y in range(0, HEIGHT, 10):
        offset = math.sin(y * 0.1 + time.time() * 2) * waviness
        points.append((line_x + offset, y))
    pygame.draw.lines(screen, BLACK, False, points, 8)  # Thicker line
    for x, y in points:
        pygame.draw.circle(screen, PALE_ORANGE, (int(x), int(y)), 5)  # Add decorative circles

def create_blood_spray(x, y, direction, num_particles=50):
    for _ in range(num_particles):
        angle = random.uniform(direction - math.pi/4, direction + math.pi/4)
        speed = random.uniform(5, 10)
        blood_particles.append({
            'x': x, 
            'y': y, 
            'dx': math.cos(angle) * speed, 
            'dy': math.sin(angle) * speed, 
            'lifetime': random.uniform(0.5, 1.5), 
            'radius': random.uniform(2, 5)
        })

def draw_blood_particles():
    global blood_particles
    new_blood_particles = []
    for particle in blood_particles:
        particle['x'] += particle['dx']
        particle['y'] += particle['dy']
        particle['dy'] += 0.5  # Add gravity effect
        particle['lifetime'] -= 0.1
        particle['radius'] *= 0.9  # Shrink over time
        if particle['lifetime'] > 0 and particle['radius'] > 0.5:
            pygame.draw.circle(screen, RED, (int(particle['x']), int(particle['y'])), int(particle['radius']))
            new_blood_particles.append(particle)
    blood_particles = new_blood_particles

def draw_aiming_line():
    global line_x
    max_waviness = 25  # Maximum horizontal movement
    if mode == "shotgun":
        max_waviness *= 2  # More erratic for shotgun mode
        line_x = WIDTH // 3  # Move line closer to player in shotgun mode
    else:
        line_x = WIDTH // 2  # Center the line in pistol mode
    
    # Calculate mouse movement speed
    mx, my = pygame.mouse.get_pos()
    mouse_speed = math.sqrt((mx - draw_aiming_line.prev_mouse_x)**2 + (my - draw_aiming_line.prev_mouse_y)**2)
    draw_aiming_line.prev_mouse_x, draw_aiming_line.prev_mouse_y = mx, my

    waviness = max_waviness * (1 - char_skill) * (1 + mouse_speed / 20)  # More skill means less waviness, more mouse speed means more waviness
    thickness = 8 if mode == "pistol" else 16  # Thicker line for shotgun mode
    points = []
    for y in range(0, HEIGHT, 10):
        offset = math.sin(y * 0.1 + time.time() * 5) * waviness
        points.append((line_x + offset, y))
    pygame.draw.lines(screen, BLACK, False, points, thickness)  # Adjust line thickness
    for x, y in points:
        pygame.draw.circle(screen, PALE_ORANGE, (int(x), int(y)), 5)  # Add decorative circles

# Initialize previous mouse position for speed calculation
draw_aiming_line.prev_mouse_x, draw_aiming_line.prev_mouse_y = pygame.mouse.get_pos()

# Selection screen variables
character_selected = False
gun_selected = False

# Font size for main menu
menu_font = pygame.font.Font(font_path, 38)

def draw_selection_screen():
    global menu_font,character_selected, gun_selected, selected_character, player_image,animation_timer
    
    screen.fill(YELLOW)
    draw_text('DUELS OF THE NOMBISH', menu_font, BLACK, screen, WIDTH // 2, HEIGHT // 8)
    menu_font = pygame.font.Font(font_path, 28)

    draw_text('Select Your Character', menu_font, BLACK, screen, WIDTH // 2, HEIGHT // 4)

    zan_nri_rect = zan_nri_pistol_image.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 - 50))
    min_zchel_rect = min_zchel_pistol_image.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 - 50))
    screen.blit(zan_nri_pistol_image, zan_nri_rect.topleft)
    screen.blit(min_zchel_pistol_image, min_zchel_rect.topleft)

    if character_selected:
        if selected_character == "Zan Nri":
            pygame.draw.rect(screen, RED, zan_nri_rect.inflate(20, 20), 4)
        else:
            pygame.draw.rect(screen, RED, min_zchel_rect.inflate(20, 20), 4)

    draw_text('Select Your Gun', menu_font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 100)

    pistol_rect = pygame.Rect(WIDTH // 4 - 100, HEIGHT // 2 + 150, 210, 50)
    shotgun_rect = pygame.Rect(3 * WIDTH // 4 - 100, HEIGHT // 2 + 150, 210, 50)

    pygame.draw.rect(screen, RED if selected_gun == "pistol" else BLACK, pistol_rect, 4)
    draw_text('Gato-Cat Pistol', menu_font, RED if selected_gun == "pistol" else BLACK, screen, pistol_rect.centerx, pistol_rect.centery)

    pygame.draw.rect(screen, RED if selected_gun == "shotgun" else BLACK, shotgun_rect, 4)
    draw_text('Olk Blunderbuss', menu_font, RED if selected_gun == "shotgun" else BLACK, screen, shotgun_rect.centerx, shotgun_rect.centery)

    if character_selected and gun_selected:
        draw_text('Press SPACE to start', menu_font, BLACK, screen, WIDTH // 2, HEIGHT - 50)

    # Draw animated cat
    animation_timer += 1
    if animation_timer % 20 < 10:
        current_cat_image = cat2_image
    else:
        current_cat_image = cat3_image

    screen.blit(current_cat_image, (50, HEIGHT - current_cat_image.get_height() - 50))


    # Draw the custom cursor on the selection screen
    mx, my = pygame.mouse.get_pos()
    pygame.draw.circle(screen, RED, (mx, my), 15, 2)  # Outer red circle
    pygame.draw.circle(screen, RED, (mx, my), 10, 3)  # Inner red circle
    pygame.draw.circle(screen, BLACK, (mx, my), 5)  # Black filled circle

# Game loop
running = True
while running:
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == SELECT_SCREEN:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                zan_nri_rect = zan_nri_pistol_image.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 - 50))
                min_zchel_rect = min_zchel_pistol_image.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 - 50))
                if zan_nri_rect.collidepoint(mx, my):
                    character_selected = True
                    selected_character = "Zan Nri"
                if min_zchel_rect.collidepoint(mx, my):
                    character_selected = True
                    selected_character = "Min Zchel"
                pistol_rect = pygame.Rect(WIDTH // 4 - 100, HEIGHT // 2 + 150, 210, 50)
                shotgun_rect = pygame.Rect(3 * WIDTH // 4 - 100, HEIGHT // 2 + 150, 210, 50)
                if pistol_rect.collidepoint(mx, my):
                    selected_gun = "pistol"
                    gun_selected = True
                if shotgun_rect.collidepoint(mx, my):
                    selected_gun = "shotgun"
                    gun_selected = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and character_selected and gun_selected:
                    mode = selected_gun
                    player_image = get_player_image()
                    reset_game()
                    game_state = READY
        elif game_state in {READY, DRAW, AIM, RESULT}:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not player_hit:
                    move_up = True
                    moving = True
                if event.key == pygame.K_s and not player_hit:
                    move_down = True
                    moving = True
                if event.key == pygame.K_SPACE and game_state == READY:
                    player_ready = True
                    draw_start_time = current_time
                    game_state = DRAW
                if event.key == pygame.K_m:  # Return to main menu
                    pygame.quit()
                    python = sys.executable
                    os.execl(python, python, *sys.argv)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    move_up = False
                if event.key == pygame.K_s:
                    move_down = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == DRAW and not player_shot:
                if indicator_x >= highlight_x and indicator_x <= highlight_x + highlight_width:
                    accurate_shot = True
                else:
                    accurate_shot = False
                game_state = AIM
            elif game_state == AIM and player_fired_bullets < player_max_bullets and not player_hit:
                mx, my = pygame.mouse.get_pos()
                shooting.play()
                if abs(mx - line_x) < 10:  # Check if the click is near the aiming line
                    player_shot = True
                    player_fired_bullets += 1
                    bullet_x, bullet_y = 100 + 20, player_y + 20  # Start from player's adjusted position
                    angle = math.atan2(my - bullet_y, mx - bullet_x)
                    bullet_dx = math.cos(angle) * player_bullet_speed
                    bullet_dy = math.sin(angle) * player_bullet_speed

                    # Adjust accuracy based on timing
                    if not accurate_shot:
                        angle_offset = random.uniform(-0.1, 0.1)
                        bullet_dx = math.cos(angle + angle_offset) * player_bullet_speed
                        bullet_dy = math.sin(angle + angle_offset) * player_bullet_speed

                    player_bullets.append((bullet_x, bullet_y, bullet_dx, bullet_dy))

    # Handle player movement
    if game_state in {READY, DRAW, AIM, RESULT}:
        if move_up and player_y > 150:
            player_y -= 5
            player_movement += 1
        if move_down and player_y < HEIGHT - 50:
            player_y += 5
            player_movement += 1

        # Gradually decrease player movement when not moving
        if not moving and player_movement > 0:
            player_movement -= 2
            if player_movement < 0:
                player_movement = 0

    # Drawing based on game state
    if game_state == SELECT_SCREEN:
        draw_selection_screen()
    else:
        screen.fill(YELLOW)

        # Draw background image above the top boundary line
        screen.blit(background_image, (0, -100))

        # Draw player and opponent
        player_rect = draw_player(100, player_y)
        opponent_rect = draw_opponent(WIDTH - 100, opponent_y)  # Adjusted position

        if game_state == READY:
            draw_text('Ready...', font, BLACK, screen, WIDTH // 2, HEIGHT // 4)
            if current_time - draw_start_time > 2:
                game_state = DRAW
                draw_start_time = current_time
        elif game_state == DRAW:
            draw_text('DRAW!', font, WHITE, screen, WIDTH // 2, HEIGHT // 4)
            draw_slider()
            indicator_x += indicator_speed
            if indicator_x > slider_x + slider_width or indicator_x < slider_x:
                indicator_speed *= -1
        elif game_state == AIM:
            draw_aiming_line()
            draw_text('AIM!', font, WHITE, screen, WIDTH // 2, HEIGHT // 4)

            if not opponent_ready:
                opponent_ready = True
                opponent_reaction_time = current_time - draw_start_time

            # Opponent fires at intervals
            if opponent_ready and current_time - draw_start_time >= opponent_fire_delay and opponent_fired_bullets < opponent_max_bullets and not opponent_hit:
                if opponent_fired_bullets < opponent_max_bullets - 1 or player_fired_bullets == player_max_bullets:
                    opponent_fire()
                    
                draw_start_time = current_time  # Reset fire delay timer

            # Update player bullets
            new_player_bullets = []
            for bx, by, bdx, bdy in player_bullets:
                bx += bdx
                by += bdy
                if 50 <= bx <= WIDTH - 50 and 50 <= by <= HEIGHT - 50:
                    if opponent_rect.collidepoint(bx, by):
                        hit_target = True
                        opponent_hit = True  # Opponent is hit
                        create_blood_spray(bx, by, math.atan2(bdy, bdx))
                        hit_timer = current_time  # Start hit timer
                        break
                    draw_bullet(bx, by)
                    new_player_bullets.append((bx, by, bdx, bdy))
            player_bullets = new_player_bullets

            # Update opponent bullets
            new_opponent_bullets = []
            for bx, by, bdx, bdy in opponent_bullets:
                bx += bdx
                by += bdy
                if 50 <= bx <= WIDTH - 50 and 50 <= by <= HEIGHT - 50:
                    if player_rect.collidepoint(bx, by):
                        opponent_hit_target = True
                        player_hit = True  # Player is hit
                        create_blood_spray(bx, by, math.atan2(bdy, bdx))
                        hit_timer = current_time  # Start hit timer
                        break
                    draw_bullet(bx, by)
                    new_opponent_bullets.append((bx, by, bdx, bdy))
            opponent_bullets = new_opponent_bullets

            # Check if bullets collide
            for pbx, pby, pdx, pdy in player_bullets:
                for obx, oby, odx, ody in opponent_bullets:
                    if bullets_collide(pbx, pby, obx, oby):
                        try:
                            player_bullets.remove((pbx, pby, pdx, pdy))
                            opponent_bullets.remove((obx, oby, odx, ody))
                        except ValueError:
                            pass

            remove_off_screen_bullets()

            if (hit_target or opponent_hit_target) or (player_fired_bullets >= player_max_bullets and opponent_fired_bullets >= opponent_max_bullets and all_bullets_off_screen()):
                game_state = RESULT

        elif game_state == RESULT:
            draw_blood_particles()  # Continue drawing blood particles during the result state
            
            if hit_target and not opponent_hit_target:
                draw_text('Player Wins!', font, GREEN, screen, WIDTH // 2, HEIGHT // 2)
                if not win_recorded:
                    win_counter += 1
                    win_recorded = True
                
            elif opponent_hit_target and not hit_target:
                draw_text('Opponent Wins!', font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
                win_counter = 0
            elif hit_target and opponent_hit_target:
                draw_text('It\'s a Draw!', font, YELLOW, screen, WIDTH // 2, 3 * HEIGHT // 4)
            
            # Delay before restarting the game to allow blood particles to continue
            if current_time - hit_timer > hit_delay:
                reset_game()

        # Opponent random up and down movement
        if not opponent_hit:
            if current_time - opponent_move_time > 1:
                opponent_move_time = current_time
                opponent_move_direction = random.choice([-1, 1])
            opponent_y += opponent_move_direction * 2
            if opponent_y < 150 or opponent_y > HEIGHT - 50:
                opponent_move_direction *= -1

        # Draw win counter and bullet counter (Move these to be drawn last)
        draw_text(f'Wins: {win_counter}', font, BLACK, screen, WIDTH // 4, 100)
        draw_text(f'Shots: {player_fired_bullets}/{player_max_bullets}', font, BLACK, screen, 3 * WIDTH // 4, 100)

        # Draw dust particles
        draw_dust_particles()
        
        # Draw blood particles
        draw_blood_particles()

        # Draw the custom cursor (two thick red circles with a black filled circle in the middle)
        mx, my = pygame.mouse.get_pos()
        pygame.draw.circle(screen, RED, (mx, my), 15, 2)  # Outer red circle
        pygame.draw.circle(screen, RED, (mx, my), 10, 3)  # Inner red circle
        pygame.draw.circle(screen, BLACK, (mx, my), 5)  # Black filled circle
        font = pygame.font.Font(font_path, 20)

        # Display opponent name
        draw_text(f'Opponent: {current_opponent_name}', font, BLACK, screen, WIDTH - 150, HEIGHT - 30)
        gunS = 'Pistol'
        if mode == 'pistol':
            gunsS = 'Gato-Cat Pistol'
        else:
            gunsS = 'Olk Blunderbuss'
        font = pygame.font.Font(font_path, 36)

        draw_text(f' {gunsS}', font, BLACK, screen, 140, HEIGHT - 30)


    pygame.display.update()
    clock.tick(60)  # Cap the frame rate to 60 FPS
