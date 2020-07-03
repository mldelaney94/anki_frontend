from aqt.qt import *
from aqt.utils import showInfo

from aqt import mw
from anki.errors import AnkiError 

class AnalyserMenu(QDialog):

    def __init__(self):
        QDialog.__init__(self, parent=mw)
        self.sort_by_freq = 0
        self.exclude_surname = 0
        self.add_parts_of_speech_to_output = 0
        self.hsk_level = 0
        self.tocfl_level = 0
        self.add_freq_to_output = 0
        self.upper_freq_bound = 8.0
        self.lower_freq_bound = 0.0
        self.simp_or_trad = 'trad'

        self.setupUi()

    def setupUi(self):
        tab_1_label = QLabel("Text1")
        tab_2_label = QLabel("Options")
        tab_3_label = QLabel("Finish")


        # Tab 1 layout
        tab_1 = QWidget()
        tab_1_text_box_label = QLabel('Please paste or type the text that you '
                                        'want to analyse')
        text_box = QTextEdit()
        tab_1_layout = QVBoxLayout()
        tab_1_layout.addWidget(tab_1_text_box_label)
        tab_1_layout.addWidget(text_box)

        tab_1.setLayout(tab_1_layout)

        # Tab 2 layout
        tab_2 = QWidget()
        tab_2_label = QLabel('Please select the filtering options you wish to '
                                'use')
        tab_2_label.setStyleSheet("QLabel {background-color: red;}")
        tab_2_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        tab_2_layout = QGridLayout()
        tab_2_layout.addWidget(tab_2_label, 0, 0)

        tab_2_test_button = QCheckBox('test')
        tab_2_layout.addWidget(tab_2_test_button, 2, 0)

        tab_2.setLayout(tab_2_layout)

        # Tab 3 layout


        
        tabWidget = QTabWidget()
        tabWidget.addTab(tab_1, 'Text')
        tabWidget.addTab(tab_2_label, 'Options')
        tabWidget.addTab(tab_3_label, 'Finish')

        tabWidget.setTabToolTip(0, 'Use this tab to define the body of text '
                'you want to create cards for')
        tabWidget.setTabToolTip(1, 'Use this tab to define filtering rules '
                'for the text')

        layout = QVBoxLayout()
        layout.addWidget(tabWidget)

        self.setLayout(layout)


