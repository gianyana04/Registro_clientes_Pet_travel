from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional


# =========================
# EXCEPCIONES PERSONALIZADAS
# =========================

class DniInvalidoError(Exception):
    pass


class RegistroDuplicadoError(Exception):
    pass


class RegistroNoEncontradoError(Exception):
    pass


class ValorInvalidoError(Exception):
    pass


# =========================
# CLASES DEL SISTEMA
# =========================

class Cliente:
    def __init__(self, dni: str, nombre: str, telefono: str, correo: str, direccion: str):
        self.dni: str = dni
        self.nombre: str = nombre
        self.telefono: str = telefono
        self.correo: str = correo
        self.direccion: str = direccion
        self.mascotas: List[Mascota] = []

    def mostrarDatos(self) -> str:
        return (
            f"DNI: {self.dni}\n"
            f"Nombre: {self.nombre}\n"
            f"Teléfono: {self.telefono}\n"
            f"Correo: {self.correo}\n"
            f"Dirección: {self.direccion}\n"
            f"Cantidad de mascotas: {len(self.mascotas)}\n"
        )


class Mascota:
    def __init__(self, codigo: str, nombre: str, especie: str, raza: str, edad: str, destino: str, dniCliente: str):
        self.codigo: str = codigo
        self.nombre: str = nombre
        self.especie: str = especie
        self.raza: str = raza
        self.edad: str = edad
        self.destino: str = destino
        self.dniCliente: str = dniCliente
        self.vacunas: List[Vacuna] = []
        self.documentos: List[Documento] = []
        self.pagos: List[Pago] = []

    def agregarVacuna(self, vacuna: Vacuna) -> None:
        self.vacunas.append(vacuna)

    def agregarDocumento(self, documento: Documento) -> None:
        self.documentos.append(documento)

    def agregarPago(self, pago: Pago) -> None:
        self.pagos.append(pago)

    def calcularTotalPagado(self) -> float:
        total: float = 0

        for pago in self.pagos:
            if pago.estado.upper() == "PAGADO":
                total += pago.monto

        return total

    def mostrarDatos(self) -> str:
        texto = (
            f"Código: {self.codigo}\n"
            f"Nombre: {self.nombre}\n"
            f"Especie: {self.especie}\n"
            f"Raza: {self.raza}\n"
            f"Edad: {self.edad}\n"
            f"Destino: {self.destino}\n"
            f"DNI del cliente: {self.dniCliente}\n"
            f"Total pagado: S/ {self.calcularTotalPagado()}\n"
        )

        texto += "\nVacunas:\n"
        if len(self.vacunas) == 0:
            texto += "No tiene vacunas registradas.\n"
        else:
            for vacuna in self.vacunas:
                texto += vacuna.mostrarDatos() + "\n"

        texto += "\nDocumentos:\n"
        if len(self.documentos) == 0:
            texto += "No tiene documentos registrados.\n"
        else:
            for documento in self.documentos:
                texto += documento.mostrarDatos() + "\n"

        texto += "\nPagos:\n"
        if len(self.pagos) == 0:
            texto += "No tiene pagos registrados.\n"
        else:
            for pago in self.pagos:
                texto += pago.mostrarDatos() + "\n"

        return texto


class Vacuna:
    def __init__(self, nombre: str, fecha: str, estado: str):
        self.nombre: str = nombre
        self.fecha: str = fecha
        self.estado: str = estado

    def mostrarDatos(self) -> str:
        return f"Vacuna: {self.nombre} | Fecha: {self.fecha} | Estado: {self.estado}"


class Documento:
    def __init__(self, nombre: str, estado: str):
        self.nombre: str = nombre
        self.estado: str = estado

    def mostrarDatos(self) -> str:
        return f"Documento: {self.nombre} | Estado: {self.estado}"


class Pago:
    def __init__(self, monto: float, fecha: str, concepto: str, estado: str):
        self.monto: float = monto
        self.fecha: str = fecha
        self.concepto: str = concepto
        self.estado: str = estado

    def mostrarDatos(self) -> str:
        return f"Monto: S/ {self.monto} | Fecha: {self.fecha} | Concepto: {self.concepto} | Estado: {self.estado}"


# =========================
# LISTAS PRINCIPALES
# =========================

clientes: List[Cliente] = []
mascotas: List[Mascota] = []


# =========================
# FUNCIONES AUXILIARES
# =========================

