class QxTextItem(QtGui.QGraphicsTextItem):
    lostFocus = QtCore.pyqtSignal(QtGui.QGraphicsTextItem)
    selectedChange = QtCore.pyqtSignal(QtGui.QGraphicsItem)
 
    def __init__(self, parent=None, text=qx.Null):
        super(QxTextItem, self).__init__(parent)
 
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setHtml(text)
 
    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            self.selectedChange.emit(self)
        return value
 
    def focusOutEvent(self, event):
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.lostFocus.emit(self)
        super(QxTextItem, self).focusOutEvent(event)
 
    def mouseDoubleClickEvent(self, event):
        if self.textInteractionFlags() == QtCore.Qt.NoTextInteraction:
            self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        super(QxTextItem, self).mouseDoubleClickEvent(event)