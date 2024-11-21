from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import time
from ultralytics import YOLO

app = Flask(__name__)

# Inicializar a câmera usando Picamera2
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))  # Mudar para RGB888
camera.start()

# Carregar o modelo YOLOv8 Nano
model = YOLO('yolov8n.pt')

def generate_frames():
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

        # Codificar o frame em JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Retornar o frame no formato esperado pelo Flask
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
