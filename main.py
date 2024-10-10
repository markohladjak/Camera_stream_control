import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication
import cam_stream
from control_panel import ControlPanel

# Глобальні змінні для збереження параметрів
brightness = 0
contrast = 1.0
sharpness = 1.0
is_grayscale = False
control_panel = None  # Для доступу до панелі керування


def apply_adjustments(frame):
    global brightness, contrast, sharpness, is_grayscale

    # Застосовуємо яскравість і контраст
    adjusted_frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

    # Додаємо різкість
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # Фільтр для різкості
    adjusted_frame = cv2.filter2D(adjusted_frame, -1, kernel * sharpness)

    # Перетворення в чорно-біле, якщо вибрано
    if is_grayscale:
        adjusted_frame = cv2.cvtColor(adjusted_frame, cv2.COLOR_BGR2GRAY)

    # Обчислення гістограми
    if is_grayscale:
        histogram = cv2.calcHist([adjusted_frame], [0], None, [256], [0, 256])
    else:
        histogram = cv2.calcHist([adjusted_frame], [0], None, [256], [0, 256])

    # Передаємо гістограму в панель керування для відображення
    control_panel.plot_histogram(histogram)

    return adjusted_frame


def update_parameters(new_brightness, new_contrast, new_sharpness, new_grayscale):
    global brightness, contrast, sharpness, is_grayscale
    brightness = new_brightness
    contrast = new_contrast
    sharpness = new_sharpness
    is_grayscale = new_grayscale


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Створюємо панель керування і передаємо функцію для оновлення параметрів
    control_panel = ControlPanel(update_parameters)
    control_panel.show()

    # Запускаємо відеопотік з динамічною обробкою кадрів
    cam_stream.start_camera_stream(apply_adjustments)

    sys.exit(app.exec_())
