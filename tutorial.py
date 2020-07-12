from text import TextBox
import const

def get_text(progress):
    tut_text_box = None
    if progress == 0:
        tut_text = 'Why hello there! Nice to meet you! A space ship stranded in a ' + \
            'distant galaxy isn\'t the best place to raise a potted plant, but I won\'t ' + \
            'complain. Why is a cactus talking to you, you ask? Simple! You\'ve been away ' + \
            'from Earth so long you\'ve started hallucinating. Space really does mess with ' + \
            'your mind, doesn\'t it?'
        tut_text_box = TextBox(tut_text, const.LARGE, None, True)
        tut_text_box.add_button('Yeah, I suppose so.', const.GREEN)
    elif progress == 1:
        tut_text = 'While I\'m here, I should probably explain how to pilot the ship. ' + \
            'You look insane enough to have forgotten, and a refresher couldn\'t hurt, ' + \
            'could it?'
        tut_text_box = TextBox(tut_text, const.MED)
        tut_text_box.add_button('Sure', const.GREEN)
        tut_text_box.add_button('Skip Tutorial', const.BLUE)
    elif progress == 2:
        tut_text = 'This room to the right is the Bridge. It\'s where you\'re standing ' + \
            'right now. You can control the entire ship from the dashboard here, without ' + \
            'ever needing to move around. Sweet, right?'
        tut_text_box = TextBox(tut_text, const.MED)
        tut_text_box.set_position(185, 100)
        tut_text_box.add_button('Yeah', const.GREEN)
    elif progress == 3:
        tut_text = 'This room to the left is on fire. Don\'t panic - it\'s actually a good thing! It\'s ' + \
            'a special form of interquazar-protostatic flames that can power our engines from ' + \
            'anywhere on the ship, as long as it doesn\'t go out!'
        tut_text_box = TextBox(tut_text, const.MED)
        tut_text_box.set_position(300, 100)
        tut_text_box.add_button('Cool!', const.GREEN)
    elif progress == 4:
        tut_text = 'Of course, flames tend to spread, and you don\'t want this fire to spread ' + \
            'too rapidly. If these flames reach certain rooms they can disable your systems, and ' + \
            'if they reach the bridge, you\'ll be burned alive!'
        tut_text_box = TextBox(tut_text, const.MED)
        tut_text_box.set_position(300, 100)
        tut_text_box.add_button('Not cool!', const.GREEN)
    return tut_text_box
