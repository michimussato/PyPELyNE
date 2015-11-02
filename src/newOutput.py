import os

from PyQt4.QtGui import *
from PyQt4.uic import *


class NewOutputUI(QDialog):
    def __init__(self, main_window, node, parent=None):
        super(NewOutputUI, self).__init__(parent)

        self.main_window = main_window

        self.used_names = None

        self.node = node

        self.ui = loadUi(os.path.join(self.main_window.pypelyne_root, 'ui', 'new_output.ui'), self)
        self.setModal(True)

        self.create_ui()
        self.add_combo_box_items()
        self.create_connects()

    def create_ui(self):
        mime_types = [('arbitrary', None), ('.ass', 'ASS'), ('.exr', 'EXR'), ('.tga', 'TGA')]

        self.comboBoxOutput.addItem('select')

        for mime in mime_types:
            self.comboBoxMime.addItem(mime[0])

        self.comboBoxMime.setEnabled(False)

        self.buttonOk.setEnabled(False)
        
        self.labelFolder.setEnabled(False)
        self.labelStatus.setEnabled(False)
    
    def add_combo_box_items(self):
        for output in self.main_window.outputs:
            self.comboBoxOutput.addItem(output[0][2][1])

    def create_connects(self):
        self.buttonOk.clicked.connect(self.on_ok)
        self.buttonCancel.clicked.connect(self.on_cancel)
        self.lineEditOutputName.textChanged.connect(self.set_status)
        self.comboBoxOutput.activated.connect(self.set_status)

    @property
    def _used_names(self):
        if self.used_names is None:
            self.used_names = os.listdir(os.path.join(self.main_window.projects_root,
                                                      self.main_window._current_project,
                                                      'content',
                                                      self.main_window._current_content['content'],
                                                      self.main_window._current_content_item,
                                                      self.node._label,
                                                      'output'))
        return self.used_names

    def set_status(self):
        if self.comboBoxOutput.currentIndex() == 0 \
                or self.comboBoxOutput.currentIndex() == 0 \
                or self.lineEditOutputName.text() == '':
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('')
            
        elif self.main_window.outputs[self.comboBoxOutput.currentIndex() - 1][0][1][1] + '__' + self.lineEditOutputName.text() in self._used_names:
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('already exists')

        elif ' ' in self.lineEditOutputName.text() \
                or '-' in self.lineEditOutputName.text() \
                or '__' in self.lineEditOutputName.text():
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('invalid character')
            
        else:
            self.buttonOk.setEnabled(True)
            self.labelStatus.setText(self.main_window.outputs[self.comboBoxOutput.currentIndex() - 1][0][1][1] + '__' + self.lineEditOutputName.text())

    def on_cancel(self):
        self.reject()
        
    def on_ok(self):
        output_name = self.main_window.outputs[self.comboBoxOutput.currentIndex() - 1][0][1][1] + '__' + self.lineEditOutputName.text()
        self.accept()

        return output_name
    
    # http://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    @staticmethod
    def get_new_output_data(main_window, node):
        dialog = NewOutputUI(main_window, node)
        result = dialog.exec_()
        output_name = dialog.on_ok()
        return output_name, result == QDialog.Accepted
