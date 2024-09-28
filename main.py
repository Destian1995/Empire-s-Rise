import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import random
import math

# Размеры окна
screen_width, screen_height = 1200, 800

# Цвета крепостей
fortress_colors = {
    "Аркадия": (0, 0.5, 0),
    "Селесия": (0, 0, 0.5),
    "Хиперион": (0.5, 0, 0.5),
    "Халидон": (0.5, 0.25, 0),
    "Этерия": (0, 0.5, 0.5)
}

# Определение регионов княжеств
kingdom_regions = {
    "Аркадия": (70, 20, 150, 250),
    "Селесия": (150, 530, 140, 200),
    "Хиперион": (500, 200, 200, 200),
    "Халидон": (800, 150, 250, 250),
    "Этерия": (1025, 450, 100, 100)
}

# Проверка минимального расстояния между точками
def is_far_enough(new_point, existing_points, min_distance):
    for point in existing_points:
        distance = math.sqrt((new_point[0] - point[0]) ** 2 + (new_point[1] - point[1]) ** 2)
        if distance < min_distance:
            return False
    return True

# Генерация точек для деревень и крепостей
def generate_points_in_region(region, num_points, min_distance):
    points = []
    attempts = 0
    max_attempts = num_points * 100

    while len(points) < num_points and attempts < max_attempts:
        x = random.randint(region[0], region[0] + region[2])
        y = random.randint(region[1], region[1] + region[3])

        if is_far_enough((x, y), points, min_distance):
            points.append((x, y))

        attempts += 1

    return points

# Генерация крепостей и деревень
kingdom_points = {}
for kingdom, region in kingdom_regions.items():
    if kingdom == "Хиперион":
        num_fortresses = 13
    elif kingdom == "Аркадия":
        num_fortresses = 7
    elif kingdom == "Селесия":
        num_fortresses = 5
    elif kingdom == "Халидон":
        num_fortresses = 6
    elif kingdom == "Этерия":
        num_fortresses = 4

    kingdom_points[kingdom] = {
        "fortresses": generate_points_in_region(region, num_fortresses, min_distance=30),
        "towns": generate_points_in_region(region, random.randint(6, 10), min_distance=20)
    }

# Виджет карты
class MapWidget(Widget):
    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        self.map_pos = [0, 0]  # Позиция карты
        self.touch_start = None  # Стартовая позиция касания

        with self.canvas:
            # Отрисовка карты
            self.map_image = Rectangle(source='files/map/map.png', pos=self.map_pos, size=(screen_width, screen_height))

            # Отрисовка крепостей и деревень
            self.draw_map()

    def draw_map(self):
        for kingdom, points in kingdom_points.items():
            # Отрисовка крепостей
            for fortress in points["fortresses"]:
                Color(*fortress_colors[kingdom])
                Ellipse(pos=(fortress[0] + self.map_pos[0], fortress[1] + self.map_pos[1]), size=(20, 20))

            # Отрисовка деревень
            for town in points["towns"]:
                Color(1, 1, 1)
                Ellipse(pos=(town[0] + self.map_pos[0], town[1] + self.map_pos[1]), size=(10, 10))

    def on_touch_down(self, touch):
        # Запоминаем начальную точку касания
        self.touch_start = touch.pos

    def on_touch_move(self, touch):
        # Вычисляем смещение
        if self.touch_start:
            dx = touch.x - self.touch_start[0]
            dy = touch.y - self.touch_start[1]
            self.touch_start = touch.pos  # Обновляем точку касания

            # Обновляем позицию карты
            self.map_pos[0] += dx
            self.map_pos[1] += dy
            self.update_map_position()

    def update_map_position(self):
        # Обновляем позицию изображения карты
        self.map_image.pos = self.map_pos

        # Перерисовываем крепости и деревни с новой позицией
        self.canvas.clear()
        with self.canvas:
            Rectangle(source='files/map/map.png', pos=self.map_pos, size=(screen_width, screen_height))
            self.draw_map()

# Основное приложение
class KingdomApp(App):
    def build(self):
        layout = FloatLayout()

        # Добавление виджета с картой
        layout.add_widget(MapWidget())

        # Создание кнопок
        button_layout = BoxLayout(size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})

        btn_politics = Button(text="Политика", on_press=self.on_politics_press)
        btn_army = Button(text="Армия", on_press=self.on_army_press)
        btn_economy = Button(text="Экономика", on_press=self.on_economy_press)

        # Добавляем кнопки в нижнюю часть интерфейса
        button_layout.add_widget(btn_politics)
        button_layout.add_widget(btn_army)
        button_layout.add_widget(btn_economy)

        layout.add_widget(button_layout)

        return layout

    # Обработчики для кнопок
    def on_politics_press(self, instance):
        print("Политика кнопка нажата")

    def on_army_press(self, instance):
        print("Армия кнопка нажата")

    def on_economy_press(self, instance):
        print("Экономика кнопка нажата")

# Запуск приложения
if __name__ == '__main__':
    KingdomApp().run()
