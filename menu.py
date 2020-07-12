import const

def draw_menu(surface):
    title_text_1 = const.TITLE_FONT.render("I am not", True, const.WHITE)
    surface.blit(title_text_1, (100, 100))
    title_text_2 = const.TITLE_FONT.render("on fire", True, const.ORANGE)
    surface.blit(title_text_2, (100, 100 + title_text_1.get_height()))
    title_text_3 = const.TITLE_FONT.render(" yet", True, const.WHITE)
    surface.blit(title_text_3, (100 + title_text_2.get_width(), 100 + title_text_1.get_height()))
    wt_text = const.TITLE_FONT_SM.render("Featuring Cactus Coolboy", True, const.WHITE)
    surface.blit(wt_text, (100, 100 + title_text_1.get_height() + title_text_2.get_height()))
    start_text = const.DEFAULT_FONT.render("Click anywhere to begin", True, const.WHITE)
    surface.blit(start_text, (const.WIN_LENGTH/2 - start_text.get_width()/2, 450))
