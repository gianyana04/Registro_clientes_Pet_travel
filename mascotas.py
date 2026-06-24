class Mascota:
    def __init__(self, nombre, especie, raza, sexo,
                 fecha_nacimiento, color, microchip, esterilizada):
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.color = color
        self.microchip = microchip
        self.esterilizada = esterilizada

    def mostrar_info(self):
        print("\n--- Datos de la Mascota ---")
        print("Nombre:", self.nombre)
        print("Especie:", self.especie)
        print("Raza:", self.raza)
        print("Sexo:", self.sexo)
        print("Fecha nacimiento:", self.fecha_nacimiento)
        print("Color:", self.color)
        print("Microchip:", self.microchip)
        print("Esterilizada:", self.esterilizada)