def datoOpcional(valor: str) -> str:
    if valor == "":
        return "No registrado"
    return valor


def validarDni(dni: str) -> None:
    if len(dni) != 8 or not dni.isdigit():
        raise DniInvalidoError("El DNI debe tener 8 dígitos numéricos.")


def buscarClientePorDni(dni: str) -> Optional[Cliente]:
    for cliente in clientes:
        if cliente.dni == dni:
            return cliente
    return None


def buscarMascotaPorCodigo(codigo: str) -> Optional[Mascota]:
    for mascota in mascotas:
        if mascota.codigo == codigo:
            return mascota
    return None


def limpiarCampos(campos: List[tk.Entry]) -> None:
    for campo in campos:
        campo.delete(0, tk.END)


def mostrarFrame(frame) -> None:
    # Ocultar todos los frames principales
    frameMenu.pack_forget()
    frameRegistrarCliente.pack_forget()
    frameRegistrarMascota.pack_forget()
    frameBuscarMascota.pack_forget()
    frameBuscarCliente.pack_forget()
    
    # Mostrar el frame solicitado
    frame.pack(fill="both", expand=True, padx=15, pady=15)


def volverAlMenu() -> None:
    mostrarFrame(frameMenu)


def mostrarResultadoMascota(texto: str) -> None:
    cajaResultadoMascota.delete("1.0", tk.END)
    cajaResultadoMascota.insert(tk.END, texto)


def mostrarResultadoCliente(texto: str) -> None:
    cajaResultadoCliente.delete("1.0", tk.END)
    cajaResultadoCliente.insert(tk.END, texto)


# =========================
# FUNCIONES DE REGISTRO
# =========================

def registrarCliente() -> None:
    try:
        dni: str = entradaDniCliente.get().strip()
        nombre: str = entradaNombreCliente.get().strip()
        telefono: str = entradaTelefonoCliente.get().strip()
        correo: str = entradaCorreoCliente.get().strip()
        direccion: str = entradaDireccionCliente.get().strip()

        validarDni(dni)

        if buscarClientePorDni(dni) is not None:
            raise RegistroDuplicadoError("Ya existe un cliente con ese DNI.")

        if nombre == "" or telefono == "":
            raise ValorInvalidoError("El nombre y el teléfono son obligatorios.")

        correo = datoOpcional(correo)
        direccion = datoOpcional(direccion)

        cliente = Cliente(dni, nombre, telefono, correo, direccion)
        clientes.append(cliente)

        messagebox.showinfo("Registro correcto", "Cliente registrado correctamente.")

        limpiarCampos([
            entradaDniCliente,
            entradaNombreCliente,
            entradaTelefonoCliente,
            entradaCorreoCliente,
            entradaDireccionCliente
        ])

    except Exception as error:
        messagebox.showerror("Error", str(error))


def registrarMascota() -> None:
    try:
        dniCliente: str = entradaDniClienteMascota.get().strip()
        codigo: str = entradaCodigoMascota.get().strip()
        nombre: str = entradaNombreMascota.get().strip()
        especie: str = entradaEspecieMascota.get().strip()
        raza: str = entradaRazaMascota.get().strip()
        edad: str = entradaEdadMascota.get().strip()
        destino: str = entradaDestinoMascota.get().strip()

        validarDni(dniCliente)

        cliente = buscarClientePorDni(dniCliente)

        if cliente is None:
            raise RegistroNoEncontradoError("No existe un cliente con ese DNI.")

        if codigo == "":
            raise ValorInvalidoError("El código de mascota es obligatorio.")

        if buscarMascotaPorCodigo(codigo) is not None:
            raise RegistroDuplicadoError("Ya existe una mascota con ese código.")

        if nombre == "" or especie == "" or destino == "":
            raise ValorInvalidoError("Nombre, especie y destino son obligatorios.")

        if edad != "" and not edad.isdigit():
            raise ValorInvalidoError("La edad debe ser un número entero.")

        raza = datoOpcional(raza)
        edad = datoOpcional(edad)

        mascota = Mascota(codigo, nombre, especie, raza, edad, destino, dniCliente)

        mascotas.append(mascota)
        cliente.mascotas.append(mascota)

        messagebox.showinfo("Registro correcto", "Mascota registrada correctamente.")

        limpiarCampos([
            entradaDniClienteMascota,
            entradaCodigoMascota,
            entradaNombreMascota,
            entradaEspecieMascota,
            entradaRazaMascota,
            entradaEdadMascota,
            entradaDestinoMascota
        ])

    except Exception as error:
        messagebox.showerror("Error", str(error))


