from flask import *
import os
import io

from api_processing import detect_image

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    return render_template("uploadPage.html", title="hi")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, "images/")

    if not os.path.isdir(target):
        os.mkdir(target)
    
    for upload in request.files.getlist("file"):
        filename = upload.filename
        ext = os.path.splitext(filename)[1]
        destination = "/".join([target, filename])

        upload.save(destination)
        obj_name = detect_image("German")['obj_name']
        os.remove(destination) 

    return render_template("process.html", image_name=filename, obj_name=obj_name)

if __name__ == '__main__':
    app.run()
