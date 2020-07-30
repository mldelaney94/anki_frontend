try:
    from aqt import mw
    import anki
except ImportError:
    from test.dummy_aqt import mw
    from test import dummy_anki as anki

def getOrCreateDeck(deckName):
    deck_id = mw.col.decks.id(deckName)
    deck = mw.col.decks.get(deck_id)
    mw.col.decks.save(deck)
    mw.col.reset()
    mw.reset()
    return deck
