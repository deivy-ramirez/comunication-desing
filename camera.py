import cv2
import numpy as np

# Cargar el modelo YOLO
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# Si tienes una GPU compatible, puedes usar CUDA
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Cargar las clases
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Abrir la cámara
cap = cv2.VideoCapture(0)

# Verificar si la cámara se abrió correctamente
if not cap.isOpened():
    print("No se puede abrir la cámara")
    exit()

# Ajustes para mejorar FPS
frame_skip = 1  # Procesar cada 2 frames
frame_count = 0

# Bucle para mostrar el video en tiempo real
while True:
    # Capturar frame por frame
    ret, frame = cap.read()

    # Si no se pudo leer el frame
    if not ret:
        print("No se pudo recibir frame (stream finalizado)")
        break

    # Redimensionar el frame para mejorar la velocidad
    frame = cv2.resize(frame, (1020, 720))  # Cambia la resolución a 320x240

    frame_count += 1
    if frame_count % frame_skip != 0:  # Procesar solo cada 'frame_skip' frames
        cv2.imshow('Detección de Objetos con YOLO', frame)
        if cv2.waitKey(1) == ord('q'):
            break
        continue

    # Detección de objetos usando YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    layer_names = net.getLayerNames()
    
    # Obtener las capas de salida no conectadas
    output_layers_indices = net.getUnconnectedOutLayers()
    output_layers = [layer_names[i - 1] for i in output_layers_indices]
    
    detections = net.forward(output_layers)

    # Almacenar las detecciones
    boxes = []
    confidences = []
    class_ids = []

    # Procesar las detecciones
    for out in detections:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Filtrar detecciones por confianza
            if confidence > 0.5:  # Ajusta este umbral según sea necesario
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                w = int(detection[2] * frame.shape[1])
                h = int(detection[3] * frame.shape[0])

                # Coordenadas del rectángulo
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Almacenar la caja, confianza y clase
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Aplicar Non-Maximum Suppression para eliminar cajas redundantes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Dibujar rectángulos alrededor de los objetos detectados
    if len(indices) > 0:  # Verificar si hay índices válidos
        for i in indices.flatten():  # Aplanar el array de índices
            box = boxes[i]
            x, y, w, h = box
            label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"

            # Color del rectángulo según la clase
            color = (0, 255, 0) if classes[class_ids[i]] == "person" else (0, 0, 255)

            # Dibujar el rectángulo
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Mostrar el frame con los rectángulos dibujados
    cv2.imshow('Detección de Objetos con YOLO', frame)

    # Salir si se presiona 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Liberar recursos y cerrar la ventana
cap.release()
cv2.destroyAllWindows()