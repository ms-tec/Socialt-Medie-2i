from urllib.parse import unquote
from sanic import Sanic
from sanic.log import logger
from sanic.response import html, redirect

import datetime

# global configuration
import config

# DAOs
from dao import DAO
import user
import post

# auth
from auth import protected, new_token, del_token

# pages
import pages.posts as posts

app = Sanic(config.APP_NAME)
app.static('static/', 'static')
app.ctx.msg = ""

# Create database tables
userDAO = user.UserDAO()
postDAO = post.PostDAO()
userDAO.create_table()
postDAO.create_table()

# Endpoints
@app.get("/")
@protected
async def index_page(request):
    all_posts = postDAO.fetch_all_display()
    return html(posts.show_posts(config.APP_NAME, all_posts))

@app.get("/u/<username>")
@protected
async def user_page(request, username: str):
    all_posts = postDAO.fetch_by_user(unquote(username))
    return html(posts.show_posts(config.APP_NAME, all_posts))

@app.get("/write")
@protected
async def write_page(request):
    return html(posts.create_page(config.APP_NAME))

@app.post("/post")
@protected
async def make_post(request):
    if not ('title' in request.form and
            request.form['title']):
        return redirect("/write")
    
    title = request.form['title'][0]
    contents = ""
    if 'contents' in request.form and request.form['contents']:
        contents = request.form['contents'][0]

    print(contents)

    usrid = userDAO.get_user_id(request.ctx.username)

    pst = post.Post(usrid, title, contents, datetime.datetime.utcnow())
    postDAO.store(pst)
    return redirect("/")

@app.post("/login")
async def login(request):
    if not ('uname' in request.form and
            'pword' in request.form and
            request.form['uname']   and
            request.form['pword']):
        app.ctx.msg = "Udfyld alle felter."
        return redirect("/")

    username = request.form['uname'][0]
    password = request.form['pword'][0]

    usr = userDAO.get_user(username)
    if not usr:
        app.ctx.msg = "Brugernavn findes ikke."
        return redirect("/")

    k = usr.make_key(password)
    if k != usr.key:
        app.ctx.msg = "Forkert adgangskode."
        return redirect("/")

    tok = new_token(username)
    resp = redirect("/")
    resp.cookies['auth'] = username + ':' + tok
    resp.cookies['auth']['expires'] = datetime.datetime.utcnow() +\
                                      datetime.timedelta(days=1)
    return resp

@app.get("/logout")
@protected
async def logout(request):
    del_token(request.ctx.username)
    logger.info(f"Logged out: {request.ctx.username}")
    return redirect("/")

@app.post("/register")
async def register(request):
    if not ('uname'  in request.form and
            'pword'  in request.form and
            'rpword' in request.form and
            request.form['uname']    and
            request.form['pword']    and
            request.form['rpword']):
        app.ctx.msg = "Udfyld alle felter."
        return redirect("/")
    
    username = request.form['uname'][0]
    password1 = request.form['pword'][0]
    password2 = request.form['rpword'][0]

    if password1 != password2:
        app.ctx.msg = "Passwords matcher ikke."
        return redirect("/")

    try:
        usr = userDAO.new(username, password1)
        userDAO.store(usr)
        logger.info(f"New user: {username}")
        return await login(request)
    except user.UserExistsError as err:
        logger.info(str(err))
        app.ctx.msg = f"Brugernavnet {username} er optaget."
        return redirect("/")

app.run(host='localhost', port=8080)