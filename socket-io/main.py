from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


def counter_thread():
    count = 0
    while count <= 100:
        socketio.emit('counter_update', {'count': count}, namespace='/counter')
        count += 1
        socketio.sleep(1)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/time1')
def time1():
    return render_template('counter.html')


@socketio.on('connect', namespace='/counter')
def counter_connect():
    global count_thread
    if 'count_thread' not in globals():
        count_thread = socketio.start_background_task(target=counter_thread)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)
