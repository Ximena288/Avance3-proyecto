import sqlite3
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QApplication, QMessageBox

# Conectar a la base de datos SQLite
conn = sqlite3.connect('Candyvoyage.db')
cursor = conn.cursor()

# Crear la tabla de clientes si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS Clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    edad INTEGER NOT NULL,
    genero TEXT NOT NULL,
    telefono TEXT NOT NULL,
    correo TEXT NOT NULL,
    departamento TEXT NOT NULL
)
""")
conn.commit()

class ClientesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Clientes")
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet("background-color: rgb(255, 160, 122);")  # Color salmón

        # Layout principal
        layout = QVBoxLayout()

        # Campos de texto y opciones
        self.txtNombre = QLineEdit(self)
        self.txtNombre.setPlaceholderText("Nombre")
        self.txtApellido = QLineEdit(self)
        self.txtApellido.setPlaceholderText("Apellido")
        self.txtEdad = QLineEdit(self)
        self.txtEdad.setPlaceholderText("Edad")
        self.txtTelefono = QLineEdit(self)
        self.txtTelefono.setPlaceholderText("Teléfono (+503)")  # Ingresar solo número
        self.txtCorreo = QLineEdit(self)
        self.txtCorreo.setPlaceholderText("Correo")
        
        self.comboGenero = QComboBox(self)
        self.comboGenero.addItems(["Femenino", "Masculino"])  # "Femenino" primero

        self.comboDepartamento = QComboBox(self)
        departamentos = [
            "Ahuachapán", "Cabañas", "Chalatenango", "Cuscatlán", "La Libertad",
            "La Paz", "Litoral", "Morazán", "San Miguel", "San Salvador", "San Vicente",
            "Santa Ana", "Sonsonate", "Usulután"
        ]
        self.comboDepartamento.addItems(departamentos)

        # Agregar los campos al layout
        layout.addWidget(self.txtNombre)
        layout.addWidget(self.txtApellido)
        layout.addWidget(self.txtEdad)
        layout.addWidget(self.comboGenero)
        layout.addWidget(self.txtTelefono)
        layout.addWidget(self.txtCorreo)
        layout.addWidget(self.comboDepartamento)

        # Botón para agregar cliente
        self.btnAgregar = QPushButton("Agregar Cliente")
        self.btnAgregar.setStyleSheet("background-color: rgb(169, 169, 169);")  # Botón gris
        self.btnAgregar.clicked.connect(self.agregar_cliente)
        layout.addWidget(self.btnAgregar)


        # Tabla para mostrar los clientes registrados
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Nombre', 'Apellido', 'Edad', 'Género', 'Teléfono', 'Correo', 'Departamento'])
        layout.addWidget(self.tableWidget)

        # Configurar la ventana
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.cargar_clientes()

    def agregar_cliente(self):
        # Obtener los datos de los campos
        nombre = self.txtNombre.text()
        apellido = self.txtApellido.text()
        edad = self.txtEdad.text()
        telefono = self.txtTelefono.text()
        correo = self.txtCorreo.text()
        genero = self.comboGenero.currentText()
        departamento = self.comboDepartamento.currentText()

        # Asegurar que el teléfono tenga el prefijo +503
        if telefono and not telefono.startswith("+503"):
            telefono = "+503" + telefono

        if not nombre or not apellido or not edad or not telefono or not correo:
            QMessageBox.warning(self, "Error", "Por favor, completa todos los campos.")
            return

        # Insertar cliente en la base de datos
        cursor.execute("INSERT INTO Clientes (nombre, apellido, edad, genero, telefono, correo, departamento) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (nombre, apellido, edad, genero, telefono, correo, departamento))
        conn.commit()
        
        # Limpiar los campos
        self.txtNombre.clear()
        self.txtApellido.clear()
        self.txtEdad.clear()
        self.txtTelefono.clear()
        self.txtCorreo.clear()
        
        # Actualizar la tabla
        self.cargar_clientes()
        QMessageBox.information(self, "Éxito", "Cliente agregado correctamente.")

    def cargar_clientes(self):
        # Limpiar la tabla
        self.tableWidget.setRowCount(0)

        # Obtener todos los registros de clientes
        cursor.execute("SELECT * FROM Clientes")
        clientes = cursor.fetchall()

        # Llenar la tabla con los datos
        for row_num, row_data in enumerate(clientes):
            self.tableWidget.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))

  

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = ClientesApp()
    ventana.show()
    sys.exit(app.exec_())


