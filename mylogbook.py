from bottle import route, run, template, static_file, request, redirect, response

import storage


@route('/hello/<name>')
def hello(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/')
def index():
    return template('index', text='')


@route('/static/<path:path>')
def callback(path):
    return static_file(path, 'static')


@route('/register')
def register():
    with storage.session_scope() as session:
        u = storage.User(request.query['name'], request.query['email'], request.query['password'])
        session.add(u)
    return redirect("/")


@route('/signin')
def signin():
    email = request.query['email']
    password = request.query['password']
    with storage.session_scope() as session:
        db_response = session.query(storage.User).filter_by(email=email).filter_by(password=password).all()
        if len(db_response) == 0:
            return redirect("/static/signin.html")
        user = db_response[0]
        us = storage.UserSession(user)
        response.set_cookie('id', us.token)
        session.add(us)
    return redirect("/")


def get_user(session):
    id_string = request.get_cookie('id', '')
    db_response = session.query(storage.UserSession).filter_by(token=id_string).all()
    assert(len(db_response) < 2)
    if len(db_response) == 0:
        return None
    user = session.query(storage.User).filter_by(id=db_response[0].user).all()[0]
    return user

@route("/projects")
def show_projects():
    with storage.session_scope() as session:
        user = get_user(session)
        if not user:
            return 'Please login'
        projects = []
        for proj in session.query(storage.Project).filter_by(user=user.id).all():
            projects.append(proj.name)
        return template('index', text='\n'.join(projects), user_name='')


@route('/info')
def info():
    token = request.get_cookie('id', '*')
    with storage.session_scope() as session:
        username = get_user(session)
        username = username.name if username else 'Unknown'
    return template('index', text=token, user_name=username)


run(host='localhost', port=8081, reloader=True)


