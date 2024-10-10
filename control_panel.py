from PyQt5.QtWidgets import QWidget, QSlider, QVBoxLayout, QLabel, QCheckBox, QPushButton
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class ControlPanel(QWidget):
    def __init__(self, update_callback):
        super().__init__()

        self.brightness = 0
        self.contrast = 1.0
        self.sharpness = 1.0
        self.is_grayscale = False
        self.update_callback = update_callback

        # Створюємо малюнок для гістограми
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.init_ui()

    def init_ui(self):
        # Повзунки для яскравості, контрасту і різкості
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(-50)
        self.brightness_slider.setMaximum(50)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(self.update_brightness)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(10)
        self.contrast_slider.setMaximum(30)
        self.contrast_slider.setValue(10)
        self.contrast_slider.valueChanged.connect(self.update_contrast)

        self.sharpness_slider = QSlider(Qt.Horizontal)
        self.sharpness_slider.setMinimum(1)
        self.sharpness_slider.setMaximum(10)
        self.sharpness_slider.setValue(1)
        self.sharpness_slider.valueChanged.connect(self.update_sharpness)

        # Чекбокс для чорно-білого режиму
        self.grayscale_checkbox = QCheckBox('Grayscale', self)
        self.grayscale_checkbox.stateChanged.connect(self.toggle_grayscale)

        # Кнопка скидання (Reset)
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_parameters)

        # Розміщення елементів на екрані
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Brightness'))
        layout.addWidget(self.brightness_slider)
        layout.addWidget(QLabel('Contrast'))
        layout.addWidget(self.contrast_slider)
        layout.addWidget(QLabel('Sharpness'))
        layout.addWidget(self.sharpness_slider)
        layout.addWidget(self.grayscale_checkbox)
        layout.addWidget(self.reset_button)  # Додаємо кнопку "Reset"

        # Додаємо полотно для гістограми
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.setWindowTitle('Control Panel')

    def update_brightness(self, value):
        self.brightness = value
        self.update_callback(self.brightness, self.contrast, self.sharpness, self.is_grayscale)

    def update_contrast(self, value):
        self.contrast = value / 10
        self.update_callback(self.brightness, self.contrast, self.sharpness, self.is_grayscale)

    def update_sharpness(self, value):
        self.sharpness = value / 5
        self.update_callback(self.brightness, self.contrast, self.sharpness, self.is_grayscale)

    def toggle_grayscale(self, state):
        self.is_grayscale = state == Qt.Checked
        self.update_callback(self.brightness, self.contrast, self.sharpness, self.is_grayscale)

    def reset_parameters(self):
        # Скидаємо всі параметри до початкових значень
        self.brightness_slider.setValue(0)
        self.contrast_slider.setValue(10)
        self.sharpness_slider.setValue(1)
        self.grayscale_checkbox.setChecked(False)

        # Оновлюємо внутрішні параметри
        self.brightness = 0
        self.contrast = 1.0
        self.sharpness = 1.0
        self.is_grayscale = False

        # Викликаємо функцію оновлення
        self.update_callback(self.brightness, self.contrast, self.sharpness, self.is_grayscale)

    def plot_histogram(self, histogram):
        # Очищаємо попередній графік
        self.ax.clear()

        # Створюємо нову гістограму
        self.ax.plot(histogram)

        # Оновлюємо полотно
        self.canvas.draw()
