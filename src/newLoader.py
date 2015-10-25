import os

from PyQt4.QtGui import *
from PyQt4.uic import *

import settings as SETTINGS

'''
#library loader procedure:
cd /Volumes/pili/pypelyne_projects/0000-00-00___test___test/content/assets/libraryTest ;

mkdir LDR_LIB__mazda;

cd LDR_LIB__mazda/;

#create the xml file:
touch propertyNode.xml;

ln -s ../../../../../../pypelyne_library/2015-05-20___myself___edelviz_____assets_____edelVizModel_____SVR_AST__edelVizModel_____2015-09-04_1632-53/output output;

ln -s ../../../../../../pypelyne_library/2015-05-20___myself___edelviz_____assets_____edelVizModel_____SVR_AST__edelVizModel_____2015-09-04_1632-53/input input;

ln -s ../../../../../../pypelyne_library/2015-05-20___myself___edelviz_____assets_____edelVizModel_____SVR_AST__edelVizModel_____2015-09-04_1632-53/live live;

'''


class NewLoaderUI(QDialog):
    def __init__(self, active_item_path, main_window, parent=None):
        super(NewLoaderUI, self).__init__(parent)

        self.main_window = main_window
        self.exclusions = SETTINGS.EXCLUSIONS
        # self.pypelyne_root = self.main_window.pypelyne_root
        
        # self.current_platform = self.main_window.current_platform
        self.active_item_path = active_item_path
        self.contentDirectory = os.path.dirname(os.path.dirname(active_item_path))

        self.loader_name = None
        self.source_saver_location = None

        self.ui = loadUi(os.path.join(self.main_window.pypelyne_root, 'ui', 'newLoader.ui'), self)

        self.setModal(True)

        self.create_ui()
        self.add_combo_box_category_items()
        self.create_connects()

    def create_ui(self):
        self.comboBoxCategory.addItem('select')
        self.comboBoxItem.addItem('select')
        
        self.comboBoxItem.setEnabled(False)

        self.buttonOk.setEnabled(False)
        
        self.labelFolder.setEnabled(False)
        self.labelStatus.setEnabled(False)

    def add_combo_box_category_items(self):
        directory_content = os.listdir(self.contentDirectory)

        for directory in directory_content:
            if directory not in SETTINGS.EXCLUSIONS:
                self.comboBoxCategory.addItem(directory)

    def create_connects(self):
        self.buttonOk.clicked.connect(self.on_ok)
        self.buttonCancel.clicked.connect(self.on_cancel)
        self.comboBoxCategory.activated.connect(self.set_status)
        self.comboBoxItem.activated.connect(self.set_combo_box_item)

    def set_combo_box_item(self):
        if str(self.comboBoxItem.currentText()) == 'select':
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('')

        else:
            subcontent_location = os.path.join(self.contentDirectory, str(self.comboBoxCategory.currentText()), str(self.comboBoxItem.currentText()))
            subcontent = os.listdir(subcontent_location)

            if any('SVR' in s for s in subcontent):
                if self.active_item_path == os.path.join(self.contentDirectory, str(self.comboBoxCategory.currentText()), str(self.comboBoxItem.currentText())):
                    self.buttonOk.setEnabled(False)
                    self.labelStatus.setText('dont\'t create its own loader')

                else:
                    self.buttonOk.setEnabled(True)
                    self.labelStatus.setText('item has saver')
                    self.source_saver_location = subcontent_location

            else:
                self.buttonOk.setEnabled(False)
                self.labelStatus.setText('item has no saver')

    def set_status(self):
        if self.comboBoxCategory.currentIndex() == 0:
            self.comboBoxItem.clear()
            self.labelStatus.setText('')
            self.comboBoxItem.addItem('select')
            self.comboBoxItem.setEnabled(False)
            self.buttonOk.setEnabled(False)

        else:
            content = os.listdir(os.path.join(self.contentDirectory, str(self.comboBoxCategory.currentText())))
            self.comboBoxItem.clear()
            self.comboBoxItem.addItem('select')
            self.labelStatus.setText('')
            self.comboBoxItem.setEnabled(True)

            if self.comboBoxItem.currentIndex() == 0:

                for directory in content:
                    if directory not in SETTINGS.EXCLUSIONS:
                        self.comboBoxItem.addItem(directory)

    def on_cancel(self):
        self.reject()
        
    def on_ok(self):
        saver_folder = [folder for folder in os.listdir(self.source_saver_location) if folder.startswith('SVR_')][0]

        for tab in self.main_window.content_tabs:
            if str(self.comboBoxCategory.currentText()) == tab['content']:
                self.loader_name = 'LDR_' + tab['abbreviation'] + '__' + str(self.comboBoxItem.currentText())
                break

        self.accept()

        return self.loader_name, os.path.join(self.source_saver_location, saver_folder)

    # http://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    @staticmethod
    # TODO: check if SETTINGS.EXCLUSIONS gets passed to this function
    def get_new_loader_data(content_directory, main_window):
        dialog = NewLoaderUI(content_directory, main_window)
        result = dialog.exec_()
        loader_name, source_saver_location = dialog.on_ok()
        return result == QDialog.Accepted, loader_name, source_saver_location
