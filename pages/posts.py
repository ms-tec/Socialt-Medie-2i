from urllib.parse import quote
import dominate
from dominate.tags import *

from sanic import Sanic

import pages.userprofile as userprofile

def show_posts(app_name, posts=[], user=None):
    app = Sanic.get_app(app_name)
    doc = dominate.document(title=f'{app_name} | Posts')

    with doc.head:
        link(rel='stylesheet', href=app.url_for('static',
                                                name='static',
                                                filename='style.css'))

    with doc:
        with div(id='contents'):
            with ul(cls='menu'):
                with li(cls='menu_item'):
                    a('Forside', cls='button post_button', href='/')
                with li(cls='menu_item'):
                    a('Log ud', cls='button post_button', href='/logout')
                with li(cls='menu_item'):
                    a('Ny post', cls='button post_button', href='/write')
            if user is not None:
                userprofile.user_profile(user)
            for display_post in posts:
                with div(cls='post'):
                    h1(display_post.post.title)
                    with div(cls='author'):
                        a(f'af: {display_post.author.username}',
                          href=f'/u/{quote(display_post.author.username)}',
                          cls='author_link')
                    with div():
                        lines = filter(bool, display_post.post.contents.splitlines())
                        for par in lines:
                            p(par)

    return doc.render()

def create_page(app_name):
    app = Sanic.get_app(app_name)
    doc = dominate.document(title=f'{app_name} | Skriv')

    with doc.head:
        link(rel='stylesheet', href=app.url_for('static',
                                                name='static',
                                                filename='style.css'))

    with doc:
        with div(id='contents'):
            with ul(cls='menu'):
                with li(cls='menu_item'):
                    a('Forside', cls='button post_button', href='/')
                with li(cls='menu_item'):
                    a('Log ud', cls='button post_button', href='/logout')
            with form(cls='post-form', method='POST', action='/post'):
                with div(cls='post'):
                    input_(type='text', cls='title_inp',
                           name='title',
                           placeholder='Indtast titel...')
                    textarea(cls='contents_inp',
                             name='contents',
                             placeholder='Indtast tekst...')
                input_(type='submit', value='Post', cls='button')

    return doc.render()