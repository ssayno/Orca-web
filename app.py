import os.path

from flask import Flask
from flask import render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = "Uploads"
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])
socketio = SocketIO(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@socketio.on('connect')
def connectFunc(data):
    print('received message:', data)
    emit("connect", "what you do")


@app.route('/tracker')
def packer_tracker():
    return render_template('packTracker.html')


@app.route('/upload', methods=["POST"])
def parseExcel():
    try:
        file_ = request.files['file']
        print(file_)
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], file_.filename
        )
        file_.save(file_path)

    except Exception as e:
        print("Error", e)
    finally:
        socketio.emit("packerUpdate", "get your file, tomorrow we will extract this file")
    return "Ok get file"


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
