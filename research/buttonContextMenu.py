# http://stackoverflow.com/questions/782255/qt-and-context-menu

from PyQt4 import QtCore, QtGui
import sys

class Foo( QtGui.QWidget ):
	
    signal = QtCore.pyqtSignal()
	
    def __init__(self):
        QtGui.QWidget.__init__(self, None)
        mainLayout = QtGui.QVBoxLayout()
        self.setLayout(mainLayout)

        # Toolbar
        toolbar = QtGui.QToolBar()
        mainLayout.addWidget(toolbar)

        # Action are added/created using the toolbar.addAction
        # which creates a QAction, and returns a pointer..
        # .. instead of myAct = new QAction().. toolbar.AddAction(myAct)
        # see also menu.addAction and others
        self.actionAdd = toolbar.addAction("New", self.foo)
        self.actionEdit = toolbar.addAction("Edit", self.foo)
        self.actionDelete = toolbar.addAction("Delete", self.foo)
        self.actionDelete.setDisabled(True)

        # Tree
        self.tree = QtGui.QPushButton('fuck me hard')
        mainLayout.addWidget(self.tree)
        self.tree.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        #self.assetButtonGroup.buttonClicked[QAbstractButton].connect( self.getAssetContent )
        self.connect(self.tree, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)
        
        #self.tree.clicked.connect( self.on_context_menu )
        #self.signal.emit()

        # Popup Menu is not visible, but we add actions from above
        self.popMenu = QtGui.QMenu( self )
        self.popMenu.addAction( self.actionEdit )
        self.popMenu.addAction( self.actionDelete )
        self.popMenu.addSeparator()
        self.popMenu.addAction( self.actionAdd )
        
    def foo(self):
    	pass

    def on_context_menu(self, point):

         self.popMenu.exec_( self.tree.mapToGlobal(point) )
         


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    widget = Foo()
    widget.show()
    app.exec_()
