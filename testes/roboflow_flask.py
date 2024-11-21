from flask import Flask, Response
import cv2
import time
from ultralytics import YOLO

app = Flask(__name__)

# Inicializar a câmera USB (0 significa a primeira câmera conectada)
camera = cv2.VideoCapture(0)

# Verifica se a câmera foi aberta corretamente
if not camera.isOpened():
    raise RuntimeError("Não foi possível acessar a câmera.")

# Carregar o modelo YOLOv8 Nano
model = YOLO('best.pt')

# Reduzir a resolução da captura para melhorar a performance
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Largura
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Altura

frame_counter = 0  # Contador de frames
last_detection = None  # Para armazenar a última detecção

def generate_frames():
    global frame_counter, last_detection

    while True:
        # Captura o frame da câmera
        ret, frame = camera.read()
        if not ret:
            break

        # Incrementa o contador de frames
        frame_counter += 1

        # Realizar a inferência a cada 60 frames
        if frame_counter % 60 == 0:
            # Início do tempo para medir o FPS
            t_start = time.monotonic()

            # Realizar a inferência
            results = model.predict(source=frame, save=False, save_txt=False, conf=0.5, verbose=False)

            # Extrair as caixas delimitadoras e as informações das detecções
            boxes = results[0].boxes
            names = model.names
            confidence, class_ids = boxes.conf, boxes.cls.int()
            rects = boxes.xyxy.int()

            # Atualizar a última detecção
            last_detection = (frame.copy(), boxes, names, confidence, class_ids)

        # Se houve uma detecção anterior, desenhar no frame
        if last_detection:
            detected_frame, boxes, names, confidence, class_ids = last_detection

            # Iterar sobre cada detecção e desenhar retângulos e rótulos
            for ind in range(len(boxes)):
                box = boxes[ind]
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # Acessando as coordenadas corretamente

                label = names[class_ids[ind].item()]
                conf = confidence[ind].item()

                # Desenhar o retângulo e o texto da detecção
                cv2.rectangle(detected_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                text = f"{label}: {conf:.2f}"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                cv2.rectangle(detected_frame, (x1, y1 - 20), (x1 + text_size[0], y1), (0, 255, 0), -1)
                cv2.putText(detected_frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            frame = detected_frame  # Usar o frame com detecções

        # Codificar o frame em JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break
        frame = buffer.tobytes()

        # Retornar o frame no formato esperado pelo Flask
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Inicia o servidor Flask na porta 5000
    app.run(host='0.0.0.0', port=5000)
