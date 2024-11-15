import pygame
import random

pygame.init()

WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BUTTON_COLOR = (50, 50, 50)
HIGHLIGHT_COLOR = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

SNAKE_SIZE = 10
FONT = pygame.font.SysFont("Comic Sans MS", 30)
LEVEL_FONT = pygame.font.SysFont("Comic Sans MS", 50)
BUTTON_FONT = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
GAME_OVER_FONT = pygame.font.SysFont("Comic Sans MS", 70)

pygame.mixer.init()
eat_sound = pygame.mixer.Sound("eat_sound.mp3")
game_over_sound = pygame.mixer.Sound("game_over_sound.wav")

def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], SNAKE_SIZE, SNAKE_SIZE))

def draw_score(score):
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_level(level):
    level_text = FONT.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (WIDTH - 120, 10))

def draw_gradient_background():
    for y_pos in range(HEIGHT):
        color = (0, 0, int(y_pos / HEIGHT * 255))
        pygame.draw.line(screen, color, (0, y_pos), (WIDTH, y_pos))

def game_over_screen(score):
    game_over_text = GAME_OVER_FONT.render("GAME OVER", True, RED)
    score_text = FONT.render(f"Your Score: {score}", True, WHITE)
    
    restart_button = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 50, 200, 50)
    restart_button_text = BUTTON_FONT.render("Restart", True, TEXT_COLOR)
    
    exit_button = pygame.Rect(WIDTH // 3, HEIGHT // 2 + 120, 200, 50)
    exit_button_text = BUTTON_FONT.render("Exit", True, TEXT_COLOR)

    screen.fill(BLACK)
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    if restart_button.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, restart_button)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, restart_button)
    screen.blit(restart_button_text, (restart_button.centerx - restart_button_text.get_width() // 2, restart_button.centery - restart_button_text.get_height() // 2))

    if exit_button.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, exit_button)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, exit_button)
    screen.blit(exit_button_text, (exit_button.centerx - exit_button_text.get_width() // 2, exit_button.centery - exit_button_text.get_height() // 2))

    pygame.display.flip()

    waiting_for_restart_or_exit = True
    while waiting_for_restart_or_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    waiting_for_restart_or_exit = False
                    return "restart"
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()

def draw_food(x, y):
    pygame.draw.circle(screen, YELLOW, (x + SNAKE_SIZE // 2, y + SNAKE_SIZE // 2), SNAKE_SIZE // 2)

def display_level_up(level):
    level_up_text = LEVEL_FONT.render(f"Level {level}!", True, RED)
    screen.blit(level_up_text, (WIDTH // 2 - level_up_text.get_width() // 2, HEIGHT // 3))
    pygame.display.flip()
    pygame.time.wait(1000)  # Wait for 1 second to display the level up message

def main():
    x = WIDTH // 2
    y = HEIGHT // 2
    dx = SNAKE_SIZE
    dy = 0
    snake_body = [(x, y)]
    food_x, food_y = random.randrange(0, WIDTH, SNAKE_SIZE), random.randrange(0, HEIGHT, SNAKE_SIZE)
    score = 0
    level = 1
    speed = 15

    running = True
    while running:
        draw_gradient_background()

        draw_score(score)
        draw_level(level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -SNAKE_SIZE
                if event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, SNAKE_SIZE
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -SNAKE_SIZE, 0
                if event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = SNAKE_SIZE, 0

        x += dx
        y += dy
        snake_body.insert(0, (x, y))

        if (x, y) == (food_x, food_y):
            score += 1
            food_x, food_y = random.randrange(0, WIDTH, SNAKE_SIZE), random.randrange(0, HEIGHT, SNAKE_SIZE)
            eat_sound.play()
            if score % 5 == 0:
                level += 1
                speed += 2
                display_level_up(level)  # Show "Level Up" message when level changes
        else:
            snake_body.pop()

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or (x, y) in snake_body[1:]:
            game_over_sound.play()
            result = game_over_screen(score)
            if result == "restart":
                main()
            running = False

        draw_snake(snake_body)
        draw_food(food_x, food_y)

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()

if __name__ == "__main__":
    main()
