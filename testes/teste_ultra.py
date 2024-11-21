from ultralytics import YOLO
import cv2
import time
import os

# os.environ["QT_QPA_PLATFORM"] = "x11"

# Carregar o modelo YOLOv8 Nano
model = YOLO('yolov8n.pt')

# Carregar a imagem 
img = cv2.imread('carros.jpg')

# Primeira execução para 'aquecimento' do modelo
model.predict(source=img, save=False, save_txt=False, conf=0.5, verbose=False)

# Segunda execução (para medir o tempo de inferência)
t_start = time.monotonic()
results = model.predict(source=img, save=False, save_txt=False, conf=0.5, verbose=False)
dt = time.monotonic() - t_start
print("Tempo de inferência:", dt)

# Obter resultados de detecção
boxes = results[0].boxes
names = model.names
confidence, class_ids = boxes.conf, boxes.cls.int()
rects = boxes.xyxy.int()

# Iterar sobre cada detecção e desenhar retângulos e rótulos
for ind in range(len(rects)):
    # Coordenadas e informações da detecção
    x1, y1, x2, y2 = map(int, rects[ind].tolist())  # Converte coordenadas para inteiros
    label = names[class_ids[ind].item()]
    conf = confidence[ind].item()

    # Desenhar o retângulo da detecção
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Verde para o retângulo

    # Texto com rótulo e confiança
    text = f"{label}: {conf:.2f}"
    cv2.putText(img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Exibir a imagem resultante
cv2.imshow("Detections", img)
cv2.waitKey(0)  # Espera uma tecla para fechar a janela
cv2.destroyAllWindows()
