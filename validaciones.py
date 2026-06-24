from datetime import datetime


def pedir_fecha(mensaje):
    while True:
        valor = input(mensaje).strip()
        try:
            datetime.strptime(valor, "%d/%m/%Y")
            return valor
        except ValueError:
            print("Fecha inválida. Use el formato DD/MM/AAAA (ej: 15/03/2020).")


def pedir_telefono(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and len(valor) >= 7:
            return valor
        print("Teléfono inválido. Ingrese solo números (mínimo 7 dígitos).")


def pedir_si_no(mensaje):
    while True:
        valor = input(mensaje).strip().lower()
        if valor in ("si", "sí", "s"):
            return "Si"
        if valor in ("no", "n"):
            return "No"
        print("Respuesta inválida. Ingrese Si o No.")
