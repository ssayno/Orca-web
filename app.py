import json
import time

from flask import Flask
from flask import render_template, request
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
from Utils.timer_get_cookies import start_requests
from Utils.extract_excel_file import extract_and_storage

import os
import sqlite3


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = "Uploads"
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

socketio = SocketIO(app)

# scheduler usage
app.config.from_object(Config())
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


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
        package_count = extract_and_storage(file_path)
        print("pcalkfjas", package_count
              )
        test_print()
    except Exception as e:
        print("Error", e)
    return '?'


@scheduler.task('interval', id='1', seconds=600)
def test_print():
    print("start >>>>>>")
    current_path = os.path.dirname(__file__)
    db_file = os.path.join(current_path, 'static', 'Data', 'orca.db')
    with sqlite3.connect(db_file) as connect:
        cursor = connect.cursor()
        try:
            cursor.execute(
                'select id from packageNumbers'
            )
            connect.commit()
            packages = cursor.fetchall()
        except Exception as e:
            print("update error", e)
            connect.rollback()
            packages = None
        finally:
            if packages:
                start = 0
                packages = [
                    item[0] for item in packages
                ]
                package_count = len(packages)
                socketio.emit('update', json.dumps(
                    {
                        'type': 'init',
                        'count': f'{package_count}',
                        'data': None
                    }
                ))
                while True:
                    end = start + 9
                    if end > package_count:
                        result = start_requests(packages[start:])
                        socketio.emit('update', json.dumps({
                            'type': 'add',
                            'data': result,
                            'count': package_count - start
                        }))
                        break
                    else:
                        result = start_requests(packages[start: end])
                        socketio.emit('update', json.dumps({
                            'type': 'add',
                            'data': result,
                            'count': end - start
                        }))
                    start += 9
                    time.sleep(10)
        cursor.close()


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
