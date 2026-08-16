"""Финальный проект спринта Изгиб питона."""

from random import choice, randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка-финальный проект')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Основной класс в игре. Игровое поле."""

    def __init__(self, position=None, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Объявляем пустой метод отрисовка, который перенаследуется дальше."""
        pass


class Apple(GameObject):
    """Объявление дочернего класса. Яблоко."""

    # Инициализация позиция блока на поле и цвет.
    def __init__(self, position=None, body_color=APPLE_COLOR):
        # Унаследование атрибутов с основного класса GameObject
        super().__init__(position, body_color)

    def randomize_position(self):
        """Метод задает случайное положение яблока."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Переопределяем метод отрисовка для яблока."""
        # Создаём прямоугольник в позиции яблока размером с 1 клетку.
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        # Заливаем прямоугольник цветом яблока.
        pygame.draw.rect(screen, self.body_color, rect)
        # Рисуем границы ячейки толщиной 1 пиксель.
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Объявляем дочерний класс Змейка."""

    def __init__(
            self, length=1, positions=None, direction=RIGHT,
            next_direction=None, body_color=SNAKE_COLOR, last=None):

        if positions is None:
            positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]

        self.length = length
        self.positions = positions
        self.direction = direction
        self.next_direction = next_direction
        self.body_color = body_color
        self.last = last
        # Унаследование атрибутов с основного класса GameObject
        super().__init__(positions[0], body_color)

    def get_head_position(self):
        """Метод возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод движения змейки."""
        # Получаем текущую позицию головы змейки.
        head = self.get_head_position()
        # Вычисляем новую позицию головы змейки.
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        # Добавляем новую голову в начало списка.
        self.positions.insert(0, new_head)
        # Удаляем хвостовой сегмент при превышении длины.
        if len(self.positions) > self.length:
            self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Переопределяем метод отрисовка для змейки."""
        # Перебираем список сегментов, кроме последнего.
        for position in self.positions[:-1]:
            # Для каждой позиции из цикла создаём квадрат.
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            # Рисуем сегмент змейки.
            pygame.draw.rect(screen, self.body_color, rect)
            # Рисуем границу сегмента с толщиной 1.
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            # Создаём прямоугольник на месте старого сегмента.
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            # Закрашиваем её цветом фона.
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def screen_fill(self):
        """Метод очистки экрана перед новой игрой."""
        screen.fill(BOARD_BACKGROUND_COLOR)

    def reset(self):
        """Метод возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


def handle_keys(game_object):
    """Метод обработки действий пользователя"""
    for event in pygame.event.get():
        # Пользователь закрывает окно.
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif (
                event.key == pygame.K_DOWN
                and game_object.direction != UP
            ):
                game_object.next_direction = DOWN
            elif (
                event.key == pygame.K_LEFT
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT
            elif (
                event.key == pygame.K_RIGHT
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple((0, 0))
    apple.randomize_position()
    # Запускаем бесконечный цикл while.
    while True:
        # Ограничеваем скорость движения змейки.
        clock.tick(SPEED)
        handle_keys(snake)
        # Обновляем положение змейки.
        snake.update_direction()
        # Проверяем движение змейки.
        snake.move()
        # Сравниваем координаты головы змейки с координатома положения яблока.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        # Сравниваем координаты головы с остальными сегментами списка.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
