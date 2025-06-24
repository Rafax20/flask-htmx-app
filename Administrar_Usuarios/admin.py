from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractScrollArea, QPushButton, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
from ventanas.Ventana_Admin import Ui_MainWindow
from cuadro_agregar import VentanaAgregar
from crud import obtener_usuarios, eliminar_usuario, editar_usuario

class VentanaAdmin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cargar_usuarios()
        self.ui.boton_Actualizar.clicked.connect(self.cargar_usuarios)
        self.ui.boton_Agregar.clicked.connect(self.abrir_dialogo_agregar)

    def abrir_dialogo_agregar(self):
        dialogo = VentanaAgregar(self)
        if dialogo.exec_():
            self.cargar_usuarios()

    def cargar_usuarios(self):
        resultados, headers = obtener_usuarios()

        if resultados:
            self.ui.tablaUsuarios.setColumnCount(len(headers) + 2)
            self.ui.tablaUsuarios.setHorizontalHeaderLabels(headers + [""] + [""])
            self.ui.tablaUsuarios.setRowCount(len(resultados))
            self.ui.tablaUsuarios.setColumnWidth(0, 30)
            self.ui.tablaUsuarios.setColumnWidth(1, 90)
            self.ui.tablaUsuarios.setColumnWidth(2, 230)  # Ajusta según tus pruebas
            self.ui.tablaUsuarios.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        for i, fila in enumerate(resultados):
            for j, valor in enumerate(fila):
                self.ui.tablaUsuarios.setItem(i, j, QTableWidgetItem(str(valor)))

            id_usuario = fila[0]
            # Botón con ícono de lapiz
            boton_editar = QPushButton()
            boton_editar.setIcon(QIcon("iconos/lapiz.png"))
            boton_editar.setToolTip("Editar este usuario")

            # Necesitamos capturar el ID de esta fila
            boton_editar.clicked.connect(lambda _, id=id_usuario: self.editar_usuario(id))
            self.ui.tablaUsuarios.setCellWidget(i, len(headers), boton_editar)

            # Botón con ícono ❌
            boton_eliminar = QPushButton()
            boton_eliminar.setIcon(QIcon("iconos/x.png"))  # Usa tu propio ícono si tienes uno
            boton_eliminar.setToolTip("Eliminar este usuario")

            # Necesitamos capturar el ID de esta fila
            boton_eliminar.clicked.connect(lambda _, id=id_usuario: self.confirmar_eliminacion(id))

            self.ui.tablaUsuarios.setCellWidget(i, len(headers) + 1, boton_eliminar)

    def editar_usuario(self, id_usuario):
        # Obtener el nombre actual de la fila seleccionada (columna 1)
        for fila in range(self.ui.tablaUsuarios.rowCount()):
            id_actual = int(self.ui.tablaUsuarios.item(fila, 0).text())
            if id_actual == id_usuario:
                nombre_actual = self.ui.tablaUsuarios.item(fila, 1).text()
                break

        # Crear diálogo de entrada
        nuevo_nombre, ok = QInputDialog.getText(self, "Editar usuario",
                                            f"Nombre actual: {nombre_actual}\nNuevo nombre:",
                                            QLineEdit.Normal, nombre_actual)
        if ok and nuevo_nombre.strip():
            editar_usuario(id_usuario, nuevo_nombre.strip())
            QMessageBox.information(self, "Usuario editado", f"Nombre actualizado a '{nuevo_nombre.strip()}'")
            self.cargar_usuarios()

    def confirmar_eliminacion(self, id_usuario):
        respuesta = QMessageBox.question(self, "Confirmar eliminación",
                                     f"¿Estás seguro de eliminar el usuario con ID {id_usuario}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            eliminar_usuario(id_usuario)
            self.cargar_usuarios()


