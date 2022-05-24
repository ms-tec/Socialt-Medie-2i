from dominate.tags import *

def show_menu(menu_items):
    with div(cls="menu"):
        with ul():
            for (txt, lnk) in menu_items:
                with li(cls='menu-item'):
                    a(txt, cls='button', href=lnk)