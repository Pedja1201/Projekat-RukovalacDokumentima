import sys
from PySide2.QtWidgets import *
class TreeWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TreeWindow, self).__init__(parent)
        self._generateUI()
        #self._simple_tree_widget()
        self._tree_widget1()
        self._tree_widget2()
        self._tree_widget3()
        
    def _generateUI(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.tree_widget = QTreeWidget()
        main_layout.addWidget(self.tree_widget)
    def _tree_widget1(self):
        self.tree_widget.setHeaderLabels(["Naslov"])
        tree_widget_item1 = QTreeWidgetItem(["Stavka1"])
        tree_widget_item1.addChild(QTreeWidgetItem(["Stavka1.2"]))
        tree_widget_item2 = QTreeWidgetItem(["Stavka2"])
        tree_widget_item2.addChild(QTreeWidgetItem(["Stavka2.2"]))
        self.tree_widget.addTopLevelItem(tree_widget_item1)
        self.tree_widget.addTopLevelItem(tree_widget_item2)
    def _tree_widget2(self):
        headers = ["Naslov1", "Naslov2", "Naslov3"]
        self.tree_widget.setHeaderLabels(headers)
        tree_widget_item1 = QTreeWidgetItem(["stavka1_kol1", "stavka1_kol2", "stavka1_kol3"])
        tree_widget_item1.addChild(QTreeWidgetItem(["stavka1_2_kol1", "stavka1_2_kol2", "stavka1_2_kol3"]))
        self.tree_widget.addTopLevelItem(tree_widget_item1)

    def _tree_widget3(self):
        self.tree_widget.setHeaderHidden(True)
        # define items as dictionary
        children_level1 = ["child1", "child2", "child3"]
        children_level2 = {"child1":["child1_1", "child1_2"], "child2":["child2_1"], "child3":["child3_1", "child3_2", "child3_3"]}
        children_level3 = {"child1_2":["child1_2_1", "child1_2_3"], "child3_1":["child3_1_1"]}
        for child1 in children_level1:
            item1 = QTreeWidgetItem([child1])
            self.tree_widget.addTopLevelItem(item1)
            if child1 in children_level2:
                for child2 in children_level2[child1]:
                    item2 = QTreeWidgetItem([child2])
                    item1.addChild(item2)
                    if child2 in children_level3:
                        for child3 in children_level3[child2]:
                            item3 = QTreeWidgetItem([child3])
                            item2.addChild(item3)