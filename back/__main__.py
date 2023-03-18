from flask import Flask, request
#import flask-socketio
from flask_socketio import SocketIO, emit

users = {}
messages = {}
app = Flask(__name__)
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

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    socketio.run(app)

