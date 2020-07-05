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
        tab_2_heading = QLabel('Please select the filtering options you wish to '
                                'use')
        tab_2_heading.setWordWrap(True)

        tab_2_hsk_label = QLabel('Level of HSK filtering')
        tab_2_tocfl_label = QLabel('Level of TOCFL filtering')
        tab_2_POS_label = QLabel('Add Parts of Speech to card')
        tab_2_freq_label = QLabel('Add frequency info to card')
        tab_2_freq_upper_limit_label = QLabel('Designate the zipf frequency '
                'upper cutoff (default 8.0)')
        tab_2_freq_lower_limit_label = QLabel('Designate the zipf frequency '
                'lower cutoff (default 0.0)')
        tab_2_add_surnames_label = QLabel('Add surname info to card')
        tab_2_simple_or_trad_label = QLabel('Traditional (default Simplified)')

        tab_2_layout = QGridLayout()
        tab_2_layout.setSpacing(10)

        tab_2_layout.addWidget(tab_2_heading, 0, 0, 1, 3)
        rule = self.create_horizontal_rule()
        tab_2_layout.addWidget(rule, 1, 0, 1, -1)


        tab_2_hsk_input = QLineEdit()
        tab_2_hsk_input.setPlaceholderText('0-6')
        tab_2_hsk_input.setFixedWidth(25)

        tab_2_tocfl_input = QLineEdit()
        tab_2_tocfl_input.setPlaceholderText('0-6')
        tab_2_tocfl_input.setFixedWidth(25)
        
        tab_2_freq_upper_limit_input = QLineEdit()
        tab_2_freq_upper_limit_input.setPlaceholderText('0.0-8.0')
        tab_2_freq_upper_limit_input.setFixedWidth(45)
        tab_2_freq_lower_limit_input = QLineEdit()
        tab_2_freq_lower_limit_input.setPlaceholderText('0.0-8.0')
        tab_2_freq_lower_limit_input.setFixedWidth(45)

        tab_2_pos_button = QCheckBox('')
        tab_2_freq_button = QCheckBox('')
        tab_2_surnames_button = QCheckBox('')
        tab_2_simple_or_trad_button = QCheckBox('')

        tab_2_layout.addWidget(tab_2_hsk_label, 2, 0)
        tab_2_layout.addWidget(tab_2_hsk_input, 2, 1)
        tab_2_layout.addWidget(tab_2_tocfl_label, 2, 2)
        tab_2_layout.addWidget(tab_2_tocfl_input, 2, 3)
        tab_2_layout.addWidget(tab_2_freq_lower_limit_label, 3, 0)
        tab_2_layout.addWidget(tab_2_freq_lower_limit_input, 3, 1)
        tab_2_layout.addWidget(tab_2_freq_upper_limit_label, 3, 2)
        tab_2_layout.addWidget(tab_2_freq_upper_limit_input, 3, 3)
        tab_2_layout.addWidget(tab_2_POS_label, 4, 0)
        tab_2_layout.addWidget(tab_2_pos_button, 4, 1)
        tab_2_layout.addWidget(tab_2_freq_label, 4, 2)
        tab_2_layout.addWidget(tab_2_freq_button, 4, 3)
        tab_2_layout.addWidget(tab_2_simple_or_trad_label, 5, 0)
        tab_2_layout.addWidget(tab_2_simple_or_trad_button, 5, 1)
        tab_2_layout.addWidget(tab_2_add_surnames_label, 5, 2)
        tab_2_layout.addWidget(tab_2_surnames_button, 5, 3)

        tab_2.setLayout(tab_2_layout)

        # Tab 3 layout


        
        tabWidget = QTabWidget()
        tabWidget.addTab(tab_1, 'Text')
        tabWidget.addTab(tab_2, 'Options')
        tabWidget.addTab(tab_3_label, 'Finish')

        tabWidget.setTabToolTip(0, 'Use this tab to define the body of text '
                'you want to create cards for')
        tabWidget.setTabToolTip(1, 'Use this tab to define filtering rules '
                'for the text')

        layout = QVBoxLayout()
        layout.addWidget(tabWidget)

        self.setLayout(layout)
        self.setMinimumWidth(800)
        self.setMinimumHeight(640)
        self.setWindowTitle('Chinese Prestudy')

    def create_horizontal_rule(self):
        """
        Returns a QFrame that is a sunken, horizontal rule.
        """
        frame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        return frame
