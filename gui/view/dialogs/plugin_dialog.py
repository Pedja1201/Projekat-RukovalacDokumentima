from PySide2 import QtWidgets
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt


class PluginDialog(QtWidgets.QDialog):
    """
    Klasa koja predstavlja dialog u kojem se vrsi manipulacija nad prosirenjima.
    """
    def __init__(self, title="Plugin settings", parent=None, plugin_service=None):
        """
        Inicijalizator dijaloga za podesavanje i prikaz pluginova.

        :param title: naslov dijaloga.
        :type title: str
        :param parent: roditeljski widget dijaloga.
        :type parent: QWidget
        :param plugin_service: servis za pluginove
        :type plugin_service: PluginService
        """
        # podesavanje dijaloga
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon("resources/icons/plugins.png"))
        self.resize(750, 400)

        self.plugin_service = plugin_service
     
        self.plugin_options_layout = QtWidgets.QHBoxLayout()

        self.install_button = QtWidgets.QPushButton(QIcon("resources/icons/installing.jpg"), "Install")
        self.uninstall_button = QtWidgets.QPushButton(QIcon("resources/icons/minus.png"), "Uninstall")
        self.enable_button = QtWidgets.QPushButton(QIcon("resources/icons/active.png"), "Activate")
        self.disable_button = QtWidgets.QPushButton(QIcon("resources/icons/deactivate.png"), "Deactivate")
        
        self.plugin_dialog_layout = QtWidgets.QVBoxLayout()

        self.plugins_table = QtWidgets.QTableWidget(self)
        self.plugins_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.plugins_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.plugin_options_layout.addWidget(self.install_button)
        self.plugin_options_layout.addWidget(self.uninstall_button)
        self.plugin_options_layout.addWidget(self.enable_button)
        self.plugin_options_layout.addWidget(self.disable_button)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.on_accept)
        self.button_box.rejected.connect(self.on_reject)

        self.enable_button.clicked.connect(self.on_set)

        self._populate_table()

        self.plugin_dialog_layout.addLayout(self.plugin_options_layout)
        self.plugin_dialog_layout.addWidget(self.plugins_table)
        self.plugin_dialog_layout.addWidget(self.button_box)

        self.setLayout(self.plugin_dialog_layout)

    def on_set(self):
        """
        Metoda koja se poziva kada se pritisne na dugme set central.
        """
        # FIXME: dobavi selekciju i aktiviraj widget
        selected_items = self.plugins_table.selectedItems()
        if len(selected_items) == 0:
            return
        name = selected_items[0].text()
        self.parent().set_central_widget(name)
        
    def on_accept(self):
        """
        Metoda koja se poziva na prihvatanje dijaloga.
        """
        return self.accept()

    def on_reject(self):
        """
        Metoda koja se poziva na odbijanje dijaloga.
        """
        return self.reject()

    def _populate_table(self):
        """
        Populise tabelu metapodacima plugina.
        """
        self.plugins_table.setColumnCount(7)
        self.plugins_table.setHorizontalHeaderLabels(
            ["Name", "Version","Core version", "Description", "Category", "Licence", "Web page"])
        # TODO: list all plugins
        self.plugins_table.setRowCount(len(self.plugin_service.plugins))
        for i, plugin in enumerate(self.plugin_service.plugins):
            name = QtWidgets.QTableWidgetItem(plugin.name)
            version = QtWidgets.QTableWidgetItem(plugin.version)
            core_version = QtWidgets.QTableWidgetItem(plugin.core_version)
            description = QtWidgets.QTableWidgetItem(plugin.description)
            category = QtWidgets.QTableWidgetItem(plugin.category)
            licence = QtWidgets.QTableWidgetItem(plugin.licence)
            web_page = QtWidgets.QTableWidgetItem(plugin.web_page)

            # setovanje flag-ova tako da se name, version, description, category, core_version,licence,web_page ne mogu menjati od strane korisnika
            # tj. nisu editable 
            name.setFlags(name.flags() ^ Qt.ItemIsEditable)
            version.setFlags(version.flags() ^ Qt.ItemIsEditable)
            core_version.setFlags(core_version.flags() ^ Qt.ItemIsEditable)
            description.setFlags(description.flags() ^ Qt.ItemIsEditable)
            category.setFlags(category.flags() ^ Qt.ItemIsEditable)
            licence.setFlags(licence.flags() ^ Qt.ItemIsEditable)
            web_page.setFlags(web_page.flags() ^ Qt.ItemIsEditable)

            self.plugins_table.setItem(i, 0, name)
            self.plugins_table.setItem(i, 1, version)
            self.plugins_table.setItem(i, 2, core_version)
            self.plugins_table.setItem(i, 3, description)
            self.plugins_table.setItem(i, 4, category)
            self.plugins_table.setItem(i, 5, licence)
            self.plugins_table.setItem(i, 6, web_page)




