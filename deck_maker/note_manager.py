from aqt import mw
import anki

MODEL_FIELDS = ['front', 'pinyin', 'back', 'audio']
MODEL_NAME = "Chinese Prestudy"

def getOrCreateDeck(deckName):
    deck_id = mw.col.decks.id(deckName)
    deck = mw.col.decks.get(deck_id)
    mw.col.decks.save(deck)
    mw.col.reset()
    mw.reset()
    return deck

def createModel():
    #check for models existence
    model = mw.col.models.byName(MODEL_NAME)
    if model:
        return model

    model = mw.col.models.new(MODEL_NAME)
    
    for field_name in MODEL_FIELDS:
        field = mw.col.models.newField(field_name)
        mw.col.models.addField(model, field)

    t = mw.col.models.newTemplate("Card 1")
    t['qfmt'] = "{{front}}<br>{{pinyin}}<br>{{audio}}"
    t['afmt'] = "{{FrontSide}}<hr id=answer>{{back}}"
    mw.col.models.addTemplate(model, t)

    t = mw.col.models.newTemplate("Card 2")
    t['qfmt'] = "{{back}}"
    t['afmt'] = "{{FrontSide}}<hr id=answer>{{front}}<br>{{pinyin}}<br>{{audio}}"
    mw.col.models.addTemplate(model, t)

    model['css'] = '''
    .card {
        font-family: arial;
        font-size: 20px;
        text-align: left;
        color: black;
        background-color: white;
    }
    '''

    mw.col.models.add(model)
    mw.col.models.save(model)
    return model

def addNotesFromList(word_list):
    for word in word_list:
        n = mw.col.newNote()
        n['front'] = word[0]
        n['pinyin'] = word[1]
        n['back'] = word[2]
