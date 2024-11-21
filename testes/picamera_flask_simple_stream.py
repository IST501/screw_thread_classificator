# Para usar a câmera do python, é mais fácil instalar tudo no root, o venv atrapalha ele encontrar as bibliotecas instaladas com apt
# Só funciona com python3 por algum motivo
# 
# sudo apt install python3-picamera2
# sudo apt install -y python3-flask python3-opencv
# sudo python3 simple_stream
#
# Único vídeo que funcionou
# https://www.youtube.com/watch?v=NOAY1aaVPAw&t=176s
# https://github.com/shillehbean/youtube-p2/blob/main/stream_usb_camera.py

from flask import Flask, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()

def generate_frames():
    while True:
        frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)