from PyQt4 import QtGui

class Window(QtGui.QWidget):
    def __init__(self, val):
        QtGui.QWidget.__init__(self)
        mygroupbox = QtGui.QGroupBox('')
        myform = QtGui.QHBoxLayout()
        labellist = []
        #combolist = []
        for i in range(val):
            labellist.append(QtGui.QPushButton('mylabel %d' %i))
            #combolist.append(QtGui.QComboBox())
            #myform.addRow(labellist[i],combolist[i])
            myform.addWidget(labellist[i])
        mygroupbox.setLayout(myform)
        scroll = QtGui.QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(100)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(scroll)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window(100)
    window.setGeometry(500, 300, 300, 400)
    window.show()
    sys.exit(app.exec_())