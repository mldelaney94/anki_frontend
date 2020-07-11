from aqt.qt import *
from aqt.utils import showInfo

from aqt import mw
from anki.errors import AnkiError 

def place_in_tab_widget(tab_layout, list_of_widgets):
    """
    Automatically places the widgets on a gridlayout in the list's order.
    Only works with the specific placement required in tab 2
    """
    i = 2
    j = 0
    for widget in list_of_widgets:
        if widget.__class__.__name__ == 'QFrame':
            if j == 0:
                tab_layout.addWidget(widget, i, j, 1, -1)
            else:
                tab_layout.addWidget(widget, i+1, 0, 1, -1)
                i += 1
                j = 0
        else:
            tab_layout.addWidget(widget, i, j)
            if j == 3:
                i += 1
                j = 0
            else:
                j += 1

    #Next line ensures it looks the way it should, just remove to see what
    #happens without it
    tab_layout.setRowStretch(i+1, 100)
    tab_layout.setSpacing(10)
    return tab_layout
        
