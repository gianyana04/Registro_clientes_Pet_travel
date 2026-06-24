class Cliente:
    def __init__(self, nombre, documento,
                 direccion_peru, telefono_peru, correo):
        self.nombre = nombre
        self.documento = documento
        self.direccion_peru = direccion_peru
        self.telefono_peru = telefono_peru
        self.correo = correo
        self.mascotas = []

    def agregar_mascota(self, mascota):
        self.mascotas.append(mascota)

    def mostrar_info(self):
        print("\n--- Datos del Cliente ---")
        print("Nombre:", self.nombre)
        print("Documento:", self.documento)