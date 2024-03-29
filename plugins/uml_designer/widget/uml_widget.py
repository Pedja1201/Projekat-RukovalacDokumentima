from PySide2 import QtWidgets, QtGui, QtCore
from functools import partial

from .item_dialog import ItemForm
from ..model.item_relation import ItemRelation
from ..model.file_managment import FileManagment


class UmlWidget(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(UmlWidget, self).__init__(parent)
        self.scene = QtWidgets.QGraphicsScene(self)

        self.mine_items = []
        self.ctrl = False
        self.hovered = None
        self.position = None
        self.new_rel = None

        self.item_menu = QtWidgets.QMenu()
        self.general_menu = QtWidgets.QMenu()

        self.setStyleSheet("background-color: #F5F5F5")
        self.add_actions()

        self.setScene(self.scene)
        self.setMouseTracking(True)

    def update_rel_position(self):
        for hov_rel in self.hovered.relationships:
            for rel in hov_rel.host.relationships:
                if rel.relation_type == hov_rel.relation_type and rel.host.name == self.hovered.name:
                    hov_rel.draw(self.hovered.graphics_item.pos() + rel.coordinates)
                    rel.draw(hov_rel.coordinates + hov_rel.host.graphics_item.pos())

    def relation_exist(self, item):
        for hov_rel in self.hovered.relationships:
            if hov_rel.host is not None:
                if hov_rel.host.name == item.name:
                    if hov_rel.relation_type.split(' ', 1)[0] == self.new_rel.split(' ', 1)[0]:
                        return True
                    elif set([hov_rel.relation_type.split(' ', 1)[0], self.new_rel.split(' ', 1)[0]]).issubset(["Unspecified", "Navigable"]):
                        return True
            else:
                return True
        return False

    def save_relation(self):
        first_item = self.hovered
        self.scene.removeItem(first_item.relationships[-1].graphics_item)
        self.hovered = self.find_item()
        if self.hovered is not None and not self.relation_exist(first_item):
            self.scene.addItem(first_item.relationships[-1].graphics_item)
            first_item.relationships[-1].host = self.hovered
            first_item.relationships[-1].reverse = True
            self.hovered.relationships.append(ItemRelation(first_item.relationships[-1].coordinates - first_item.graphics_item.pos(),
                                                           self.new_rel, first_item, False))
            first_item.relationships[-1].coordinates = self.position - self.hovered.graphics_item.pos()
            self.scene.addItem(self.hovered.relationships[-1].graphics_item)
        else:
            del first_item.relationships[-1]
        self.new_rel = None
        self.hovered = None

    def show_menu(self, pos):
        if self.hovered is not None:
            self.item_menu.exec_(pos)
        else:
            self.general_menu.exec_(pos)

    def add_rel(self, relation_type, navigable=True):
        self.new_rel = relation_type
        self.hovered = self.find_item()
        self.hovered.relationships.append(ItemRelation(self.position, relation_type))
        self.hovered.relationships[-1].draw(self.position)
        self.scene.addItem(self.hovered.relationships[-1].graphics_item)
        self.hovered.graphics_item.setSelected(False)

    def set_rel(self, new_item, old_name):
        for rel in new_item.relationships:
            for host_rel in rel.host.relationships:
                if host_rel.host.name == old_name:
                    host_rel.host = new_item
                    break

    def add_item(self):
        self.hovered = self.find_item()
        item_form = ItemForm(self, self.mine_items, self.hovered)
        if self.hovered is not None:
            temp_name = self.hovered.name
            self.hovered.name = ""
        item_form.exec_()
        if item_form.result() == 1:
            self.mine_items.append(item_form.item)
            if self.hovered is not None:
                self.position = self.hovered.graphics_item.pos()
                self.set_rel(item_form.item, self.hovered.name)
                self.remove_item()
                for rel in item_form.item.relationships:
                    self.scene.addItem(rel.graphics_item)
            item_form.item.draw(self.position)
            self.scene.addItem(item_form.item.graphics_item)
        elif self.hovered is not None:
            self.hovered.name = temp_name
        self.hovered = None

    def remove_item(self):
        for rel in self.hovered.relationships:
            for host_rel in rel.host.relationships:
                if host_rel.host.name == self.hovered.name:
                    self.scene.removeItem(host_rel.graphics_item)
                    rel.host.relationships.remove(host_rel)
            self.scene.removeItem(rel.graphics_item)
        self.scene.removeItem(self.hovered.graphics_item)
        self.mine_items.remove(self.hovered)
        self.hovered = None

    def find_item(self):
        if self.scene.itemAt(self.position, QtGui.QTransform()) is not None:
            for item in self.mine_items:
                if item.graphics_item == self.scene.itemAt(self.position, QtGui.QTransform()):
                    return item
                elif item.graphics_item == self.scene.itemAt(self.position, QtGui.QTransform()).topLevelItem():
                    return item
        return None

    def add_actions(self):
        save_action = QtWidgets.QAction("Save to file", self)
        save_action.triggered.connect(partial(FileManagment.save_file, self.mine_items))
        self.general_menu.addAction(save_action)

        remove_item = QtWidgets.QAction("Remove item", self)
        remove_item.triggered.connect(self.remove_item)
        self.item_menu.addAction(remove_item)

        relationships = ["Unspecified Association", "Navigable Association", "Aggregation", "Composition"]
        rel_type = [" to unsecified association", " to navigable association"]

        self.item_menu.addSeparator()

        for rel in relationships:
            rel_menu = QtWidgets.QMenu(rel)
            for rel_t in rel_type:
                nav_rel = QtWidgets.QAction(rel + rel_t, self)
                nav_rel.triggered.connect(partial(self.add_rel, rel + rel_t))
                rel_menu.addAction(nav_rel)
            self.item_menu.addMenu(rel_menu)

        gen_rel = QtWidgets.QAction("Generalization", self)
        gen_rel.triggered.connect(partial(self.add_rel, "Generalization"))
        self.item_menu.addAction(gen_rel)

    def mouseMoveEvent(self, event):
        super(UmlWidget, self).mouseMoveEvent(event)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.position = self.mapToScene(event.pos())
        if self.hovered is not None:
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            self.position = self.mapToScene(event.pos())
            if len(self.scene.selectedItems()) == 0:
                self.hovered.relationships[-1].draw(self.position)
            else:
                self.update_rel_position()

    def mousePressEvent(self, event):
        super(UmlWidget, self).mousePressEvent(event)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.position = self.mapToScene(event.pos())
        if self.new_rel is not None:
            self.save_relation()
        self.hovered = self.find_item()
        if event.buttons() & QtCore.Qt.RightButton:
            self.show_menu(self.mapToGlobal(event.pos()))

    def mouseDoubleClickEvent(self, event):
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.position = self.mapToScene(event.pos())
        self.add_item()

    def mouseReleaseEvent(self, event):
        super(UmlWidget, self).mouseReleaseEvent(event)
        if len(self.scene.selectedItems()) > 0:
            self.hovered = None

    def keyPressEvent(self, event):
        super(UmlWidget, self).keyPressEvent(event)
        if event.key() == 16777249:
            self.ctrl = True

    def keyReleaseEvent(self, event):
        super(UmlWidget, self).keyReleaseEvent(event)
        if event.key() == 16777249:
            self.ctrl = False
        if event.key() == 16777216:
            self.scene.removeItem(self.hovered.relationships[-1].graphics_item)
            del self.hovered.relationships[-1]
            self.new_rel = None
            self.hovered = None

    def wheelEvent(self, event):
        super(UmlWidget, self).wheelEvent(event)
        if self.ctrl:
            zoomInFactor = 1.25
            zoomOutFactor = 1 / zoomInFactor
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)
            oldPos = self.mapToScene(event.pos())
            if event.delta() > 0:
                zoomFactor = zoomInFactor
            else:
                zoomFactor = zoomOutFactor
            self.scale(zoomFactor, zoomFactor)
            newPos = self.mapToScene(event.pos())
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                fname = str(url.toLocalFile())

            del self.mine_items[:]
            for item in FileManagment.load_file(fname, self.scene):
                self.mine_items.append(item)
            for item in self.mine_items:
                self.hovered = item
                self.update_rel_position()
            self.hovered = None

        else:
            event.ignore()