def agregarVacuna() -> None:
    try:
        codigo: str = entradaCodigoVacuna.get().strip()
        nombre: str = entradaNombreVacuna.get().strip()
        fecha: str = entradaFechaVacuna.get().strip()
        estado: str = entradaEstadoVacuna.get().strip()

        mascota = buscarMascotaPorCodigo(codigo)

        if mascota is None:
            raise RegistroNoEncontradoError("No existe una mascota con ese código.")

        if nombre == "" or estado == "":
            raise ValorInvalidoError("El nombre y el estado de la vacuna son obligatorios.")

        fecha = datoOpcional(fecha)

        vacuna = Vacuna(nombre, fecha, estado)
        mascota.agregarVacuna(vacuna)

        messagebox.showinfo("Registro correcto", "Vacuna registrada correctamente.")

        limpiarCampos([
            entradaCodigoVacuna,
            entradaNombreVacuna,
            entradaFechaVacuna,
            entradaEstadoVacuna
        ])

    except Exception as error:
        messagebox.showerror("Error", str(error))


def agregarDocumento() -> None:
    try:
        codigo: str = entradaCodigoDocumento.get().strip()
        nombre: str = entradaNombreDocumento.get().strip()
        estado: str = entradaEstadoDocumento.get().strip()

        mascota = buscarMascotaPorCodigo(codigo)

        if mascota is None:
            raise RegistroNoEncontradoError("No existe una mascota con ese código.")

        if nombre == "" or estado == "":
            raise ValorInvalidoError("El nombre y el estado del documento son obligatorios.")

        documento = Documento(nombre, estado)
        mascota.agregarDocumento(documento)

        messagebox.showinfo("Registro correcto", "Documento registrado correctamente.")

        limpiarCampos([
            entradaCodigoDocumento,
            entradaNombreDocumento,
            entradaEstadoDocumento
        ])

    except Exception as error:
        messagebox.showerror("Error", str(error))


def agregarPago() -> None:
    try:
        codigo: str = entradaCodigoPago.get().strip()
        montoTexto: str = entradaMontoPago.get().strip()
        fecha: str = entradaFechaPago.get().strip()
        concepto: str = entradaConceptoPago.get().strip()
        estado: str = entradaEstadoPago.get().strip()

        mascota = buscarMascotaPorCodigo(codigo)

        if mascota is None:
            raise RegistroNoEncontradoError("No existe una mascota con ese código.")

        if montoTexto == "" or estado == "":
            raise ValorInvalidoError("El monto y el estado del pago son obligatorios.")

        monto: float = float(montoTexto)

        if monto < 0:
            raise ValorInvalidoError("El monto no puede ser negativo.")

        fecha = datoOpcional(fecha)
        concepto = datoOpcional(concepto)

        pago = Pago(monto, fecha, concepto, estado)
        mascota.agregarPago(pago)

        messagebox.showinfo("Registro correcto", "Pago registrado correctamente.")

        limpiarCampos([
            entradaCodigoPago,
            entradaMontoPago,
            entradaFechaPago,
            entradaConceptoPago,
            entradaEstadoPago
        ])

    except ValueError:
        messagebox.showerror("Error", "El monto debe ser un número.")

    except Exception as error:
        messagebox.showerror("Error", str(error))


# =========================
# FUNCIONES DE CONSULTA
# =========================

def listarClientes() -> None:
    if len(clientes) == 0:
        mostrarResultadoCliente("No hay clientes registrados.")
    else:
        texto = "LISTA DE CLIENTES\n"
        texto += "=================\n\n"

        for cliente in clientes:
            texto += cliente.mostrarDatos()
            texto += "-----------------------------\n"

        mostrarResultadoCliente(texto)


def listarMascotas() -> None:
    if len(mascotas) == 0:
        mostrarResultadoMascota("No hay mascotas registradas.")
    else:
        texto = "LISTA DE MASCOTAS\n"
        texto += "=================\n\n"

        for mascota in mascotas:
            texto += mascota.mostrarDatos()
            texto += "-----------------------------\n"

        mostrarResultadoMascota(texto)


