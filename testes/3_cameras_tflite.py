from flask import Flask, Response
import cv2
import numpy as np
import time
from tflite_runtime.interpreter import Interpreter

app = Flask(__name__)

# Inicializar as câmeras
camera_left = cv2.VideoCapture(0)
camera_center = cv2.VideoCapture(2)
camera_right = cv2.VideoCapture(3)

if not camera_left.isOpened():
    raise RuntimeError("Erro: Câmera esquerda (0) não pode ser acessada.")
if not camera_center.isOpened():
    raise RuntimeError("Erro: Câmera central (2) não pode ser acessada.")
if not camera_right.isOpened():
    raise RuntimeError("Erro: Câmera direita (3) não pode ser acessada.")

# Carregar os modelos
interpreter_left = Interpreter(model_path="model_left.tflite")
interpreter_center = Interpreter(model_path="model_center.tflite")
interpreter_right = Interpreter(model_path="model_right.tflite")

interpreter_left.allocate_tensors()
interpreter_center.allocate_tensors()
interpreter_right.allocate_tensors()

# Informações do modelo
input_details_left = interpreter_left.get_input_details()
output_details_left = interpreter_left.get_output_details()

input_details_center = interpreter_center.get_input_details()
output_details_center = interpreter_center.get_output_details()

input_details_right = interpreter_right.get_input_details()
output_details_right = interpreter_right.get_output_details()

# Dimensão de entrada esperada
input_shape = (135, 100)

# Classes
class_labels = {0: "Sem Peca", 1: "Sem Rosca", 2: "Com Rosca"}

def preprocess_image(frame):
    try:
        img_array = np.array(frame)
        img_resized = cv2.resize(img_array, input_shape)
        img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        img_float = img_gray.astype(np.float32)
        img_input = img_float.reshape(-1, 135, 100, 1)
        return img_input
    except Exception as e:
        print(f"Erro no pré-processamento: {e}")
        return None

def classify_frame(interpreter, input_details, output_details, frame):
    input_data = preprocess_image(frame)
    if input_data is None:
        return "Erro", 0.0
    try:
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        predicted_class = np.argmax(output_data)
        confidence = output_data[0][predicted_class]
        return class_labels.get(predicted_class, "Desconhecido"), confidence
    except Exception as e:
        print(f"Erro na classificação: {e}")
        return "Erro", 0.0

def generate_frames():
    while True:
        # Captura dos frames das 3 câmeras
        ret_left, frame_left = camera_left.read()
        ret_center, frame_center = camera_center.read()
        ret_right, frame_right = camera_right.read()

        if not ret_left or not ret_center or not ret_right:
            print("Erro ao capturar frames das câmeras.")
            break

        # Classificar os frames das 3 câmeras
        label_left, confidence_left = classify_frame(
            interpreter_left, input_details_left, output_details_left, frame_left
        )
        label_center, confidence_center = classify_frame(
            interpreter_center, input_details_center, output_details_center, frame_center
        )
        label_right, confidence_right = classify_frame(
            interpreter_right, input_details_right, output_details_right, frame_right
        )

        # Adicionar rótulos às imagens
        text_left = f"{label_left}: {confidence_left:.2f}"
        text_center = f"{label_center}: {confidence_center:.2f}"
        text_right = f"{label_right}: {confidence_right:.2f}"

        for text, frame in [(text_left, frame_left), (text_center, frame_center), (text_right, frame_right)]:
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            text_x = int((frame.shape[1] - text_size[0]) / 2)
            text_y = 30
            cv2.rectangle(frame, (text_x, text_y - 20), (text_x + text_size[0], text_y), (0, 255, 0), -1)
            cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        # Combinar os frames das 3 câmeras horizontalmente
        combined_frame = cv2.hconcat([frame_left, frame_center, frame_right])

        # Codificar o frame combinado
        ret, buffer = cv2.imencode('.jpg', combined_frame)
        if not ret:
            print("Erro ao codificar frame combinado.")
            break

        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
