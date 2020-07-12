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
        tut_text_box.set_position(300, 150)
        tut_text_box.add_button('Cool!', const.GREEN)
    elif progress == 4:
        tut_text = 'Of course, flames tend to spread, and you don\'t want this fire to spread ' + \
            'too rapidly. If these flames reach certain rooms they can disable your systems, and ' + \
            'if they reach the bridge, you\'ll be burned alive!'
        tut_text_box = TextBox(tut_text, const.MED)
        tut_text_box.set_position(300, 150)
        tut_text_box.add_button('Not cool!', const.GREEN)
    elif progress == 5:
        tut_text = 'Luckily, we have a sprinkler system you can use to put out the flames. ' + \
            'Just click a room to place a sprinkler, and it will start spraying water in that room. ' + \
            'Click the room again to remove it.'
        tut_text_box = TextBox(tut_text, const.MED)
        tut_text_box.set_position(300, 90)
        tut_text_box.add_button('Seems simple enough', const.GREEN)
    elif progress == 6:
        tut_text = 'Be careful, though, because you can only place 3 sprinklers at a time! ' + \
            'You also have a limited amount of water that will deplete as the sprinklers run. ' + \
            'The more sprinklers you\'ve placed, the faster it will deplete.'
        tut_text_box = TextBox(tut_text, const.MED)
        tut_text_box.set_position(300, 90)
        tut_text_box.add_button('Now I\'m thirsty', const.GREEN)
    elif progress == 7:
        tut_text = 'One last thing I should mention: At certain times, alien ships may try to ' + \
            'come at us and steal our interquazar flames. If not dealt with, these ships will keep ' + \
            'firing at us until our hull is breached.'
        tut_text_box = TextBox(tut_text, const.MED)
        tut_text_box.add_button('That sounds bad', const.GREEN)
    elif progress == 8:
        tut_text = 'You can see these aliens coming on the radar in the bottom right, and you can ' + \
            'use the port (top) and starboard (bottom) lasers to shoot them before they get close ' + \
            'enough to fire at us.'
        tut_text_box = TextBox(tut_text, const.MED)
        tut_text_box.set_position(100, 250)
        tut_text_box.add_button('This ship has lasers?!', const.GREEN)
    elif progress == 9:
        tut_text = 'Remember, if the radar room is on fire, you won\'t be able to see anything there, ' + \
            'and if the laser rooms are on fire, you won\'t be able to fire at aliens. Manage the fire ' + \
            'carefully and you should be fine.'
        tut_text_box = TextBox(tut_text, const.MED)
        tut_text_box.set_position(100, 250)
        tut_text_box.add_button('Yeah, whatever', const.GREEN)
    elif progress == 10:
        tut_text = 'Well, that\'s about all the advice I have. It shouldn\'t take too long to reach ' + \
            'the nearest spaceport. Click the cactus on the dashboard to repeat this tutorial at ' + \
            'any time. Good luck!'
        tut_text_box = TextBox(tut_text, const.MED)
        tut_text_box.add_button('We\'re screwed.', const.GREEN)
    return tut_text_box
