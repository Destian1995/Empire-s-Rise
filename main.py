from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

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

# Координаты крепостей и деревень для каждого княжества
# Добавлены параметры вершин 7-угольников для каждой крепости
kingdom_points = {
    "Аркадия": {
        "fortresses": [
            {"pos": (80, 100), "polygon": [(30, 40), (70, 20), (50, -30), (-20, -50), (-70, -20), (-50, 30), (20, 50)]},
            {"pos": (120, 150), "polygon": [(40, 50), (80, 30), (60, -40), (-30, -60), (-80, -30), (-60, 40), (30, 60)]}
        ],
        "towns": [(90, 120), (130, 180), (170, 230), (210, 270), (230, 120), (250, 160), (270, 200)]
    },
    "Селесия": {
        "fortresses": [
            {"pos": (180, 560), "polygon": [(30, 40), (70, 20), (50, -30), (-20, -50), (-70, -20), (-50, 30), (20, 50)]},
            {"pos": (200, 600), "polygon": [(40, 50), (80, 30), (60, -40), (-30, -60), (-80, -30), (-60, 40), (30, 60)]}
        ],
        "towns": [(190, 570), (210, 620), (230, 660), (250, 700)]
    },
    "Хиперион": {
        "fortresses": [
            {"pos": (510, 220), "polygon": [(40, 50), (70, 20), (60, -40), (-20, -60), (-70, -20), (-60, 40), (30, 50)]},
            {"pos": (710, 120), "polygon": [(40, 50), (70, 20), (60, -40), (-20, -60), (-70, -20), (-60, 40), (30, 50)]},
            {"pos": (810, 420), "polygon": [(40, 50), (70, 20), (60, -40), (-20, -60), (-70, -20), (-60, 40), (30, 50)]},
            {"pos": (310, 200), "polygon": [(70, 90), (80, 90), (60, -90), (-10, -30), (-10, -30), (-20, 50), (30, 70)]} #южный
        ],
        "towns": [(220, 240), (540, 280), (560, 320), (580, 360), (600, 400)]
    },
    "Халидон": {
        "fortresses": [
            {"pos": (820, 160), "polygon": [(40, 60), (70, 40), (60, -40), (-30, -60), (-70, -30), (-60, 40), (30, 60)]}
        ],
        "towns": [(750, 270), (850, 220), (870, 260), (890, 300)]
    },
    "Этерия": {
        "fortresses": [
            {"pos": (1030, 460), "polygon": [(40, 50), (80, 30), (60, -40), (-30, -60), (-80, -30), (-60, 40), (30, 50)]}
        ],
        "towns": [(1040, 370), (900, 510), (1080, 550)]
    }
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
            # Отрисовка крепостей с границами в виде настраиваемых полигонов
            for fortress_data in points["fortresses"]:
                fortress = fortress_data["pos"]
                polygon = fortress_data["polygon"]

                # Рисуем крепость
                Color(*fortress_colors[kingdom])  # Цвет крепости
                Ellipse(pos=(fortress[0] + self.map_pos[0], fortress[1] + self.map_pos[1]), size=(20, 20))

                # Рисуем полигон вокруг крепости
                self.draw_custom_polygon(fortress[0] + 10 + self.map_pos[0], fortress[1] + 10 + self.map_pos[1], polygon)

            # Отрисовка деревень
            for town in points["towns"]:
                Color(1, 1, 1)
                Ellipse(pos=(town[0] + self.map_pos[0], town[1] + self.map_pos[1]), size=(10, 10))

    def draw_custom_polygon(self, x_center, y_center, polygon_points):
        """Отрисовка полигона на основе списка точек относительно крепости."""
        points = []

        for point in polygon_points:
            x = x_center + point[0]
            y = y_center + point[1]
            points.extend([x, y])

        Color(1, 1, 1, 0.5)  # Полупрозрачная граница
        Line(points=points, close=True, width=1)

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
