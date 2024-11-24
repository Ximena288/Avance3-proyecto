from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton, QCheckBox, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class VentaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Venta de Productos")
        self.setGeometry(100, 100, 600, 600)

        # Cambiar el color de la ventana a lila
        self.setStyleSheet("background-color: #D8B7DD;")  # Lila claro

        # Layout principal
        layout = QVBoxLayout()

        # Label de la empresa
        lbl_empresa = QLabel("CandyVoyage - Ventas", self)
        font = QFont()
        font.setPointSize(12)
        lbl_empresa.setFont(font)
        lbl_empresa.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_empresa)

        # Nombre del cliente
        self.nombre_cliente = QLineEdit(self)
        self.nombre_cliente.setPlaceholderText("Nombre del Cliente")
        layout.addWidget(self.nombre_cliente)

        # Selección de productos (con cantidad)
        self.productos_layout = QVBoxLayout()

        productos = [
            "Dulce cafe", "Chocolate kiss", "Marsmello",
            "Chicle frutal", "Caramelo ácido", "Gomitas",
            "Paleta de frutas", "Barra de chocolate"
        ]

        self.productos_checkboxes = []
        self.productos_cantidades = []

        for producto in productos:
            checkbox_layout = QHBoxLayout()
            checkbox = QCheckBox(producto, self)
            cantidad_input = QLineEdit(self)
            cantidad_input.setPlaceholderText("Cantidad")

            self.productos_checkboxes.append(checkbox)
            self.productos_cantidades.append(cantidad_input)

            checkbox_layout.addWidget(checkbox)
            checkbox_layout.addWidget(cantidad_input)
            self.productos_layout.addLayout(checkbox_layout)

        layout.addLayout(self.productos_layout)

        # Selección del departamento
        self.departamentos_combo = QComboBox(self)
        departamentos = [
            "Ahuachapán", "Cabañas", "Chalatenango", "Cuscatlán", "La Libertad", "La Paz", "San Salvador", "San Vicente",
            "Santa Ana", "Sonsonate", "Usulután", "Morazán", "La Unión", "Rivas"
        ]
        self.departamentos_combo.addItems(departamentos)
        layout.addWidget(self.departamentos_combo)

        # Envío departamental
        self.envio_checkbox = QCheckBox("Incluir envío departamental ($2.50)", self)
        layout.addWidget(self.envio_checkbox)

        # Método de pago
        self.metodo_pago_combo = QComboBox(self)
        self.metodo_pago_combo.addItem("Seleccionar método de pago")
        self.metodo_pago_combo.addItem("Efectivo")
        self.metodo_pago_combo.addItem("Tarjeta de Crédito/Débito")
        layout.addWidget(self.metodo_pago_combo)

        # Botón de confirmar venta
        self.btn_confirmar = QPushButton("Confirmar Venta", self)
        self.btn_confirmar.setStyleSheet("background-color: white; font-size: 12px;")
        self.btn_confirmar.clicked.connect(self.confirmar_venta)
        layout.addWidget(self.btn_confirmar)


        # Contenedor central
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Tabla para mostrar el registro de ventas
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Nombre", "Departamento", "Productos", "Método de pago", "Envío"])
        self.table_widget.setRowCount(0)  # Inicialmente vacía
        layout.addWidget(self.table_widget)

    def confirmar_venta(self):
        # Obtener el nombre del cliente
        nombre_cliente = self.nombre_cliente.text()

        # Obtener los productos seleccionados y las cantidades
        productos_seleccionados = []
        for i, checkbox in enumerate(self.productos_checkboxes):
            if checkbox.isChecked():
                cantidad = self.productos_cantidades[i].text()
                if cantidad:
                    productos_seleccionados.append(f"{checkbox.text()} x {cantidad}")

        # Obtener el departamento seleccionado
        departamento = self.departamentos_combo.currentText()

        # Obtener el método de pago seleccionado
        metodo_pago = self.metodo_pago_combo.currentText()

        # Obtener si se incluye el envío departamental
        incluir_envio = self.envio_checkbox.isChecked()

        # Verificar si hay productos seleccionados
        if not productos_seleccionados:
            print("Por favor, selecciona al menos un producto.")
        else:
            # Mostrar la información de la venta
            print(f"Cliente: {nombre_cliente}")
            print(f"Departamento: {departamento}")
            print(f"Productos seleccionados: {', '.join(productos_seleccionados)}")
            print(f"Método de pago: {metodo_pago}")
            if incluir_envio:
                print("Envío departamental: $2.50")

            # Agregar la venta a la tabla
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(nombre_cliente))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(departamento))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(", ".join(productos_seleccionados)))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(metodo_pago))
            envio = "$2.50" if incluir_envio else "No"
            self.table_widget.setItem(row_position, 4, QTableWidgetItem(envio))

    
if __name__ == "__main__":
    app = QApplication([])
    ventana = VentaApp()
    ventana.show()
    app.exec_()







