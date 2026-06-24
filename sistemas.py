from clientes import Cliente
from mascotas import Mascota
from viajes import Viaje


class SistemaPetTravel:

    def __init__(self):
        self.registros = []

    def registrar_cliente(self):

        nombre = input("Nombre completo: ")
        documento = input("Documento: ")
        direccion = input("Dirección: ")
        telefono = input("Teléfono: ")
        correo = input("Correo: ")

        cliente = Cliente(
            nombre,
            documento,
            direccion,
            telefono,
            correo
        )

        nombre_mascota = input("Nombre mascota: ")
        especie = input("Especie: ")
        raza = input("Raza: ")
        sexo = input("Sexo: ")
        fecha = input("Fecha nacimiento: ")
        color = input("Color: ")
        microchip = input("Microchip: ")
        esterilizada = input("Esterilizada: ")

        mascota = Mascota(
            nombre_mascota,
            especie,
            raza,
            sexo,
            fecha,
            color,
            microchip,
            esterilizada
        )

        cliente.agregar_mascota(mascota)

        pais = input("País destino: ")
        direccion_destino = input("Dirección destino: ")
        codigo = input("Código postal: ")
        telefono_destino = input("Teléfono destino: ")
        fecha_viaje = input("Fecha viaje: ")

        viaje = Viaje(
            cliente,
            pais,
            direccion_destino,
            codigo,
            telefono_destino,
            fecha_viaje
        )

        self.registros.append(viaje)

        print("Registro guardado correctamente.")

    def mostrar_registros(self):

        for registro in self.registros:

            registro.cliente.mostrar_info()

            for mascota in registro.cliente.mascotas:
                mascota.mostrar_info()

            registro.mostrar_info()

    def menu(self):

        while True:

            print("\n===== PET TRAVEL =====")
            print("1. Registrar cliente")
            print("2. Mostrar registros")
            print("3. Salir")

            opcion = input("Seleccione: ")

            if opcion == "1":
                self.registrar_cliente()

            elif opcion == "2":
                self.mostrar_registros()

            elif opcion == "3":
                break

            else:
                print("Opción inválida")