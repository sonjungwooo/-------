import pygame
import random
from datetime import datetime, timedelta

pygame.init()

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

size = [400,400]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}

def draw_block(screen, color, position):
    block = pygame.Rect(
        (position[1] * 20, position[0] * 20),
        (20, 20)
    )
    pygame.draw.rect(screen, color, block)

def draw_score(score):
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Score : {score}", True, BLACK)
    screen.blit(text, (10, 10))

def draw_game_over(score):
    font_big = pygame.font.SysFont(None, 50)
    font_mid = pygame.font.SysFont(None, 32)

    over = font_big.render("GAME OVER", True, RED)
    score_text = font_mid.render(f"Score : {score}", True, BLACK)

    screen.blit(over, (80, 160))
    screen.blit(score_text, (130, 220))

class Snake:
    def __init__(self):
        self.positions = [(0,2),(0,1),(0,0)]
        self.direction = None

    def draw(self):
        for position in self.positions:
            draw_block(screen, GREEN, position)

    def move(self):
        if self.direction is None:
            return

        y, x = self.positions[0]

        if self.direction == 'N':
            new_head = (y - 1, x)
        elif self.direction == 'S':
            new_head = (y + 1, x)
        elif self.direction == 'W':
            new_head = (y, x - 1)
        elif self.direction == 'E':
            new_head = (y, x + 1)

        self.positions = [new_head] + self.positions[:-1]

    def grow(self):
        self.positions.append(self.positions[-1])

class Apple:
    def __init__(self):
        self.position = (
            random.randint(0, 19),
            random.randint(0, 19)
        )

    def draw(self):
        draw_block(screen, RED, self.position)

def runGame():
    snake = Snake()
    apple = Apple()
    score = 0
    last_moved_time = datetime.now()
    game_over = False

    while True:
        clock.tick(60)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

        if not game_over and datetime.now() - last_moved_time >= timedelta(seconds=0.12):
            snake.move()
            last_moved_time = datetime.now()

            y, x = snake.positions[0]

            # 벽 충돌
            if y < 0 or y >= 20 or x < 0 or x >= 20:
                game_over = True

            # 자기 몸 충돌
            elif snake.positions[0] in snake.positions[1:]:
                game_over = True

            # 사과
            elif snake.positions[0] == apple.position:
                snake.grow()
                apple = Apple()
                score += 1

        snake.draw()
        apple.draw()
        draw_score(score)

        if game_over:
            draw_game_over(score)

        pygame.display.update()

runGame()
pygame.quit()
