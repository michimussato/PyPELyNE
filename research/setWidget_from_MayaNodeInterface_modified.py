~/Dropbox/development/workspace/PyPELyNE/research/MayaNodeInterface_modified/ui/nodeModule.py:23:     def getWidgetMenu(self):

    def getWidgetMenu(self):
        if self._widgetMenuObj is None and self.widgetMenu:
            self._widgetMenuObj = self.widgetMenu()
        return self._widgetMenuObj
        



~/Dropbox/development/workspace/PyPELyNE/research/MayaNodeInterface_modified/nodeGui.py:74:         setWidget = self.nodeMenuArea.setWidget(item.getWidgetMenu())
        
    def setWidgetMenu(self, item):
    	print "duude"
        takeWidget = self.nodeMenuArea.takeWidget()
        print takeWidget
        setWidget = self.nodeMenuArea.setWidget(item.getWidgetMenu())
        print setWidget
        self.nodeOptionsWindow.setTitle(item.displayText.toPlainText())
        




SceneView.dragMoveEvent() called
SceneView.dropEven() called
SceneView.createNode() called
nodeModule.getWidgetMenu
nodeModule.getWidgetMenu
nodeModule.getWidgetMenu
SceneView.createNode(): sceneNode = <MayaNodeInterface.ui.nodeModule.AttrNode object at 0x13695a3b0>



SceneView.mousePressEvent(): self.itemAt(event.scenePos()) = <MayaNodeInterface.ui.nodeModule.AttrNode object at 0x13695a3b0>
nodeGui.setWidgetMenu
<PyQt4.QtGui.QWidget object at 0x1367d6170>
nodeModule.getWidgetMenu
None
SceneView.mouseMoveEvent() called
SceneView.mouseMoveEvent() called