from aqt.qt import *
from aqt.utils import showInfo

from aqt import mw
from anki.errors import AnkiError

def place_in_tab_widget(tab_layout, list_of_widgets):
    """
    Automatically places the widgets on a gridlayout in the list's order.
    Only works with the specific placement required in tab 2
    """
    for row_indx, row in enumerate(list_of_widgets):
        for col_indx, widget in enumerate(row):
            col_span = -1 if len(row) == 1 else 1
            tab_layout.addWidget(widget, row_indx, col_indx, 1, col_span)

    #Next line ensures it looks the way it should, just remove to see what
    #happens without it
    tab_layout.setRowStretch(len(list_of_widgets), 100)
    tab_layout.setSpacing(10)
    return tab_layout
