from aqt.qt import *
from aqt.utils import showInfo

from aqt import mw
from anki.errors import AnkiError 

from .utils import *

class AnalyserMenu(QDialog):

    def __init__(self):
        QDialog.__init__(self, parent=mw)
        self.sort_by_freq = False
        self.exclude_surname_tag = True 
        self.exclude_surname_def = True 
        self.add_parts_of_speech_to_output = False
        self.hsk_level = 0
        self.tocfl_level = 0
        self.add_freq_to_output = False
        self.upper_freq_bound = 8.0
        self.lower_freq_bound = 0.0
        self.simp_or_trad = 'trad'

        self.setupUi()

    def setupUi(self):
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

        hsk_tocfl_tooltip = 'All words of a level LOWER than the input will be excluded. I.e. \'4\' means levels 1, 2 and 3 are removed'

        tab_2_hsk_label = QLabel('Level of HSK filtering')
        tab_2_hsk_label.setToolTip(hsk_tocfl_tooltip)
        tab_2_tocfl_label = QLabel('Level of TOCFL filtering')
        tab_2_tocfl_label.setToolTip(hsk_tocfl_tooltip)
        tab_2_POS_label = QLabel('Add Parts of Speech to card (tag)')
        tab_2_freq_label = QLabel('Add zipf frequency info to card (tag)')
        tab_2_freq_upper_limit_label = QLabel('Designate the zipf frequency '
                'upper cutoff (default 8.0)')
        tab_2_freq_lower_limit_label = QLabel('Designate the zipf frequency '
                'lower cutoff (default 0.0)')
        tab_2_add_surnames_definition_label = QLabel('Add surname to card '
                '(definition)')
        tab_2_add_surnames_definition_label.setToolTip('Adds \'surname\' to the '
                'card\'s definition')
        tab_2_add_surnames_tag_label = QLabel('Add surname to card (tag)')
        tab_2_add_surnames_tag_label.setToolTip('Adds \'surname\' to the card\'s '
                'tags')
        tab_2_simple_or_trad_label = QLabel('Traditional (default Simplified)')
        tab_2_sort_by_freq_label = QLabel('Sort by frequency')
        tab_2_sort_by_freq_label.setToolTip('Most frequent cards will come up '
                'first, according to zipf frequency')


        tab_2_hsk_input = QLineEdit()
        tab_2_hsk_input.setPlaceholderText('0-6')
        tab_2_hsk_input.setFixedWidth(25)
        tab_2_hsk_input.setToolTip(hsk_tocfl_tooltip)

        tab_2_tocfl_input = QLineEdit()
        tab_2_tocfl_input.setPlaceholderText('0-6')
        tab_2_tocfl_input.setFixedWidth(25)
        tab_2_tocfl_input.setToolTip(hsk_tocfl_tooltip)
        
        tab_2_freq_upper_limit_input = QLineEdit()
        tab_2_freq_upper_limit_input.setPlaceholderText('0.0-8.0')
        tab_2_freq_upper_limit_input.setFixedWidth(45)
        tab_2_freq_lower_limit_input = QLineEdit()
        tab_2_freq_lower_limit_input.setPlaceholderText('0.0-8.0')
        tab_2_freq_lower_limit_input.setFixedWidth(45)

        tab_2_pos_button = QCheckBox('')
        tab_2_freq_button = QCheckBox('')
        tab_2_surnames_button_def = QCheckBox('')
        tab_2_surnames_button_tag = QCheckBox('')
        tab_2_simple_or_trad_button = QCheckBox('')
        tab_2_sort_by_freq_button = QCheckBox('')
        tab_2_sort_by_freq_button.setToolTip('Most frequent cards will come up '
                'first, according to zipf frequency')
        
        tab_2_pos_button.clicked.connect(self.set_add_parts_of_speech_to_output)
        tab_2_sort_by_freq_button.clicked.connect(self.set_sort_by_freq)

        list_of_widgets = []

        list_of_widgets.append(tab_2_hsk_label)
        list_of_widgets.append(tab_2_hsk_input)
        list_of_widgets.append(tab_2_tocfl_label)
        list_of_widgets.append(tab_2_tocfl_input)
        list_of_widgets.append(tab_2_freq_lower_limit_label)
        list_of_widgets.append(tab_2_freq_lower_limit_input)
        list_of_widgets.append(tab_2_freq_upper_limit_label)
        list_of_widgets.append(tab_2_freq_upper_limit_input)
        list_of_widgets.append(tab_2_POS_label)
        list_of_widgets.append(tab_2_pos_button)
        list_of_widgets.append(tab_2_freq_label)
        list_of_widgets.append(tab_2_freq_button)
        list_of_widgets.append(tab_2_simple_or_trad_label)
        list_of_widgets.append(tab_2_simple_or_trad_button)
        list_of_widgets.append(tab_2_add_surnames_definition_label)
        list_of_widgets.append(tab_2_surnames_button_def)
        list_of_widgets.append(tab_2_add_surnames_tag_label)
        list_of_widgets.append(tab_2_surnames_button_tag)
        list_of_widgets.append(tab_2_sort_by_freq_label)
        list_of_widgets.append(tab_2_sort_by_freq_button)

        tab_2_layout = place_in_tab_widget(QGridLayout(), list_of_widgets)

        tab_2_layout.addWidget(tab_2_heading, 0, 0, 1, 3)
        rule = self.create_horizontal_rule()
        tab_2_layout.addWidget(rule, 1, 0, 1, -1)

        tab_2.setLayout(tab_2_layout)

        # Tab 3 layout
        tab_3 = QWidget()
        tab_3_heading = QLabel("Review your options on the previous pages "
                "and press 'finish' to start")
        tab_3_heading.setWordWrap(True)
        tab_3_finish_button = QPushButton("Finish", self)
        #Sets the width of the button according the size of the font and the
        #num of chars
        font_width = QFontMetrics(tab_3_finish_button.font())
        tab_3_finish_button.setFixedWidth(font_width.width("   " + tab_3_finish_button.text() + "   "))

        tab_3_layout = QVBoxLayout()
        tab_3_layout.addWidget(tab_3_heading)
        tab_3_layout.addWidget(tab_3_finish_button)

        tab_3_layout.addStretch(100)
        tab_3.setLayout(tab_3_layout)

        #Tab bar layout
        tabWidget = QTabWidget()
        tabWidget.addTab(tab_1, 'Text')
        tabWidget.addTab(tab_2, 'Options')
        tabWidget.addTab(tab_3, 'Finish')

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

    def set_sort_by_freq(self):
        self.sort_by_freq = not self.sort_by_freq

    def set_exclude_surname_tag(self):
        self.exclude_surname_tag = not self.exclude_surname_tag
    
    def set_exclude_surname_def(self):
        self.exclude_surname_def = not self.exclude_surname_def

    def set_add_parts_of_speech_to_output(self):
        self.add_parts_of_speech_to_output = not self.add_parts_of_speech_to_output
    
    def set_hsk_level(self, level):
        self.hsk_level = level

    def set_tocfl_level(self, level):
        self.tocfl_level = level

    def set_add_freq_to_output(self):
        self.add_freq_to_output = not self.add_freq_to_output

    def set_upper_freq_bound(self, bound):
        self.upper_freq_bound = bound

    def set_lower_freq_bound(self, bound):
        self.lower_freq_bound = bound

    def set_simp_or_trad(self):
        if self.simp_or_trad == 'trad':
            self.simp_or_trad = 'simp'
        else:
            self.simp_or_trad = 'trad'
    

