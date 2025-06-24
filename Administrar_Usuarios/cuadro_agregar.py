from PyQt5.QtWidgets import QDialog, QMessageBox
from ventanas.ventana_agregar import Ui_Dialog
from crud import agregar_usuario

class VentanaAgregar(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Conectar la acción del botón "OK"
        self.ui.buttonBox.accepted.connect(self.procesar_agregado)
        self.ui.buttonBox.rejected.connect(self.reject)

    def procesar_agregado(self):
        nombre = self.ui.inputNombreNuevo.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Campo vacío", "Por favor ingresa un nombre.")
            return

        agregar_usuario(nombre)
        QMessageBox.information(self, "Usuario agregado", f"Usuario '{nombre}' registrado exitosamente.")
        self.accept()
