import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont
import facturacion  # Importa el archivo facturacion.py que contiene la clase FacturacionApp
import inventario  # Importa el archivo inventario.py
import registro_de_clientes  # Importa el archivo registro_clientes.py
import ventas  # Importa el archivo ventas.py 

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("MenuPrincipal")
        self.resize(500, 600)
        self.setStyleSheet("background-color: rgb(173, 216, 230);")
        self.centralwidget = QWidget(self)
        
        # Título del menú principal
        self.lblTitulo = QLabel("Menú Principal", self.centralwidget)
        self.lblTitulo.setGeometry(QRect(0, 50, 500, 80))
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.lblTitulo.setFont(font)
        self.lblTitulo.setStyleSheet("color: rgb(12, 11, 13);")
        self.lblTitulo.setAlignment(Qt.AlignCenter)

        # Botón para ir a la ventana de facturación
        self.btnFacturacion = QPushButton("Ir a Facturación", self.centralwidget)
        self.btnFacturacion.setGeometry(QRect(150, 200, 200, 50))
        self.btnFacturacion.setStyleSheet("background-color: rgb(10, 10, 10); color: white; font-size: 16px;")
        self.btnFacturacion.clicked.connect(self.abrir_facturacion)

        # Botón para ir a la ventana de inventario
        self.btnInventario = QPushButton("Ir a Inventario", self.centralwidget)
        self.btnInventario.setGeometry(QRect(150, 280, 200, 50))
        self.btnInventario.setStyleSheet("background-color: rgb(10, 10, 10); color: white; font-size: 16px;")
        self.btnInventario.clicked.connect(self.abrir_inventario)

        # Botón para registro de clientes
        self.btnRegistroClientes = QPushButton("Registro de Clientes", self.centralwidget)
        self.btnRegistroClientes.setGeometry(QRect(150, 360, 200, 50))
        self.btnRegistroClientes.setStyleSheet("background-color: rgb(10, 10, 10); color: white; font-size: 16px;")
        self.btnRegistroClientes.clicked.connect(self.registro_clientes)

        # Botón para ventas
        self.btnVentas = QPushButton("Ventas", self.centralwidget)
        self.btnVentas.setGeometry(QRect(150, 440, 200, 50))
        self.btnVentas.setStyleSheet("background-color: rgb(10, 10, 10); color: white; font-size: 16px;")
        self.btnVentas.clicked.connect(self.ventas)

        # Configurar el widget central
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("Menú Principal - CandyVoyage")

    def abrir_facturacion(self):
        """Abre la ventana de facturación y oculta el menú principal."""
        self.facturacion_window = facturacion.FacturacionApp()  # Crear instancia de FacturacionApp
        self.facturacion_window.show()
        self.hide()  # Ocultar el menú principal mientras se muestra la ventana de facturación

    def abrir_inventario(self):
        """Abre la ventana de inventario y oculta el menú principal."""
        self.inventario_window = inventario.InventarioApp()  # Crear instancia de InventarioApp
        self.inventario_window.show()
        self.hide()  # Ocultar el menú principal mientras se muestra la ventana de inventario

    def registro_clientes(self):
        """Abre la ventana de registro de clientes y oculta el menú principal."""
        self.registro_clientes_window = registro_de_clientes.ClientesApp()  # Crear instancia de RegistroClientesApp
        self.registro_clientes_window.show()
        self.hide()  # Ocultar el menú principal mientras se muestra la ventana de registro de clientes

    def ventas(self):
        """Abre la ventana de ventas y oculta el menú principal."""
        self.ventas_window = ventas.VentaApp()  # Crear instancia de VentasApp
        self.ventas_window.show()
        self.hide()  # Ocultar el menú principal mientras se muestra la ventana de ventas

    def closeEvent(self, event):
        """Cierra la aplicación cuando se cierra el menú principal."""
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = MainWindow()
    ventana_principal.show()
    sys.exit(app.exec_())

