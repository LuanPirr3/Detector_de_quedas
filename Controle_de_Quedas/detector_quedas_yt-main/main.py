import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import math

video = cv2.VideoCapture('vd05.mp4')
detector = PoseDetector()

while True:
    check, img = video.read()
    img = cv2.resize(img, (1280, 720))

    resultado = detector.findPose(img)
    pontos, bbox = detector.findPosition(img, draw=False)

    if len(pontos) >= 1:
        x, y, w, h = bbox['bbox']
        cabeca = pontos[0][1], pontos[0][2]  # Cabeça: ponto
        ombro = pontos[11][1], pontos[11][2]  # Ombro esquerdo
        quadril = pontos[23][1], pontos[23][2]  # Quadril esquerdo
        joelho = pontos[26][1], pontos[26][2]  # Joelho esquerdo

        # Calcular ângulo entre ombro e quadril (ângulo do tronco)
        delta_x = quadril[0] - ombro[0]
        delta_y = quadril[1] - ombro[1]
        angulo_tronco = math.degrees(math.atan2(delta_y, delta_x))

        # Verificar se o ângulo do tronco é quase horizontal
        if -30 < angulo_tronco < 30:
            print("Possível Queda Detectada!")
            cvzone.putTextRect(img, 'QUEDA DETECTADA', (x, y - 80), scale=3, thickness=3, colorR=(0, 0, 255))

        # Verificar se a posição da cabeça está muito próxima do chão (indicando uma queda)
        if cabeca[1] > joelho[1]:  # cabeça estiver mais baixa que o joelho
            print("Possível Queda Detectada!")
            cvzone.putTextRect(img, 'QUEDA DETECTADA', (x, y - 80), scale=3, thickness=3, colorR=(0, 0, 255))

    cv2.imshow('IMG', img)
    cv2.waitKey(1)