def buscarMascota() -> None:
    codigo: str = entradaBuscarMascota.get().strip()

    if codigo == "":
        messagebox.showwarning("Advertencia", "Ingrese el código de la mascota.")
    else:
        mascota = buscarMascotaPorCodigo(codigo)

        if mascota is None:
            mostrarResultadoMascota("No se encontró una mascota con ese código.")
        else:
            mostrarResultadoMascota(mascota.mostrarDatos())
            # Auto-completar el código en las otras sub-pestañas
            limpiarCampos([entradaCodigoVacuna, entradaCodigoDocumento, entradaCodigoPago])
            entradaCodigoVacuna.insert(0, mascota.codigo)
            entradaCodigoDocumento.insert(0, mascota.codigo)
            entradaCodigoPago.insert(0, mascota.codigo)
            # Seleccionar la sub-pestaña de Detalles
            try:
                subPestanasMascota.select(0)
            except Exception:
                pass


def buscarCliente() -> None:
    dni: str = entradaBuscarCliente.get().strip()

    if dni == "":
        messagebox.showwarning("Advertencia", "Ingrese el DNI del cliente.")
    else:
        cliente = buscarClientePorDni(dni)

        if cliente is None:
            mostrarResultadoCliente("No se encontró un cliente con ese DNI.")
        else:
            texto = "DATOS DEL CLIENTE\n"
            texto += "=================\n\n"
            texto += cliente.mostrarDatos()
            if len(cliente.mascotas) > 0:
                texto += "\nMascotas asociadas:\n"
                for mascota in cliente.mascotas:
                    texto += f"- Código: {mascota.codigo} | Nombre: {mascota.nombre} | Especie: {mascota.especie}\n"
            else:
                texto += "\nNo tiene mascotas asociadas.\n"
            mostrarResultadoCliente(texto)


# =========================
# DATOS DE PRUEBA
# =========================

def cargarDatosDePrueba() -> None:
    cliente1 = Cliente("12345678", "Juan Pérez", "987654321", "juan@gmail.com", "Av. Lima 123")
    cliente2 = Cliente("87654321", "María López", "912345678", "No registrado", "Jr. Real 456")

    clientes.append(cliente1)
    clientes.append(cliente2)

    mascota1 = Mascota("M001", "Bobby", "Perro", "Golden Retriever", "4", "España", "12345678")
    mascota2 = Mascota("M002", "Michi", "Gato", "Persa", "2", "Chile", "87654321")

    mascotas.append(mascota1)
    mascotas.append(mascota2)

    cliente1.mascotas.append(mascota1)
    cliente2.mascotas.append(mascota2)

    mascota1.agregarVacuna(Vacuna("Rabia", "10/05/2026", "Aplicada"))
    mascota1.agregarDocumento(Documento("Certificado sanitario", "Completo"))
    mascota1.agregarPago(Pago(500, "12/05/2026", "Adelanto", "Pagado"))

    mascota2.agregarVacuna(Vacuna("Triple felina", "No registrado", "Pendiente"))
    mascota2.agregarDocumento(Documento("Permiso de viaje", "Pendiente"))
    mascota2.agregarPago(Pago(300, "15/05/2026", "Reserva", "Pagado"))


# =========================
# INTERFAZ GRÁFICA
# =========================

ventana = tk.Tk()
ventana.title("Sistema Pet Travel")
ventana.geometry("900x680")

titulo = tk.Label(ventana, text="SISTEMA PET TRAVEL", font=("Arial", 18, "bold"))
titulo.pack(pady=10)

subtitulo = tk.Label(ventana, text="Los campos con * son obligatorios")
subtitulo.pack()

# =========================
# CREACIÓN DE FRAMES PRINCIPALES
# =========================

frameMenu = tk.Frame(ventana)
frameRegistrarCliente = tk.Frame(ventana)
frameRegistrarMascota = tk.Frame(ventana)
frameBuscarMascota = tk.Frame(ventana)
frameBuscarCliente = tk.Frame(ventana)


# =========================
# DISEÑO DE MENÚ PRINCIPAL
# =========================

tk.Label(frameMenu, text="MENÚ PRINCIPAL", font=("Arial", 14, "bold"), fg="#37474f").pack(pady=15)

btn_width = 30
btn_font = ("Arial", 12, "bold")

