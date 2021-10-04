import sys
from PySide2 import QtWidgets
from gui.view.main_window import MainWindow
from plugin_framework.component_framework import ComponentFramework

def main():
    # Pravljenje komponentnog okruzenja
    component_framework = ComponentFramework()
    component_framework.install_components()
    # Kreiranje aplikacije
    app = QtWidgets.QApplication(sys.argv)
    # Kreiranje glavnog prozora
    main_window = MainWindow()
    # Prikazivanje - obavezno
    main_window.show()
    # Iskljucivanje interpretera zajedno sa iskljucivanjem aplikacije
    sys.exit(app.exec_())

# Pokretanje aplikacije samo ako je pokrenut glavni modul
if __name__ == "__main__":
    main()