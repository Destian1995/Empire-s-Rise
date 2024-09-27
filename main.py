import pygame
import sys
import os
import random

# Инициализация Pygame
pygame.init()

# Загрузка изображения карты
default_path = os.getcwd()
map_image = pygame.image.load(default_path + r"\files\map\map.png")
map_rect = map_image.get_rect()

# Размеры окна
screen = pygame.display.set_mode(map_rect.size)
pygame.display.set_caption("Карта княжеств")

# Определение регионов для каждого княжества (x_min, x_max, y_min, y_max)
kingdom_regions = {
    "blue": (0, 300, 0, 400),
    "green": (300, 600, 300, 600),
    "red": (300, 500, 100, 300),
    "purple": (500, 800, 0, 300),
    "yellow": (500, 800, 300, 600)
}

# Цвета княжеств
kingdom_colors = {
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128)
}

# Генерация случайных точек для каждого княжества
def generate_random_points(region, num_fortresses, num_towns):
    x_min, x_max, y_min, y_max = region
    fortresses = [(random.randint(x_min, x_max), random.randint(y_min, y_max)) for _ in range(num_fortresses)]
    towns = [(random.randint(x_min, x_max), random.randint(y_min, y_max)) for _ in range(num_towns)]
    return fortresses, towns

# Генерация точек для всех княжеств
blue_fortresses, blue_towns = generate_random_points(kingdom_regions["blue"], 9, 12)
green_fortresses, green_towns = generate_random_points(kingdom_regions["green"], 5, 8)
red_fortresses, red_towns = generate_random_points(kingdom_regions["red"], 3, 6)
purple_fortresses, purple_towns = generate_random_points(kingdom_regions["purple"], 6, 8)
yellow_fortresses, yellow_towns = generate_random_points(kingdom_regions["yellow"], 5, 10)

# Функция для отрисовки объектов на карте
def draw_objects():
    screen.blit(map_image, map_rect)

    # Отрисовка объектов для синего княжества
    for fortress in blue_fortresses:
        pygame.draw.circle(screen, (0, 0, 255), fortress, 10)  # Синие крепости
    for town in blue_towns:
        pygame.draw.circle(screen, (255, 255, 255), town, 5)  # Белые деревни

    # Отрисовка объектов для зеленого княжества
    for fortress in green_fortresses:
        pygame.draw.circle(screen, (0, 255, 0), fortress, 10)  # Зеленые крепости
    for town in green_towns:
        pygame.draw.circle(screen, (255, 255, 255), town, 5)  # Белые деревни

    # Отрисовка объектов для красного княжества
    for fortress in red_fortresses:
        pygame.draw.circle(screen, (255, 0, 0), fortress, 10)  # Красные крепости
    for town in red_towns:
        pygame.draw.circle(screen, (255, 255, 255), town, 5)  # Белые деревни

    # Отрисовка объектов для фиолетового княжества
    for fortress in purple_fortresses:
        pygame.draw.circle(screen, (128, 0, 128), fortress, 10)  # Фиолетовые крепости
    for town in purple_towns:
        pygame.draw.circle(screen, (255, 255, 255), town, 5)  # Белые деревни

    # Отрисовка объектов для желтого княжества
    for fortress in yellow_fortresses:
        pygame.draw.circle(screen, (255, 255, 0), fortress, 10)  # Желтые крепости
    for town in yellow_towns:
        pygame.draw.circle(screen, (255, 255, 255), town, 5)  # Белые деревни

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Очистка экрана и отрисовка карты и объектов
    screen.fill((0, 0, 0))
    draw_objects()

    # Обновление экрана
    pygame.display.flip()

    pygame.time.delay(100)  # Задержка, чтобы снизить нагрузку на процессор
