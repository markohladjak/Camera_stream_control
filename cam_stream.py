import cv2

def start_camera_stream(update_frame_callback):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Не вдалося відкрити камеру")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не вдалося отримати кадр")
            break

        # Виклик функції обробки кадру
        frame = update_frame_callback(frame)

        # Відображення кадру
        cv2.imshow('Камера', frame)

        # Вихід з циклу при натисканні клавіші 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
