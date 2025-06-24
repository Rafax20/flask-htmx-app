from dotenv import load_dotenv
import os
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ventanas.Login_Admin import Ui_MainWindow  # <- Este es tu archivo generado por pyuic5
from admin import VentanaAdmin

load_dotenv() # Carga las variables del .env

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ejecutar = Ui_MainWindow()
        self.ejecutar.setupUi(self)

# Conecta el botón a la función de verificación
        self.ejecutar.pushButton.clicked.connect(self.verificar_credenciales)

    def conectar_base(self):
    	url = os.environ.get("DATABASE_URL")
    	conn = psycopg2.connect(url)
    	return conn

    def verificar_credenciales(self):
    
        usuario = self.ejecutar.userText.text()
        contrasena = self.ejecutar.passwordText.text()
        try:
            conn = self.conectar_base()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM "Administradores"
                WHERE usuario = %s AND contrasena = %s
            """, (usuario, contrasena))

            if cursor.fetchone():
                QMessageBox.information(self, "Bienvenido", f"Acceso concedido, {usuario}")
                self.abrir_ventana_administrador()  # Este método lo defines tú
            else:
                QMessageBox.warning(self, "Acceso denegado", "Usuario o contraseña incorrectos")

            cursor.close()
            conn.close()

        except Exception as error:
            QMessageBox.critical(self, "Error de conexión", str(error))
    
    def abrir_ventana_administrador(self):
        self.admin = VentanaAdmin()
        self.admin.show()
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    ventana = Ventana()
    ventana.show()
    app.exec_()
