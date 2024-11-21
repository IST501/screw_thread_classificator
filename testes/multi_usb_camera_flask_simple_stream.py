import threading
import time
from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

# Inicializa as duas câmeras USB
camera_1 = cv2.VideoCapture(0)
camera_2 = cv2.VideoCapture(2)

camera_1.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera_1.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

camera_2.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera_2.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Verifica se as câmeras foram abertas corretamente
if not camera_1.isOpened() or not camera_2.isOpened():
    raise RuntimeError("Não foi possível acessar uma ou ambas as câmeras.")

def generate_frames(camera):
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Adiciona um pequeno atraso para evitar sobrecarga de captura
        time.sleep(0.03)  # 30ms de atraso (~33 FPS)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera1_feed')
def camera1_feed():
    return Response(generate_frames(camera_1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera2_feed')
def camera2_feed():
    return Response(generate_frames(camera_2), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Inicia o servidor Flask em um thread separado para capturar frames paralelamente
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000}).start()
