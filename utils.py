from aqt.qt import *
from aqt.utils import showInfo

from aqt import mw
from anki.errors import AnkiError

def place_in_grid(grid_layout, list_of_widgets):
    """
    Automatically places the widgets on a gridlayout in the list's order.
    Only works with the specific placement required in tab 2
    """
    for row_indx, row in enumerate(list_of_widgets):
        for col_indx, widget in enumerate(row):
            col_span = -1 if len(row) == 1 else 1
            grid_layout.addWidget(widget, row_indx, col_indx, 1, col_span)

    #Next line ensures it looks the way it should, just remove to see what
    #happens without it
    grid_layout.setRowStretch(len(list_of_widgets), 100)
    grid_layout.setSpacing(10)
    return grid_layout


def create_horizontal_rule():
    """
    Returns a QFrame that is a sunken, horizontal rule.
    """
    rule = QFrame()
    rule.setFrameShape(QFrame.HLine)
    rule.setFrameShadow(QFrame.Sunken)
    return rule


def create_input_box(place_holder_text, tooltip):
    """
    Creates a QLineEdit with just enough width for the placeholder text
    """
    input_box = QLineEdit()
    input_box.setPlaceholderText(place_holder_text)

    #Sets width according to width of characters
    font = QFontMetrics(input_box.font())
    input_box.setFixedWidth(font.width("  " + place_holder_text + "  "))
    input_box.setToolTip(tooltip)

    return input_box
