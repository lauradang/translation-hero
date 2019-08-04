from flask import *
import os
import io

from api_processing import detect_image
from languagedictionary import languages


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

IMAGE_FOLDER = os.path.join('static', 'images')
STYLE_FOLDER = os.path.join('static', 'style')

app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
app.config['STYLE_FOLDER'] = STYLE_FOLDER

@app.route("/")
def home():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'world.png')
    style = os.path.join(app.config['STYLE_FOLDER'], 'style.css')
    script = os.path.join(app.config['STYLE_FOLDER'], 'script.js')
    return render_template (
        "uploadPage.html", 
        languages=languages, 
        logo=full_filename, 
        style=style,
        script=script
    )

@app.route("/test")
def test():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    target = os.path.join(APP_ROOT, "images/")
    print(target)
    print(request.files.getlist("file"))
    print("JDKLSAJFDKSALJFDKSALJFDKSALJFKDSALJFDKSALJ")
    if not os.path.isdir(target):
        os.mkdir(target)
    
    for upload in request.files.getlist("file"):
        filename = upload.filename
        ext = os.path.splitext(filename)[1]
        destination = "/".join([target, filename])

        upload.save(destination)
        # user_language = request.form.get("userLanguage")
        user_language = request.form.get("userLanguage")
        print(user_language)

        obj_name_english = detect_image(user_language)['obj_name']
        obj_name_user_lang = detect_image(user_language)['translation']

        os.remove(destination) 

    return render_template (
        "process.html", 
        obj_name_english=obj_name_english, 
        obj_name_user_lang=obj_name_user_lang,
        user_language=user_language
    )

if __name__ == '__main__':
    app.run()
