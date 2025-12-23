import pygame
import random

pygame.init() 

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)

screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height)) 

clock = pygame.time.Clock() 

def runGame():
    score = 0
    SUCCESS = 1
    FAILURE = 2
    game_over = 0

    bricks = []
    COLUMN_COUNT = 8
    ROW_COUNT = 7
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            brick = pygame.Rect(
                column_index * (60 + 10) + 35,
                row_index * (16 + 5) + 35,
                60, 16
            )
            bricks.append(brick)

    ball = pygame.Rect(
        screen_width // 2 - 8,
        screen_height // 2 - 8,
        16, 16
    )
    ball_dx = 5
    ball_dy = -5

    paddle = pygame.Rect(
        screen_width // 2 - 40,
        screen_height - 16,
        80, 16
    )

    def increase_ball_speed():
        nonlocal ball_dx, ball_dy
        ball_dx += 1 if ball_dx > 0 else -1
        ball_dy += 1 if ball_dy > 0 else -1

    while True:
        clock.tick(30)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # 패들 이동 (끊김 방지)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.left -= 14
        elif keys[pygame.K_RIGHT]:
            paddle.left += 14

        paddle.left = max(0, min(paddle.left, screen_width - paddle.width))

        if game_over == 0:
            ball.left += ball_dx
            ball.top += ball_dy

            if ball.left <= 0 or ball.left >= screen_width - ball.width:
                ball_dx *= -1
            if ball.top <= 0:
                ball_dy *= -1

            if ball.top >= screen_height:
                game_over = FAILURE

            if ball.colliderect(paddle):
                ball_dy = -ball_dy

            # 벽돌마다 다른 반사
            for brick in bricks:
                if ball.colliderect(brick):
                    offset = (ball.centerx - brick.centerx) / (brick.width / 2)
                    ball_dx += int(offset * 2)
                    ball_dy *= -1

                    bricks.remove(brick)
                    score += 1
                    increase_ball_speed()
                    break

            if len(bricks) == 0:
                game_over = SUCCESS

        for brick in bricks:
            pygame.draw.rect(screen, GREEN, brick)

        if game_over == 0:
            pygame.draw.circle(screen, WHITE, (ball.centerx, ball.centery), 8)

        pygame.draw.rect(screen, BLUE, paddle)

        score_image = small_font.render(f'Point {score}', True, YELLOW)
        screen.blit(score_image, (10, 10))

        if game_over == SUCCESS:
            msg = large_font.render('성공', True, RED)
            screen.blit(msg, msg.get_rect(center=(screen_width//2, screen_height//2)))
        elif game_over == FAILURE:
            msg = large_font.render('게임 오버', True, RED)
            screen.blit(msg, msg.get_rect(center=(screen_width//2, screen_height//2)))

        pygame.display.update()

runGame()
pygame.quit()
