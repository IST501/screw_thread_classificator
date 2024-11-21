from flask import Flask, Response
import cv2

app = Flask(__name__)

# Inicializa a câmera USB (0 significa a primeira câmera conectada)
camera = cv2.VideoCapture(0)

# Verifica se a câmera foi aberta corretamente
if not camera.isOpened():
    raise RuntimeError("Não foi possível acessar a câmera.")

def generate_frames():
    while True:
        # Captura frame por frame da câmera
        ret, frame = camera.read()
        if not ret:
            break

        # Codifica o frame como JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break

        frame = buffer.tobytes()

        # Gera o frame como resposta HTTP
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
    # Rota principal que retorna o feed de vídeo
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Inicia o servidor Flask na porta 5000
    app.run(host='0.0.0.0', port=5000)
