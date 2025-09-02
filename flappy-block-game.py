import pygame
import random
import time

# إعداد اللعبة
pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()

# تحميل الصور
player_image = pygame.image.load("player.png")  # صورة اللاعب العادية
player_image = pygame.transform.scale(player_image, (50, 50))  # تكبير حجم الصورة

game_over_image = pygame.image.load("game_over_player.png")  # صورة عند الخسارة
game_over_image = pygame.transform.scale(game_over_image, (70, 70))  # تكبير حجم الصورة

# ألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# اللاعب
player = pygame.Rect(50, 300, 50, 50)
player_speed = 0
gravity = 1
jump_power = -10
max_fall_speed = 10

# الحواجز
obstacles = []
obstacle_speed = 5
obstacle_frequency = 1500  # كل 1.5 ثانية
last_obstacle = pygame.time.get_ticks() - obstacle_frequency

# النقاط
score = 0
high_score = 0  # إضافة متغير أعلى نتيجة
font = pygame.font.Font(None, 50)

def draw_text(text, x, y, color=BLACK):
    render = font.render(text, True, color)
    text_rect = render.get_rect(center=(200, y))
    screen.blit(render, text_rect)

def reset_game():
    global player, player_speed, obstacles, score, obstacle_speed, obstacle_frequency, last_obstacle, high_score
    if score > high_score:
        high_score = score  # تحديث أعلى نتيجة إذا كانت النتيجة الحالية أعلى
    player = pygame.Rect(50, 300, 50, 50)
    player_speed = 0
    obstacles.clear()
    score = 0
    obstacle_speed = 5
    obstacle_frequency = 1500
    last_obstacle = pygame.time.get_ticks() - obstacle_frequency

# مؤقت البداية
start_time = time.time()
while time.time() - start_time < 3:
    screen.fill(WHITE)
    draw_text(str(3 - int(time.time() - start_time)), 200, 300)
    pygame.display.flip()

# اللعبة
running = True
game_over = False
collision_time = None
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player_speed = jump_power
            if event.key == pygame.K_r and game_over:
                reset_game()
                game_over = False

    if not game_over:
        player_speed = min(player_speed + gravity, max_fall_speed)
        player.y += player_speed

        obstacle_speed = min(obstacle_speed + 0.0005, 10)
        obstacle_frequency = max(800, obstacle_frequency - 0.05)

        now = pygame.time.get_ticks()
        if now - last_obstacle > obstacle_frequency:
            obstacle_height = random.randint(150, 450)
            gap_size = max(120, 200 - int(score / 2))
            obstacles.append(pygame.Rect(400, obstacle_height - 600, 50, 600))
            obstacles.append(pygame.Rect(400, obstacle_height + gap_size, 50, 600))
            last_obstacle = now

        for obstacle in list(obstacles):
            obstacle.x -= obstacle_speed
            if obstacle.x < -50:
                obstacles.remove(obstacle)
                score += 1

        if player.y > 570 or player.y < 0:
            game_over = True
            collision_time = pygame.time.get_ticks()

        for obstacle in obstacles:
            if player.colliderect(obstacle):
                game_over = True
                collision_time = pygame.time.get_ticks()

    if game_over:
        if collision_time and pygame.time.get_ticks() - collision_time < 1000:
            screen.blit(game_over_image, (player.x, player.y))  # عرض صورة الخسارة
            for obstacle in obstacles:
                pygame.draw.rect(screen, BLACK, obstacle)  # إبقاء الحواجز ظاهرة لثانية
        else:
            screen.fill(WHITE)
            draw_text("GAME OVER", 200, 300, RED)
            draw_text("Press R to Restart", 200, 350, BLACK)
            draw_text(f"High Score: {high_score}", 200, 400, BLACK)
            obstacles.clear()  # حذف الحواجز عند ظهور شاشة الخسارة
    else:
        screen.blit(player_image, (player.x, player.y))  # استبدال الدائرة بالصورة العادية أثناء اللعب
        for obstacle in obstacles:
            pygame.draw.rect(screen, BLACK, obstacle)
    
    draw_text(f"Score: {score}", 200, 50)
    draw_text(f"High Score: {high_score}", 200, 90)  # عرض أعلى نتيجة

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
