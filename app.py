import os.path

from flask import Flask
from flask import render_template, request
from Utils.timer_get_cookies import start_requests
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = "Uploads"
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])


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

    except Exception as e:
        print("Error", e)
    r = """
        YT2220621272046565
        YT2222021272078719
        YT2224121225000875
        YT2223921272038985
        YT2223921266009420
        YT2223721272045551
        YT2224121292004552
        YT2224121292005619
        YT2224121292004717
        YT2224121292018871
        YT2224122093000003
        YT2224221225000671
        YT2224221225000672
        YT2224221225000721
        YT2224221225000673
        """
    packer_numbers = [
        item.strip() for item in r.split("\n") if item.strip()
    ]
    print(packer_numbers)
    # start_requests('YT2222021272078719')
    return start_requests(packer_numbers[:9])


if __name__ == '__main__':
    Flask.run(app)
