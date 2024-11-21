from flask import Flask, Response
import cv2
import time
import numpy as np
from tflite_runtime.interpreter import Interpreter

app = Flask(__name__)

# Inicializar a câmera USB (0 significa a primeira câmera conectada)
camera = cv2.VideoCapture(0)

# Verifica se a câmera foi aberta corretamente
if not camera.isOpened():
    raise RuntimeError("Não foi possível acessar a câmera.")

# Carregar o modelo TensorFlow Lite
model_path = "model_right.tflite"  # Altere para o caminho do seu modelo .tflite
interpreter = Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Obtenha informações de entrada e saída do modelo
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Definir dimensões de entrada esperadas (480x640)
input_shape = (135, 100)  # Largura x Altura

# Dicionário de rótulos (substitua com os rótulos reais do seu modelo)
class_labels = {0: "Sem Peca", 1: "Sem Rosca", 2: "Com Rosca"}  # Exemplo de rótulos

def preprocess_image(frame):
    # Redimensiona o frame para o tamanho de entrada do modelo e normaliza
    img_array = np.array(frame)
    img_resized = cv2.resize(img_array, input_shape)
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    img_float = img_gray.astype(np.float32)
    img_input = img_float.reshape(-1, 135, 100, 1)

    return img_input

def classify_frame(frame):
    # Preprocessar o frame
    input_data = preprocess_image(frame)

    # Realizar a inferência
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Obter o resultado da classificação
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.argmax(output_data)
    confidence = output_data[0][predicted_class]

    return class_labels.get(predicted_class, "Desconhecido"), confidence

def generate_frames():
    while True:
        # Captura o frame da câmera
        ret, frame = camera.read()
        if not ret:
            break

        # Realizar a classificação a cada frame
        label, confidence = classify_frame(frame)

        # Exibir a classe detectada e a confiança no frame
        text = f"{label}: {confidence:.2f}"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        text_x = int((frame.shape[1] - text_size[0]) / 2)
        text_y = 30

        # Coloca o texto no frame
        cv2.rectangle(frame, (text_x, text_y - 20), (text_x + text_size[0], text_y), (0, 255, 0), -1)
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

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
