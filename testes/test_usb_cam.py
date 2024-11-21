import cv2

# Inicializa a captura de vídeo
cam = cv2.VideoCapture(0)

# Variáveis de controle
recording = False
out = None

while True:
    ret, image = cam.read()
    if not ret:
        print("Falha ao capturar a imagem")
        break

    # Exibe o frame ao vivo na janela "Imagetest"
    cv2.imshow('Imagetest', image)

    # Verifica se a gravação está ativa e grava o frame no arquivo
    if recording:
        out.write(image)

    # Verifica se alguma tecla foi pressionada
    k = cv2.waitKey(1) & 0xFF

    # Se a tecla 'r' for pressionada, começa a gravar o vídeo
    if k == ord('r'):
        if not recording:
            print("Gravação iniciada")
            # Define o codec e cria o objeto VideoWriter para salvar o vídeo
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output_video.avi', fourcc, 20.0, (640, 480))
            recording = True

    # Se a tecla 's' for pressionada, para a gravação
    elif k == ord('s'):
        if recording:
            print("Gravação parada")
            recording = False
            out.release()  # Libera o arquivo de vídeo

    # Se a tecla 'q' for pressionada, sai do loop e fecha a janela
    elif k == ord('q'):
        print("Saindo")
        break

# Salva a última imagem capturada como 'testimage.jpg'
cv2.imwrite('/home/pi/testimage.jpg', image)

# Libera a câmera e o arquivo de vídeo se ainda estiver gravando
cam.release()
if out is not None:
    out.release()

# Fecha todas as janelas
cv2.destroyAllWindows()
