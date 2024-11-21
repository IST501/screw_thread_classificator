from ultralytics import YOLO
from picamera2 import Picamera2
import cv2
import time

# Inicializar a câmera usando Picamera2
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
camera.start()

# Carregar o modelo YOLOv8 Nano
model = YOLO('yolov8n.pt')

# Primeira execução para 'aquecimento' do modelo
frame = camera.capture_array()
model.predict(source=frame, save=False, save_txt=False, conf=0.5, verbose=False)

# Laço principal para detecção em tempo real
while True:
    # Captura o frame da câmera
    frame = camera.capture_array()

    # Início do tempo para medir o FPS
    t_start = time.monotonic()

    # Realizar a inferência
    results = model.predict(source=frame, save=False, save_txt=False, conf=0.5, verbose=False)
    
    # Extrair as caixas delimitadoras e as informações das detecções
    boxes = results[0].boxes
    names = model.names
    confidence, class_ids = boxes.conf, boxes.cls.int()
    rects = boxes.xyxy.int()

    # Iterar sobre cada detecção e desenhar retângulos e rótulos
    for ind in range(len(rects)):
        x1, y1, x2, y2 = map(int, rects[ind].tolist())
        label = names[class_ids[ind].item()]
        conf = confidence[ind].item()

        # Desenhar o retângulo e o texto da detecção
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        text = f"{label}: {conf:.2f}"
        cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Exibir o frame com detecções
    cv2.imshow("Detections", frame)

    # Cálculo do tempo de inferência
    dt = time.monotonic() - t_start
    print("Tempo de inferência:", dt)

    # Espera para ajustar o FPS para 1 (1 frame por segundo)
    time.sleep(max(1 - dt, 0))

    # Sair com a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha janelas
camera.stop()
cv2.destroyAllWindows()
