import RPi.GPIO as GPIO
import time
import pygame

# Configuración del servomotor
SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500
Servo = 23

def map(value, inMin, inMax, outMin, outMax):
    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin

def setup():
    global p
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Servo, GPIO.OUT)
    GPIO.output(Servo, GPIO.LOW)
    p = GPIO.PWM(Servo, 50)
    p.start(0)

def setAngle(angle):
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)

def destroy():
    p.stop()
    GPIO.cleanup()

# Configuración del joystick
pygame.init()
pygame.joystick.init()

# Inicializa la ventana de Pygame
screen = pygame.display.set_mode((640, 480))

def main():
    setup()
    hecho = False
    reloj = pygame.time.Clock()

    # Establecer el ángulo inicial en 90 grados
    current_angle = 90
    setAngle(current_angle)

    while not hecho:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                hecho = True

        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            # Obtener los valores de los ejes L2 y R2
            eje_l2 = joystick.get_axis(2)  # L2
            eje_r2 = joystick.get_axis(5)  # R2

            # Ajustar el ángulo basado en L2 y R2
            if eje_r2 > 0:  # Girar a la derecha
                current_angle -= 1  # Incrementar el ángulo
            elif eje_l2 > 0:  # Girar a la izquierda
                current_angle += 1  # Decrementar el ángulo

            # Establecer el ángulo del servomotor
            setAngle(current_angle)

        # Actualiza la pantalla y limita la tasa de refresco
        pygame.display.flip()
        reloj.tick(60)

    destroy()
    pygame.quit()

if __name__ == '__main__':
    main()