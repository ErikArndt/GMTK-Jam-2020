import const

def draw_menu(surface):
    title_text = const.TITLE_FONT.render("Fireship", True, const.WHITE)
    surface.blit(title_text, (100, 100))
    wt_text = const.TITLE_FONT_SM.render("(Working Title)", True, const.WHITE)
    surface.blit(wt_text, (100, 100 + title_text.get_height()))
    start_text = const.DEFAULT_FONT.render("Click anywhere to begin", True, const.WHITE)
    surface.blit(start_text, (const.WIN_LENGTH/2 - start_text.get_width()/2, 450))
