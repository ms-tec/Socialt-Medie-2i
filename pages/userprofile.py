import dominate
from dominate.tags import *

from sanic import Sanic

from pages.menu import show_menu

def user_profile(user):
    """Helper function for displaying profile info."""
    with div(id='profile-info'):
        h1(user.username)
        img(src=user.img_path)
        p(user.desc)

def edit_profile(app_name, user):
    """Full page for editing a user profile."""
    app = Sanic.get_app(app_name)
    doc = dominate.document(title=f'{app_name} | Rediger profil')

    with doc.head:
        link(rel='stylesheet', href=app.url_for('static',
                                                name='static',
                                                filename='style.css'))
    
    with doc:
        with div(id='contents'):
            menu_items = [
                ('Forside', '/'),
                ('Log ud', '/logout'),
                ('Ny post', '/write'),
            ]
            show_menu(menu_items)
            with form(cls='profile-form', enctype="multipart/form-data", method='POST', action='/update_profile'):
                with div(id='profile-info'):
                    h1(f'{user.username} - rediger profil')
                    img(src=user.img_path)
                    label('Vælg profilbillede:', for_='profile-icon')
                    input_(type='file',
                           name='profile-icon',
                           accept="image/png, image/jpg")
                    textarea(user.desc,
                             cls='desc-inpt',
                             name='description',
                             placeholder='Indtast beskrivelse...')
                    input_(type='submit', value='Gem', cls='button')

    return doc.render()