tk.Button(
    frameMenu, 
    text="Registrar Cliente", 
    font=btn_font, 
    width=btn_width, 
    height=2, 
    bg="#e3f2fd", 
    fg="#0d47a1", 
    activebackground="#bbdefb", 
    command=lambda: mostrarFrame(frameRegistrarCliente)
).pack(pady=10)

tk.Button(
    frameMenu, 
    text="Registrar Mascota", 
    font=btn_font, 
    width=btn_width, 
    height=2, 
    bg="#e8f5e9", 
    fg="#1b5e20", 
    activebackground="#c8e6c9", 
    command=lambda: mostrarFrame(frameRegistrarMascota)
).pack(pady=10)

tk.Button(
    frameMenu, 
    text="Buscar Mascota", 
    font=btn_font, 
    width=btn_width, 
    height=2, 
    bg="#fff3e0", 
    fg="#e65100", 
    activebackground="#ffe0b2", 
    command=lambda: mostrarFrame(frameBuscarMascota)
).pack(pady=10)

tk.Button(
    frameMenu, 
    text="Buscar Cliente", 
    font=btn_font, 
    width=btn_width, 
    height=2, 
    bg="#f3e5f5", 
    fg="#4a148c", 
    activebackground="#e1bee7", 
    command=lambda: mostrarFrame(frameBuscarCliente)
).pack(pady=10)

tk.Button(
    frameMenu, 
    text="Salir", 
    font=btn_font, 
    width=btn_width, 
    height=2, 
    bg="#ffebee", 
    fg="#b71c1c", 
    activebackground="#ffcdd2", 
    command=ventana.destroy
).pack(pady=10)


# =========================
# DISEÑO REGISTRAR CLIENTE
# =========================

tk.Label(frameRegistrarCliente, text="REGISTRAR NUEVO CLIENTE", font=("Arial", 14, "bold"), fg="#0d47a1").pack(pady=10)

formCliente = tk.Frame(frameRegistrarCliente)
formCliente.pack(pady=10)

