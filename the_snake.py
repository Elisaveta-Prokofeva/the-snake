from random import choice, randint

import pygame

# --- Константы ---
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

SCREEN_CENTER = (
    GRID_WIDTH // 2 * GRID_SIZE,
    GRID_HEIGHT // 2 * GRID_SIZE,
)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20


pygame.init()

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(
        self,
        body_color=BOARD_BACKGROUND_COLOR,
        position=SCREEN_CENTER,
    ):
        """Инициализирует игровой объект."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает игровой объект."""
        pass


class Apple(GameObject):
    """Представляет яблоко на игровом поле."""

    def __init__(self):
        """Создаёт яблоко."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Перемещает яблоко в случайную клетку поля."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE),
        )

        pygame.draw.rect(
            screen,
            self.body_color,
            rect,
        )

        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            rect,
            1,
        )


class Snake(GameObject):
    """Представляет змейку."""

    def __init__(self):
        """Создаёт змейку длиной в один сегмент."""
        super().__init__(body_color=SNAKE_COLOR)

        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Применяет новое направление движения."""
        if self.next_direction is None:
            return

        if (
            self.next_direction == UP
            and self.direction != DOWN
        ):
            self.direction = UP

        elif (
            self.next_direction == DOWN
            and self.direction != UP
        ):
            self.direction = DOWN

        elif (
            self.next_direction == LEFT
            and self.direction != RIGHT
        ):
            self.direction = LEFT

        elif (
            self.next_direction == RIGHT
            and self.direction != LEFT
        ):
            self.direction = RIGHT

        self.next_direction = None

    def move(self):
        """Перемещает змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)
        self.last = None

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice(
            [UP, DOWN, LEFT, RIGHT]
        )
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовывает змейку."""
        for position in self.positions:
            rect = pygame.Rect(
                position,
                (GRID_SIZE, GRID_SIZE),
            )

            pygame.draw.rect(
                screen,
                self.body_color,
                rect,
            )

            pygame.draw.rect(
                screen,
                BORDER_COLOR,
                rect,
                1,
            )

        if self.last is not None:
            rect = pygame.Rect(
                self.last,
                (GRID_SIZE, GRID_SIZE),
            )

            pygame.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                rect,
            )


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            return True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                snake.next_direction = UP

            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN

            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT

            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT

    return False


def main():
    """Запускает игру."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        if handle_keys(snake):
            break

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        head = snake.get_head_position()

        if head in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
