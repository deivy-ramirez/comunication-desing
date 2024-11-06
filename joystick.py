"""
# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/
"""
 
import pygame
 
# Definimos algunos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
 
class TextPrint(object):
    """Esta es una sencilla clase que nos ayudará a imprimir sobre la pantalla.
    No tiene nada que ver con los joysticks, tan solo imprime información.""" 
    
    def __init__(self):
        """Constructor"""
        self.reset()
        self.x_pos = 10
        self.y_pos = 10
        self.font = pygame.font.Font(None, 20)
 
    def print(self, mi_pantalla, text_string):
        textBitmap = self.font.render(text_string, True, NEGRO)
        mi_pantalla.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
         
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
         
    def indent(self):
        self.x += 10
         
    def unindent(self):
        self.x -= 10
 
pygame.init()
  
# Establecemos el largo y alto de la pantalla [largo,alto]
dimensiones = [500, 700]
pantalla = pygame.display.set_mode(dimensiones)
 
pygame.display.set_caption("Mi Juego")
 
# Iteramos hasta que el usuario pulsa el botón de salir.
hecho = False
 
# Lo usamos para gestionar cuán rápido de refresca la pantalla.
reloj = pygame.time.Clock()
 
# Inicializa los joysticks
pygame.joystick.init()
     
# Se prepara para imprimir
text_print = TextPrint()

# Definir un diccionario con nombres personalizados para los botones
nombres_botones = {
    0: "Boton X",
    1: "Boton Circulo",
    2: "Boton Cuadro",
    3: "Boton Triangulo",
    4: "Boton Share",
    5: "Boton Ps",
    6: "Boton Options",
    7: "Boton L3",
    8: "Boton R3",
    9: "Boton L1",
    10: "Boton R1",
    11: "Boton Flecha arriba",
    12: "Boton Flecha abajo",
    13: "Boton Flecha izquierda",
    14: "Boton Flecha derecha",
    15: "Panel Tactil",
    16: "Boton L2",
    17: "Boton R2",
}

# Definir un diccionario con nombres personalizados para los ejes
nombres_ejes = {
    0: "Joystick Izquierdo Horizontal",
    1: "Joystick Izquierdo Vertical",
    2: "Joystick Derecho Horizontal",
    3: "Joystick Derecho Vertical",
}
 
# Definir el umbral para tratar el eje como botón
umbral_boton = 0.5
 
# -------- Bucle Principal del Programa -----------
while not hecho:
    # PROCESAMIENTO DEL EVENTO
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            hecho = True
         
        # Acciones posibles del joystick: JOYAXISMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION
        if evento.type == pygame.JOYBUTTONDOWN:
            print("Botón presionado del joystick.")
        if evento.type == pygame.JOYBUTTONUP:
            print("Botón liberado del joystick.")
  
    # DIBUJAMOS
    # Primero, limpiamos la pantalla con color blanco.
    pantalla.fill(BLANCO)
    text_print.reset()
 
    # Contamos el número de joysticks
    joystick_count = pygame.joystick.get_count()
 
    text_print.print(pantalla, "Número de joysticks: {}".format(joystick_count) )
    text_print.indent()
     
    # Para cada joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
     
        text_print.print(pantalla, "Joystick {}".format(i) )
        text_print.indent()
     
        # Obtiene el nombre del Sistema Operativo del controlador/joystick
        nombre = joystick.get_name()
        text_print.print(pantalla, "Nombre del joystick: {}".format(nombre))
         
        # Habitualmente, los ejes van en pareja
        ejes = joystick.get_numaxes()
        text_print.print(pantalla, "Número de ejes: {}".format(ejes))
        text_print.indent()
         
        for i in range(ejes):
            if i < 4:  # Solo mostramos los ejes 0 a 3 como ejes
                eje = joystick.get_axis(i)
                nombre_eje = nombres_ejes.get(i, f"Eje {i}")
                text_print.print(pantalla, "{} valor: {:>6.3f}".format(nombre_eje, eje))
                
        text_print.unindent()
             
        botones = joystick.get_numbuttons() + 2  # Añadimos 2 para L2 y R2 como botones
        text_print.print(pantalla, "Número de botones: {}".format(botones))
        text_print.indent()
 
        for i in range(botones - 2):  # Restamos los 2 botones que añadiremos
            boton = joystick.get_button(i)
            nombre_boton = nombres_botones.get(i, f"Botón {i}")
            text_print.print(pantalla, "{} valor: {}".format(nombre_boton, boton))

        # Tratar ejes 4 y 5 como botones
        eje_l2 = joystick.get_axis(4)
        valor_boton_l2 = 1 if eje_l2 > umbral_boton else 0
        text_print.print(pantalla, "{} valor: {}".format(nombres_botones[16], valor_boton_l2))

        eje_r2 = joystick.get_axis(5)
        valor_boton_r2 = 1 if eje_r2 > umbral_boton else 0
        text_print.print(pantalla, "{} valor: {}".format(nombres_botones[17], valor_boton_r2))

        text_print.unindent()
             
        # Hat switch
        hats = joystick.get_numhats()
        text_print.print(pantalla, "Número de hats: {}".format(hats))
        text_print.indent()
 
        for i in range(hats):
            hat = joystick.get_hat(i)
            text_print.print(pantalla, "Hat {} valor: {}".format(i, str(hat)))
        text_print.unindent()
         
        text_print.unindent()
 
    # Actualizamos la pantalla con lo que hemos dibujado.
    pygame.display.flip()
 
    # Limitamos a 60 fotogramas por segundo.
    reloj.tick(60)
     
pygame.quit()