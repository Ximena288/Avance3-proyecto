import sys
import os
import smtplib
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from dotenv import load_dotenv
load_dotenv()

remit = os.getenv('CORREO')
serv = os.getenv('SERV')
puerto = os.getenv('PUERTO')
contra = os.getenv('CONTRA')

# Verificar si las variables se cargan correctamente
if not all([remit, serv, puerto, contra]):
    print("Error: No se pudieron cargar todas las variables de entorno.")
    print(f"CORREO: {remit}, SERV: {serv}, PUERTO: {puerto}, CONTRA: {contra}")
    exit(1)  # Salir del programa si faltan variables

# Convertir puerto a entero
try:
    puerto = int(puerto)
except ValueError:
    print(f"Error: PUERTO no es un número válido. Valor obtenido: {puerto}")
    exit(1)


# Conectar a la base de datos SQLite
conn = sqlite3.connect('Candyvoyage.db')
cursor = conn.cursor()

class FacturacionApp(QMainWindow):
    def __init__(self):
        super(FacturacionApp, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("CandyVoyage")
        self.resize(466, 750)
        self.setStyleSheet("background-color: rgb(237, 159, 172);")
        self.centralwidget = QWidget(self)
        
        # Layout principal
        main_layout = QVBoxLayout(self.centralwidget)

        # Label para el nombre de la Tienda
        self.lblEmpresa = QLabel("CandyVoyage", self.centralwidget)
        font = QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(16)
        self.lblEmpresa.setFont(font)
        self.lblEmpresa.setStyleSheet("background-color: rgb(245, 213, 231); font: 63 16pt 'Yu Gothic UI Semibold';")
        self.lblEmpresa.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lblEmpresa)

        # ComboBox para seleccionar el producto
        self.cmbProducto = QComboBox(self.centralwidget)
        self.cmbProducto.setStyleSheet("background-color: rgb(237, 159, 172); font: 14pt 'MS Shell Dlg 2';")
        self.cmbProducto.addItems([
            "Dulce cafe $1.00", "Chocolate kiss $1.50", "Marsmello $0.75", 
            "Chicle frutal $0.25", "Caramelo ácido $0.50", "Gomitas $1.20", 
            "Paleta de frutas $0.80", "Barra de chocolate $2.00"
        ])

        # Campo de entrada para cantidad
        self.txtCantidad = QLineEdit(self.centralwidget)
        self.txtCantidad.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.txtCantidad.setPlaceholderText("Cantidad")

        # Layout para producto y cantidad
        product_layout = QGridLayout()
        product_layout.addWidget(QLabel("Producto:"), 0, 0)
        product_layout.addWidget(self.cmbProducto, 0, 1)
        product_layout.addWidget(QLabel("Cantidad:"), 1, 0)
        product_layout.addWidget(self.txtCantidad, 1, 1)
        main_layout.addLayout(product_layout)

        # Botón para agregar productos
        self.btnAgregarProducto = QPushButton("Agregar Producto", self.centralwidget)
        self.btnAgregarProducto.setStyleSheet("background-color: rgb(255, 255, 102);")
        self.btnAgregarProducto.clicked.connect(self.agregar_producto)
        main_layout.addWidget(self.btnAgregarProducto)

        # Label para mostrar el total
        self.lblTotal = QLabel("Cuenta: $0.00", self.centralwidget)
        self.lblTotal.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lblTotal.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lblTotal)

        # Campo para el dinero recibido del cliente
        self.txtPagoCliente = QLineEdit(self.centralwidget)
        self.txtPagoCliente.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.txtPagoCliente.setPlaceholderText("Dinero recibido del cliente")
        main_layout.addWidget(self.txtPagoCliente)

        # Label para el cambio
        self.lblCambio = QLabel("Cambio: $0.00", self.centralwidget)
        self.lblCambio.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lblCambio.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lblCambio)

        # Botón para calcular el total y el cambio
        self.btnCalcular = QPushButton("Calcular Total y Cambio", self.centralwidget)
        self.btnCalcular.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.btnCalcular.clicked.connect(self.calcular_total)
        main_layout.addWidget(self.btnCalcular)

        # Campo para dirección de correo del cliente
        self.txtCorreoCliente = QLineEdit(self.centralwidget)
        self.txtCorreoCliente.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.txtCorreoCliente.setPlaceholderText("Correo del cliente")
        main_layout.addWidget(self.txtCorreoCliente)

        # Botón para enviar el recibo
        self.btnEnviarRecibo = QPushButton("Enviar Recibo", self.centralwidget)
        self.btnEnviarRecibo.setStyleSheet("background-color: rgb(255, 170, 0);")
        self.btnEnviarRecibo.clicked.connect(self.enviar_recibo)
        main_layout.addWidget(self.btnEnviarRecibo)


        # Configurar el widget central y ventana
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("CandyVoyage")

    def agregar_producto(self):
        producto = self.cmbProducto.currentText()
        cantidad_texto = self.txtCantidad.text()
        
        try:
            cantidad = int(cantidad_texto)
            if cantidad <= 0:
                self.lblTotal.setText("Cantidad debe ser mayor a 0")
                return
        except ValueError:
            self.lblTotal.setText("Cantidad inválida")
            return
        
        precios = {
            "Dulce cafe $1.00": 1.00,
            "Chocolate kiss $1.50": 1.50,
            "Marsmello $0.75": 0.75,
            "Chicle frutal $0.25": 0.25,
            "Caramelo ácido $0.50": 0.50,
            "Gomitas $1.20": 1.20,
            "Paleta de frutas $0.80": 0.80,
            "Barra de chocolate $2.00": 2.00
        }
        precio = precios.get(producto, 0)
        total_producto = precio * cantidad
        self.lblTotal.setText(f"Cuenta: ${total_producto:.2f}")

    def calcular_total(self):
        try:
            pago_cliente = float(self.txtPagoCliente.text())
            total = float(self.lblTotal.text().split(": $")[-1])
            cambio = pago_cliente - total
            if cambio < 0:
                self.lblCambio.setText("Cambio: Pago insuficiente")
            else:
                self.lblCambio.setText(f"Cambio: ${cambio:.2f}")
        except ValueError:
            self.lblCambio.setText("Cambio: Ingrese un pago válido")

    def enviar_recibo(self):
        correo_cliente = self.txtCorreoCliente.text()
        if not correo_cliente:
            print("Por favor ingrese un correo válido.")
            return

        total = self.lblTotal.text().split(": $")[-1]
        cambio = self.lblCambio.text().split(": $")[-1]

        mensaje = MIMEMultipart()
        mensaje['From'] = remit
        mensaje['To'] = correo_cliente
        mensaje['Subject'] = "Recibo de compra - CandyVoyage"
        
        cuerpo = f"Gracias por su compra.\nTotal de la cuenta: ${total}\nCambio: ${cambio}\n¡MUCHAS GRACIAS POR TU COMPRA!"
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        try:
            if puerto == 465:
                with smtplib.SMTP_SSL(serv, puerto) as server:
                    server.login(remit, contra)
                    server.sendmail(remit, correo_cliente, mensaje.as_string())
            else:
                with smtplib.SMTP(serv, puerto) as server:
                    server.starttls()
                    server.login(remit, contra)
                    server.sendmail(remit, correo_cliente, mensaje.as_string())

            print("Recibo enviado correctamente.")
        except smtplib.SMTPException as e:
            print(f"Error al enviar el recibo: {e}")

    def regresar_menu(self):
        print("Volviendo al menú principal...")
        # Aquí podrías agregar la lógica para regresar al menú principal de tu aplicación.

    def closeEvent(self, event):
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FacturacionApp()
    ventana.show()
    sys.exit(app.exec_()) 
