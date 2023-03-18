from flask import Flask, request
#import flask-socketio
from flask_socketio import SocketIO, emit
print("hello world")
users = {}
messages = {}
app = Flask(__name__, static_folder='./front/build/', static_url_path='/')
app.config['SECRET_KEY'] = 'secret'
#init flask-socketio
socketio = SocketIO(app,cors_allowed_origins="*")

#
@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
@socketio.on('message')
def handle_message(data):
    print("asdadadadsdadad")
    print('received message: ' + data['message'])
    print(users[request.sid])
    emit('message', {'message': data['message'],'user':users[request.sid]['name']}, broadcast=True)

@socketio.on('login')
def login(data):
    print('login')
    print(data)
    users[request.sid] = {'name':data['username'],'room':'general'}
    print(users)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    if path == 'favicon.ico':
        return app.send_from_directory('public', 'favicon.ico')
    return app.send_static_file('index.html')

if __name__ == '__main__':
    socketio.run(app)

