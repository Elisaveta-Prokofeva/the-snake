from random import choice

import pygame as pg


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
        if color is None:
            color = self.body_color

        rect = pg.Rect(
            position,
            (GRID_SIZE, GRID_SIZE),
        )

        pg.draw.rect(
            screen,
            color,
            rect,
        )

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
        free_positions = [
            (
                x * GRID_SIZE,
                y * GRID_SIZE,
            )
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (
                x * GRID_SIZE,
                y * GRID_SIZE,
            ) not in occupied_positions
        ]

        self.position = choice(free_positions)

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

            elif (
                event.key == pg.K_UP
                and snake.direction != DOWN
            ):
                snake.update_direction(UP)

            elif (
                event.key == pg.K_DOWN
                and snake.direction != UP
            ):
                snake.update_direction(DOWN)

            elif (
                event.key == pg.K_LEFT
                and snake.direction != RIGHT
            ):
                snake.update_direction(LEFT)

            elif (
                event.key == pg.K_RIGHT
                and snake.direction != LEFT
            ):
                snake.update_direction(RIGHT)

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
