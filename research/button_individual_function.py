import sys
from PyQt4 import QtGui

class Widget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__( parent )

        # Arrange buttons horizontally
        buttonLayout = QtGui.QHBoxLayout()

        # QButtonGroup to keep track of buttons
        self.buttonGroup = QtGui.QButtonGroup()

        # Connect the 'buttonClicked' signal 'self.setLabel'
        # There are two overloads for 'buttonClicked' signal: QAbstractButton (button itself) or int (id)
        # Specific overload for the signal is selected via [QtGui.QAbstractButton]
        # Clicking any button in the QButtonGroup will send this signal with the button
        self.buttonGroup.buttonClicked[ QtGui.QAbstractButton ].connect( self.setLabel )

        for i in range( 5 ): # Let's create 5 button
            button = QtGui.QPushButton( '%d' % i )     # make a button
            buttonLayout.addWidget( button )           # add to layout
            self.buttonGroup.addButton( button )       # add to QButtonGroup
            #self.buttonGroup.addButton( button, i )   # You can give an 'id' if you like

        self.label = QtGui.QLabel()  # just to write some output

        # lay everything out
        layout = QtGui.QVBoxLayout()
        layout.addLayout(buttonLayout)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def setLabel(self, button):
        print button.text()
        # clicking any button will call this slot 
        # 'button' argument will be the button itself
        # so... let's show its text in the label:
        self.label.setText('You clicked button with text "%s"' % button.text())
        
        



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    widget = Widget()
    widget.show()
    app.exec_()