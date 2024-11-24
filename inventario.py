from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QApplication, QMessageBox
from PyQt5.QtCore import Qt

# Conectar a la base de datos SQLite
import sqlite3
conn = sqlite3.connect('Candyvoyage.db')
cursor = conn.cursor()

# Crear la tabla de productos si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS Inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL
)
""")
conn.commit()

class InventarioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CandyVoyage - Inventario")
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet("background-color: rgb(255, 94, 77);")  # Color sandía

        # Layout principal
        layout = QVBoxLayout()

        # ComboBox para seleccionar el producto
        self.cmbProducto = QComboBox()
        self.cmbProducto.addItems(["Dulce cafe", "Chocolate kiss", "Marsmello", "Chicle frutal", "Caramelo ácido", "Gomitas", "Paleta de frutas", "Barra de chocolate"])
        layout.addWidget(self.cmbProducto)

        # Campos para cantidad y precio
        self.txtCantidad = QLineEdit()
        self.txtCantidad.setPlaceholderText("Cantidad")
        self.txtPrecio = QLineEdit()
        self.txtPrecio.setPlaceholderText("Precio")
        layout.addWidget(self.txtCantidad)
        layout.addWidget(self.txtPrecio)

        # Botones de agregar, eliminar y actualizar
        self.btnAgregar = QPushButton("Agregar Producto")
        self.btnEliminar = QPushButton("Eliminar Producto")
        self.btnActualizar = QPushButton("Actualizar Inventario")


        self.btnAgregar.setStyleSheet("background-color: rgb(169, 169, 169);")  # Botón gris
        self.btnEliminar.setStyleSheet("background-color: rgb(169, 169, 169);")  # Botón gris
        self.btnActualizar.setStyleSheet("background-color: rgb(169, 169, 169);")  # Botón gris
    

        self.btnAgregar.clicked.connect(self.agregar_producto)
        self.btnEliminar.clicked.connect(self.eliminar_producto)
        self.btnActualizar.clicked.connect(self.cargar_inventario)

        layout.addWidget(self.btnAgregar)
        layout.addWidget(self.btnEliminar)
        layout.addWidget(self.btnActualizar)

        # Tabla de inventario
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Producto', 'Cantidad', 'Precio'])
        layout.addWidget(self.tableWidget)

        # Configurar la ventana
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.cargar_inventario()

    def agregar_producto(self):
        producto = self.cmbProducto.currentText()
        try:
            cantidad = int(self.txtCantidad.text())
            precio = float(self.txtPrecio.text())
            if cantidad <= 0 or precio <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingresa datos válidos.")
            return

        cursor.execute("INSERT INTO Inventario (producto, cantidad, precio) VALUES (?, ?, ?)", (producto, cantidad, precio))
        conn.commit()
        self.cargar_inventario()
        self.txtCantidad.clear()
        self.txtPrecio.clear()
        QMessageBox.information(self, "Éxito", f"Producto '{producto}' agregado.")

    def eliminar_producto(self):
        row = self.tableWidget.currentRow()
        if row >= 0:
            producto_id = self.tableWidget.item(row, 0).text()
            cursor.execute("DELETE FROM Inventario WHERE id=?", (producto_id,))
            conn.commit()
            self.cargar_inventario()
            QMessageBox.information(self, "Éxito", f"Producto con ID {producto_id} eliminado.")
        else:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un producto.")

    def cargar_inventario(self):
        self.tableWidget.setRowCount(0)
        cursor.execute("SELECT * FROM Inventario")
        productos = cursor.fetchall()
        for row_index, row_data in enumerate(productos):
            self.tableWidget.insertRow(row_index)
            for col_index, data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(data)))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = InventarioApp()
    ventana.show()
    sys.exit(app.exec_())