tk.Label(formCliente, text="DNI *:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entradaDniCliente = tk.Entry(formCliente, width=40)
entradaDniCliente.grid(row=0, column=1, padx=10, pady=5)

tk.Label(formCliente, text="Nombre completo *:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entradaNombreCliente = tk.Entry(formCliente, width=40)
entradaNombreCliente.grid(row=1, column=1, padx=10, pady=5)

tk.Label(formCliente, text="Teléfono *:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entradaTelefonoCliente = tk.Entry(formCliente, width=40)
entradaTelefonoCliente.grid(row=2, column=1, padx=10, pady=5)

tk.Label(formCliente, text="Correo:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entradaCorreoCliente = tk.Entry(formCliente, width=40)
entradaCorreoCliente.grid(row=3, column=1, padx=10, pady=5)

tk.Label(formCliente, text="Dirección:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entradaDireccionCliente = tk.Entry(formCliente, width=40)
entradaDireccionCliente.grid(row=4, column=1, padx=10, pady=5)

btnFrameCliente = tk.Frame(frameRegistrarCliente)
btnFrameCliente.pack(pady=15)

tk.Button(btnFrameCliente, text="Registrar cliente", font=("Arial", 10, "bold"), bg="#4caf50", fg="white", activebackground="#388e3c", command=registrarCliente).pack(side="left", padx=10)
tk.Button(btnFrameCliente, text="Volver al Menú", font=("Arial", 10), bg="#9e9e9e", fg="white", activebackground="#757575", command=volverAlMenu).pack(side="left", padx=10)


# =========================
# DISEÑO REGISTRAR MASCOTA
# =========================

tk.Label(frameRegistrarMascota, text="REGISTRAR NUEVA MASCOTA", font=("Arial", 14, "bold"), fg="#1b5e20").pack(pady=10)

formMascota = tk.Frame(frameRegistrarMascota)
formMascota.pack(pady=10)

tk.Label(formMascota, text="DNI del cliente *:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entradaDniClienteMascota = tk.Entry(formMascota, width=40)
entradaDniClienteMascota.grid(row=0, column=1, padx=10, pady=5)

tk.Label(formMascota, text="Código de mascota *:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entradaCodigoMascota = tk.Entry(formMascota, width=40)
entradaCodigoMascota.grid(row=1, column=1, padx=10, pady=5)

tk.Label(formMascota, text="Nombre *:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entradaNombreMascota = tk.Entry(formMascota, width=40)
entradaNombreMascota.grid(row=2, column=1, padx=10, pady=5)

tk.Label(formMascota, text="Especie *:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entradaEspecieMascota = tk.Entry(formMascota, width=40)
entradaEspecieMascota.grid(row=3, column=1, padx=10, pady=5)

tk.Label(formMascota, text="Raza:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entradaRazaMascota = tk.Entry(formMascota, width=40)
entradaRazaMascota.grid(row=4, column=1, padx=10, pady=5)

tk.Label(formMascota, text="Edad:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
entradaEdadMascota = tk.Entry(formMascota, width=40)
entradaEdadMascota.grid(row=5, column=1, padx=10, pady=5)

tk.Label(formMascota, text="Destino de viaje *:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
entradaDestinoMascota = tk.Entry(formMascota, width=40)
entradaDestinoMascota.grid(row=6, column=1, padx=10, pady=5)

btnFrameMascota = tk.Frame(frameRegistrarMascota)
btnFrameMascota.pack(pady=15)

tk.Button(btnFrameMascota, text="Registrar mascota", font=("Arial", 10, "bold"), bg="#4caf50", fg="white", activebackground="#388e3c", command=registrarMascota).pack(side="left", padx=10)
tk.Button(btnFrameMascota, text="Volver al Menú", font=("Arial", 10), bg="#9e9e9e", fg="white", activebackground="#757575", command=volverAlMenu).pack(side="left", padx=10)


# =========================
# DISEÑO BUSCAR MASCOTA Y GESTIÓN
# =========================

tk.Label(frameBuscarMascota, text="BÚSQUEDA Y GESTIÓN DE MASCOTAS", font=("Arial", 14, "bold"), fg="#e65100").pack(pady=10)

# Buscador superior
searchFrameMascota = tk.Frame(frameBuscarMascota)
searchFrameMascota.pack(fill="x", pady=5)

tk.Label(searchFrameMascota, text="Código de mascota:").pack(side="left", padx=5)
entradaBuscarMascota = tk.Entry(searchFrameMascota, width=15)
entradaBuscarMascota.pack(side="left", padx=5)

tk.Button(searchFrameMascota, text="Buscar", bg="#e65100", fg="white", activebackground="#f57c00", command=buscarMascota).pack(side="left", padx=5)
tk.Button(searchFrameMascota, text="Listar todas", bg="#2196f3", fg="white", activebackground="#1976d2", command=listarMascotas).pack(side="left", padx=5)
tk.Button(searchFrameMascota, text="Volver al Menú", bg="#9e9e9e", fg="white", activebackground="#757575", command=volverAlMenu).pack(side="right", padx=5)

# Sub-Notebook para organizar los detalles y los registros adicionales
subPestanasMascota = ttk.Notebook(frameBuscarMascota)
subPestanasMascota.pack(fill="both", expand=True, pady=10)

# Sub-pestaña 1: Detalles de Mascota
pestanaDetalles = tk.Frame(subPestanasMascota)
subPestanasMascota.add(pestanaDetalles, text="Detalles / Lista")

cajaResultadoMascota = tk.Text(pestanaDetalles, width=95, height=20)
cajaResultadoMascota.pack(fill="both", expand=True, padx=5, pady=5)

# Sub-pestaña 2: Agregar Vacuna
pestanaVacuna = tk.Frame(subPestanasMascota)
subPestanasMascota.add(pestanaVacuna, text="Registrar Vacuna")

formVacuna = tk.Frame(pestanaVacuna)
formVacuna.pack(pady=10)

tk.Label(formVacuna, text="Código de mascota *:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entradaCodigoVacuna = tk.Entry(formVacuna, width=40)
entradaCodigoVacuna.grid(row=0, column=1, padx=10, pady=5)

tk.Label(formVacuna, text="Nombre de vacuna *:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entradaNombreVacuna = tk.Entry(formVacuna, width=40)
entradaNombreVacuna.grid(row=1, column=1, padx=10, pady=5)

tk.Label(formVacuna, text="Fecha:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entradaFechaVacuna = tk.Entry(formVacuna, width=40)
entradaFechaVacuna.grid(row=2, column=1, padx=10, pady=5)

tk.Label(formVacuna, text="Estado *:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entradaEstadoVacuna = tk.Entry(formVacuna, width=40)
entradaEstadoVacuna.grid(row=3, column=1, padx=10, pady=5)

tk.Button(pestanaVacuna, text="Agregar vacuna", font=("Arial", 10, "bold"), bg="#4caf50", fg="white", activebackground="#388e3c", command=agregarVacuna).pack(pady=10)

# Sub-pestaña 3: Agregar Documento
pestanaDocumento = tk.Frame(subPestanasMascota)
subPestanasMascota.add(pestanaDocumento, text="Registrar Documento")

formDocumento = tk.Frame(pestanaDocumento)
formDocumento.pack(pady=10)

tk.Label(formDocumento, text="Código de mascota *:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entradaCodigoDocumento = tk.Entry(formDocumento, width=40)
entradaCodigoDocumento.grid(row=0, column=1, padx=10, pady=5)

tk.Label(formDocumento, text="Nombre de documento *:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entradaNombreDocumento = tk.Entry(formDocumento, width=40)
entradaNombreDocumento.grid(row=1, column=1, padx=10, pady=5)

tk.Label(formDocumento, text="Estado *:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entradaEstadoDocumento = tk.Entry(formDocumento, width=40)
entradaEstadoDocumento.grid(row=2, column=1, padx=10, pady=5)

tk.Button(pestanaDocumento, text="Agregar documento", font=("Arial", 10, "bold"), bg="#4caf50", fg="white", activebackground="#388e3c", command=agregarDocumento).pack(pady=10)

# Sub-pestaña 4: Agregar Pago
pestanaPago = tk.Frame(subPestanasMascota)
subPestanasMascota.add(pestanaPago, text="Registrar Pago")

formPago = tk.Frame(pestanaPago)
formPago.pack(pady=10)

tk.Label(formPago, text="Código de mascota *:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entradaCodigoPago = tk.Entry(formPago, width=40)
entradaCodigoPago.grid(row=0, column=1, padx=10, pady=5)

tk.Label(formPago, text="Monto *:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entradaMontoPago = tk.Entry(formPago, width=40)
entradaMontoPago.grid(row=1, column=1, padx=10, pady=5)

tk.Label(formPago, text="Fecha:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entradaFechaPago = tk.Entry(formPago, width=40)
entradaFechaPago.grid(row=2, column=1, padx=10, pady=5)

tk.Label(formPago, text="Concepto:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entradaConceptoPago = tk.Entry(formPago, width=40)
entradaConceptoPago.grid(row=3, column=1, padx=10, pady=5)

tk.Label(formPago, text="Estado *:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entradaEstadoPago = tk.Entry(formPago, width=40)
entradaEstadoPago.grid(row=4, column=1, padx=10, pady=5)

tk.Button(pestanaPago, text="Agregar pago", font=("Arial", 10, "bold"), bg="#4caf50", fg="white", activebackground="#388e3c", command=agregarPago).pack(pady=10)


# =========================
# DISEÑO BUSCAR CLIENTE
# =========================

tk.Label(frameBuscarCliente, text="BÚSQUEDA Y CONSULTA DE CLIENTES", font=("Arial", 14, "bold"), fg="#4a148c").pack(pady=10)

# Buscador superior
searchFrameCliente = tk.Frame(frameBuscarCliente)
searchFrameCliente.pack(fill="x", pady=5)

tk.Label(searchFrameCliente, text="DNI del cliente:").pack(side="left", padx=5)
entradaBuscarCliente = tk.Entry(searchFrameCliente, width=15)
entradaBuscarCliente.pack(side="left", padx=5)

tk.Button(searchFrameCliente, text="Buscar", bg="#4a148c", fg="white", activebackground="#7b1fa2", command=buscarCliente).pack(side="left", padx=5)
tk.Button(searchFrameCliente, text="Listar todos", bg="#2196f3", fg="white", activebackground="#1976d2", command=listarClientes).pack(side="left", padx=5)
tk.Button(searchFrameCliente, text="Volver al Menú", bg="#9e9e9e", fg="white", activebackground="#757575", command=volverAlMenu).pack(side="right", padx=5)

cajaResultadoCliente = tk.Text(frameBuscarCliente, width=95, height=22)
cajaResultadoCliente.pack(fill="both", expand=True, padx=5, pady=10)


# =========================
# EJECUCIÓN DEL PROGRAMA
# =========================

cargarDatosDePrueba()
mostrarFrame(frameMenu)
ventana.mainloop()