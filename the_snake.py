"""Финальный проект спринта Изгиб питона."""

from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
# Ширина и высота игрового окна.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
# Размеры 1 клетки
GRID_SIZE = 20
# 640 // 20 = 32 клетки помещается по ширине
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
# 480 // 20 = 24 клетки помещается по высоте
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Константа словарь для управления клавишами:
DIRECTIONS = {
    (UP, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_LEFT): LEFT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока красный
APPLE_COLOR = (255, 0, 0)

# Цвет змейки зелёный
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка-финальный проект')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Основной класс в игре. Игровое поле."""

    def __init__(self, body_color=None):
        self.body_color = body_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self):
        """Объявляем пустой метод отрисовка, который перенаследуется дальше."""
        raise NotImplementedError

    def draw_rect(self, position, body_color=BORDER_COLOR):
        """Метод создание прямоугольника"""
        # Создаём прямоугольник размером с 1 клетку.
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        # Рисуем ячейку.
        pg.draw.rect(screen, body_color, rect)

        if body_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Объявление дочернего класса. Яблоко."""

    # Инициализация заданной позиции яблока на поле и цвет.
    def __init__(self, occupied_positions=[], body_color=APPLE_COLOR):
        # Унаследование атрибутов с основного класса GameObject
        super().__init__(body_color)
        # Вызываем метод случайное положение яблока и передаем в него аргумент.
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=[]):
        """Метод задает случайное положение яблока."""
        self.occupied_positions = occupied_positions
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Переопределяем метод отрисовка для яблока."""
        self.draw_rect(self.position, self.body_color)


class Snake(GameObject):
    """Объявляем дочерний класс Змейка."""

    def __init__(self, body_color=SNAKE_COLOR):
        self.body_color = body_color
        # Унаследование атрибутов с основного класса GameObject
        super().__init__(body_color)
        self.reset()

    def get_head_position(self):
        """Метод возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод движения змейки."""
        # Получаем текущую позицию головы змейки.
        head = self.get_head_position()
        # Распакуем координаты в переменные x и y.
        x, y = head
        # Вычисляем новую позицию головы змейки.
        self.position = (
            (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        # Добавляем новую голову в начало списка.
        self.positions.insert(0, self.position)
        # Удаляем хвостовой сегмент при превышении длины.
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self, new_direction):
        """Метод обновления направления после нажатия на кнопку."""
        if new_direction:
            self.direction = new_direction

    def draw(self):
        """Переопределяем метод отрисовка для змейки."""
        # Затирание последнего сегмента
        if self.last:
            # Создаём прямоугольник на месте старого сегмента.
            self.draw_rect(self.last, BOARD_BACKGROUND_COLOR)
        # Перебираем список сегментов, кроме последнего.
        for position in self.positions:
            self.draw_rect(position, self.body_color)

    def reset(self):
        """Метод возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Метод обработки действий пользователя"""
    global SPEED

    for event in pg.event.get():
        # Пользователь закрывает окно.
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type != pg.KEYDOWN:
            continue
        elif event.key == pg.K_ESCAPE:
            pg.quit()
            raise SystemExit
        # Управляем скоростью змейки.
        elif event.key == pg.K_w:
            SPEED = min(SPEED + 1, 40)
        elif event.key == pg.K_s:
            SPEED = max(SPEED - 1, 2)
        else:
            new_direction = DIRECTIONS.get(
                (game_object.direction, event.key),
                game_object.direction)
            game_object.update_direction(new_direction)


def main():
    """Основной игровой цикл."""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)
    # Запускаем бесконечный цикл while.
    while True:
        # Ограничеваем скорость движения змейки.
        clock.tick(SPEED)
        handle_keys(snake)
        # Проверяем движение змейки.
        snake.move()
        # Сравниваем координаты головы змейки с координатома положения яблока.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        # Сравниваем координаты головы с остальными сегментами списка.
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
