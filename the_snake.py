from random import randint, choice
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


class GameObject:
    def __init__(self, position=(0, 0), body_color=None):
        self.position = position
        self.body_color = body_color or BOARD_BACKGROUND_COLOR

    def draw(self, surface):
        raise NotImplementedError(
            "Метод draw() должен быть реализован в дочернем классе"
        )


class Apple(GameObject):
    def __init__(self, snake_positions=None):
        super().__init__(body_color=APPLE_COLOR)
        self.snake_positions = snake_positions or []
        self.position = self.randomize_position()

    def randomize_position(self):
        all_positions = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        ]

        available_positions = [
            pos for pos in all_positions if pos not in self.snake_positions
        ]

        if not available_positions:
            return (0, 0)

        return choice(available_positions)

    def draw(self, surface):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self):
        position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(position, SNAKE_COLOR)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        if self.next_direction:
            # Запрещаем разворот на 180 градусов
            if (
                self.next_direction[0] + self.direction[0],
                self.next_direction[1] + self.direction[1],
            ) != (0, 0):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction

        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        self.positions.insert(0, new_position)
        self.last = self.positions.pop()
        self.position = new_position

    def grow(self):
        self.length += 1
        if self.last:
            self.positions.append(self.last)

    def draw(self, surface):
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.position = position
        self.last = None


def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    score = 0
    game_over = False
    font = pygame.font.SysFont(None, 36)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if not game_over:
            snake.update_direction()
            snake.move()

            if snake.get_head_position() == apple.position:
                snake.grow()
                apple = Apple(snake.positions)
                score += 1

            if snake.get_head_position() in snake.positions[1:]:
                snake.reset()

            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.draw(screen)
            apple.draw(screen)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                game_over = True
        else:
            screen.fill(BOARD_BACKGROUND_COLOR)
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            restart_text = font.render("Press R to restart", True, (255, 255, 255))

            screen.blit(
                game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20)
            )
            screen.blit(
                restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20)
            )

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                snake.reset()
                apple = Apple()
                score = 0
                game_over = False

        pygame.display.update()


if __name__ == "__main__":
    main()
