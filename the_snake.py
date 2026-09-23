from random import choice

import pygame as pg

# --- Константы ---
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

ALL_CELLS = set(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
)

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

DIRECTION_KEYS = {
    (UP, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_DOWN): DOWN,
    (DOWN, pg.K_LEFT): LEFT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (LEFT, pg.K_LEFT): LEFT,
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_RIGHT): RIGHT,
}

pg.init()

screen = pg.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
pg.display.set_caption('Змейка')

clock = pg.time.Clock()


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

    def draw_cell(self, position, color=None):
        """Отрисовывает одну клетку."""
        color = color or self.body_color

        rect = pg.Rect(
            position,
            (GRID_SIZE, GRID_SIZE),
        )

        pg.draw.rect(
            screen,
            color,
            rect,
        )

        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(
                screen,
                BORDER_COLOR,
                rect,
                1,
            )

    def draw(self):
        """Отрисовывает игровой объект."""
        raise NotImplementedError(
            'Метод draw() должен быть реализован '
            'в дочернем классе.'
        )


class Apple(GameObject):
    """Представляет яблоко на игровом поле."""

    def __init__(
        self,
        body_color=APPLE_COLOR,
        position=SCREEN_CENTER,
        occupied_positions=None,
    ):
        """Создаёт яблоко."""
        super().__init__(
            body_color=body_color,
            position=position,
        )
        self.randomize_position(
            occupied_positions or []
        )

    def randomize_position(self, occupied_positions):
        """Перемещает яблоко в случайную свободную клетку."""
        free_positions = (
            ALL_CELLS - set(occupied_positions)
        )
        self.position = choice(
            tuple(free_positions)
        )

    def draw(self):
        """Отрисовывает яблоко."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Представляет змейку."""

    def __init__(
        self,
        body_color=SNAKE_COLOR,
        position=SCREEN_CENTER,
    ):
        """Создаёт змейку длиной в один сегмент."""
        super().__init__(
            body_color=body_color,
            position=position,
        )
        self.reset()
        self.direction = RIGHT

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self, direction):
        """Меняет направление движения змейки."""
        self.direction = direction

    def move(self):
        """Перемещает змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)
        self.last = self.positions.pop()

    def grow(self):
        """Увеличивает змейку на один сегмент."""
        if self.last is not None:
            self.positions.append(self.last)
            self.last = None

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.positions = [self.position]
        self.direction = choice(
            [UP, DOWN, LEFT, RIGHT]
        )
        self.last = None

    def draw(self):
        """Отрисовывает змейку."""
        if self.last is not None:
            self.draw_cell(
                self.last,
                BOARD_BACKGROUND_COLOR,
            )

        self.draw_cell(
            self.get_head_position()
        )


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return True

            new_direction = DIRECTION_KEYS.get(
                (snake.direction, event.key),
                snake.direction,
            )
            snake.update_direction(new_direction)

    return False


def main():
    """Запускает игру."""
    snake = Snake()

    apple = Apple(
        occupied_positions=snake.positions
    )

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        if handle_keys(snake):
            break

        snake.move()

        head = snake.get_head_position()

        if head == apple.position:
            snake.grow()
            apple.randomize_position(
                snake.positions
            )

        elif head in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(
                snake.positions
            )
            screen.fill(
                BOARD_BACKGROUND_COLOR
            )

        snake.draw()
        apple.draw()

        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    main()
