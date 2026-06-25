import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Bird
bird_x = 100
bird_y = HEIGHT // 2
bird_radius = 20
bird_velocity = 0
gravity = 0.5
jump_strength = -8

# Pipes
pipe_width = 70
pipe_gap = 180
pipe_speed = 4
pipes = []

score = 0


def create_pipe():
    height = random.randint(100, 500)
    return {
        "x": WIDTH,
        "top": height,
        "bottom": height + pipe_gap
    }


pipes.append(create_pipe())


def draw_bird():
    pygame.draw.circle(screen, YELLOW, (bird_x, int(bird_y)), bird_radius)


def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(
            screen,
            GREEN,
            (pipe["x"], 0, pipe_width, pipe["top"])
        )

        pygame.draw.rect(
            screen,
            GREEN,
            (
                pipe["x"],
                pipe["bottom"],
                pipe_width,
                HEIGHT - pipe["bottom"]
            )
        )


def check_collision():
    global bird_y

    if bird_y <= 0 or bird_y >= HEIGHT:
        return True

    bird_rect = pygame.Rect(
        bird_x - bird_radius,
        bird_y - bird_radius,
        bird_radius * 2,
        bird_radius * 2
    )

    for pipe in pipes:
        top_rect = pygame.Rect(
            pipe["x"],
            0,
            pipe_width,
            pipe["top"]
        )

        bottom_rect = pygame.Rect(
            pipe["x"],
            pipe["bottom"],
            pipe_width,
            HEIGHT - pipe["bottom"]
        )

        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True

    return False


running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

    # Bird physics
    bird_velocity += gravity
    bird_y += bird_velocity

    # Move pipes
    for pipe in pipes:
        pipe["x"] -= pipe_speed

    # Add new pipes
    if pipes[-1]["x"] < 250:
        pipes.append(create_pipe())

    # Remove old pipes
    if pipes[0]["x"] < -pipe_width:
        pipes.pop(0)
        score += 1

    # Collision
    if check_collision():

        game_over_text = font.render(
            f"Game Over! Score: {score}",
            True,
            BLACK
        )

        screen.fill(WHITE)
        screen.blit(
            game_over_text,
            (
                WIDTH // 2 - game_over_text.get_width() // 2,
                HEIGHT // 2
            )
        )

        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    # Draw everything
    screen.fill(BLUE)

    draw_bird()
    draw_pipes()

    score_text = font.render(
        f"Score: {score}",
        True,
        BLACK
    )

    screen.blit(score_text, (20, 20))

    pygame.display.update()

pygame.quit()
sys.exit()