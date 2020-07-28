from aqt.qt import *
from aqt.utils import showInfo

from aqt import mw
from anki.errors import AnkiError

from .utils import *
from .zh_analyser import zh_analyser

class AnalyserMenu(QDialog):

    def __init__(self):
        QDialog.__init__(self, parent=mw)
        self.sort_by_freq = False
        self.include_surname_tag = False
        self.include_surname_def = False
        self.add_parts_of_speech_to_output = False
        self.hsk_level = 0
        self.tocfl_level = 0
        self.add_freq_to_output = False
        self.upper_freq_bound = 8.0
        self.lower_freq_bound = 0.0
        self.simp_or_trad = 'simp'
        self.deck_name = ''
        self.zh_input = ''

        self.setupUi()

    def setupUi(self):
        # Tab 1 layout
        tab_1 = QWidget()
        tab_1_deck_name_info = QLabel('Please enter the name of the deck you '
                'wish to create (must be unique):')
        tab_1_text_box_info = QLabel('Please paste or type the text that you '
                'want to analyse:')
        tab_1_deck_name_box = QLineEdit()
        tab_1_deck_name_box.setPlaceholderText('Name... ')
        tab_1_text_box = QTextEdit()

        tab_1_layout = QVBoxLayout()
        tab_1_layout.addWidget(tab_1_deck_name_info)
        tab_1_layout.addWidget(tab_1_deck_name_box)
        tab_1_layout.addWidget(tab_1_text_box_info)
        tab_1_layout.addWidget(tab_1_text_box)

        tab_1.setLayout(tab_1_layout)

        # Tab 2 layout
        tab_2 = QWidget()
        tab_2_heading = QLabel('Please select the options you wish to use')

        hsk_tocfl_tooltip = 'Removes all words at a level <= the number in the box'
        tab_2_hsk_label = QLabel('Level of HSK filtering')
        tab_2_hsk_label.setToolTip(hsk_tocfl_tooltip)
        tab_2_tocfl_label = QLabel('Level of TOCFL filtering')
        tab_2_tocfl_label.setToolTip(hsk_tocfl_tooltip)
        tab_2_POS_label = QLabel('Add Parts of Speech to card (tag)')
        tab_2_freq_label = QLabel('Add zipf frequency info to card (tag)')
        tab_2_freq_upper_limit_label = QLabel('Designate the zipf frequency '
                'upper cutoff (default 8.0). Leave at 8.0 if no filtering '
                'desired')
        tab_2_freq_lower_limit_label = QLabel('Designate the zipf frequency '
                'lower cutoff (default 0.0). Leave at 0.0 if no filtering '
                'desired')
        tab_2_add_surnames_definition_label = QLabel('Add surname to card '
                '(definition)')
        tab_2_add_surnames_tag_label = QLabel('Add surname to card (tag)')
        tab_2_add_surnames_tag_label.setToolTip('Adds \'surname\' to the card\'s '
                'tags')
        tab_2_simple_or_trad_label = QLabel('Traditional (default Simplified)')
        tab_2_sort_by_freq_label = QLabel('Sort by frequency')
        tab_2_sort_by_freq_label.setToolTip('Most frequent cards will come up '
                'first, according to zipf frequency')

        tab_2_hsk_input = create_spin_box('normal', 0, 6, 0)
        tab_2_tocfl_input = create_spin_box('normal', 0, 5, 0)

        tab_2_freq_upper_limit_input = create_spin_box('double', 0.0, 8.0, 8.0)
        tab_2_freq_lower_limit_input = create_spin_box('double', 0.0, 8.0, 0.0)

        tab_2_pos_button = QCheckBox('')
        tab_2_freq_button = QCheckBox('')
        tab_2_surnames_tag_button = QCheckBox('')
        tab_2_simple_or_trad_button = QCheckBox('')
        tab_2_sort_by_freq_button = QCheckBox('')

        tab_2_pos_button.clicked.connect(self.set_add_parts_of_speech_to_output)
        tab_2_sort_by_freq_button.clicked.connect(self.set_sort_by_freq)
        tab_2_freq_button.clicked.connect(self.set_add_freq_to_output)
        tab_2_surnames_tag_button.clicked.connect(self.set_include_surname_tag)
        tab_2_simple_or_trad_button.clicked.connect(self.set_simp_or_trad)

        list_of_widgets = [
            [ tab_2_heading ],
            [ create_horizontal_rule() ],
            [ tab_2_simple_or_trad_label, tab_2_simple_or_trad_button ],
            [ create_horizontal_rule() ],
            [ tab_2_hsk_label, tab_2_hsk_input, tab_2_tocfl_label, tab_2_tocfl_input ],
            [ tab_2_freq_lower_limit_label, tab_2_freq_lower_limit_input, tab_2_freq_upper_limit_label, tab_2_freq_upper_limit_input ],
            [ create_horizontal_rule() ],
            [ tab_2_freq_label, tab_2_freq_button, tab_2_POS_label, tab_2_pos_button ],
            [ tab_2_sort_by_freq_label, tab_2_sort_by_freq_button, tab_2_add_surnames_tag_label, tab_2_surnames_tag_button ],
        ]

        tab_2_layout = place_in_grid(QGridLayout(), list_of_widgets)

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
        tab_3_finish_button.clicked.connect(lambda:
                self.set_deck_name(tab_1_deck_name_box.text()))
        tab_3_finish_button.clicked.connect(lambda:
                self.set_zh_input(tab_1_text_box.toPlainText()))
        tab_3_finish_button.clicked.connect(lambda:
                self.set_upper_freq_bound(tab_2_freq_upper_limit_input.value()))
        tab_3_finish_button.clicked.connect(lambda:
                self.set_lower_freq_bound(tab_2_freq_lower_limit_input.value()))
        tab_3_finish_button.clicked.connect(lambda:
                zh_analyser.analyse(self.zh_input, self.sort_by_freq,
                    self.add_freq_to_output, self.hsk_level, self.tocfl_level,
                    self.simp_or_trad, self.add_parts_of_speech_to_output,
                    self.upper_freq_bound, self.lower_freq_bound,
                    self.deck_name, self.include_surname_tag))
        tab_3_finish_button.clicked.connect(lambda: self.close())

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

    def set_sort_by_freq(self):
        self.sort_by_freq = not self.sort_by_freq

    def set_include_surname_tag(self):
        self.include_surname_tag = not self.include_surname_tag

    def set_include_surname_def(self):
        self.include_surname_def = not self.include_surname_def

    def set_add_parts_of_speech_to_output(self):
        self.add_parts_of_speech_to_output = not self.add_parts_of_speech_to_output

    def set_hsk_level(self, level):
        self.hsk_level = level

    def set_tocfl_level(self, level):
        self.tocfl_level = level

    def set_add_freq_to_output(self):
        self.add_freq_to_output = not self.add_freq_to_output

    def set_upper_freq_bound(self, bound):
        if self.upper_freq_bound > self.lower_freq_bound:
            self.upper_freq_bound = bound

    def set_lower_freq_bound(self, bound):
        if self.lower_freq_bound < self.upper_freq_bound:
            self.lower_freq_bound = bound

    def set_simp_or_trad(self):
        if self.simp_or_trad == 'trad':
            self.simp_or_trad = 'simp'
        else:
            self.simp_or_trad = 'trad'

    def set_deck_name(self, _deck_name):
        self.deck_name = _deck_name

    def set_zh_input(self, _zh_input):
        self.zh_input = _zh_input
