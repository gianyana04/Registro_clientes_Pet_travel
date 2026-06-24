class Viaje:
    def __init__(self, cliente, pais_destino,
                 direccion_destino, codigo_postal,
                 telefono_destino, fecha_viaje):

        self.cliente = cliente
        self.pais_destino = pais_destino
        self.direccion_destino = direccion_destino
        self.codigo_postal = codigo_postal
        self.telefono_destino = telefono_destino
        self.fecha_viaje = fecha_viaje

    def mostrar_info(self):
        print("\n--- Datos del Viaje ---")
        print("Destino:", self.pais_destino)
        print("Fecha:", self.fecha_viaje)