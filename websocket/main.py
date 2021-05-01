from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Creating a flask app and using it to instantiate a socket object
app = Flask(__name__, static_url_path="", static_folder="static")
socketio = SocketIO(app)

# values['slider1'] and values['slider2'] store the current value of the sliders
# This is done to prevent data loss on page reload by client.
values = {
    'slider1': 25,
    'slider2': 0,
}


# Handler for default flask route
# Using jinja template to render html along with slider value as input
@app.route('/')
def index():
    return render_template('index.html', **values)


# Handler for a message recieved over 'connect' channel
@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})


@socketio.on('after connect')
def test_after_connect(msg):
    print(f"after connect got message: {msg}")


@socketio.on('Slider value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)


# Notice how socketio.run takes care of app instantiation as well.
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
