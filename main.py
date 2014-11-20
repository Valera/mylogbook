from bottle import route, run, template


@route('/hello/<name>')
def hello(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route('/')
def index():
    return template('index')


run(host='localhost', port=8080, reloader=True)
