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

full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'world.png')
style = os.path.join(app.config['STYLE_FOLDER'], 'style.css')
script = os.path.join(app.config['STYLE_FOLDER'], 'script.js')

@app.route("/")
def home():
    uploaded = False
    return render_template (
        "uploadPage.html", 
        uploaded=uploaded,
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
    target = os.path.join(APP_ROOT, "images")

    if not os.path.isdir(target):
        os.mkdir(target)

    for upload in request.files.getlist("file"):
        filename = upload.filename
        destination = "/".join([target, filename])

        upload.save(destination)
        user_language = request.form.get("userLanguage")

        obj_name_english = detect_image(user_language)['obj_name']
        obj_name_user_lang = detect_image(user_language)['translation']

        os.remove(destination) 

    uploaded = True

    return render_template (
        "uploadPage.html", 
        uploaded=uploaded,
        obj_name_english=obj_name_english, 
        obj_name_user_lang=obj_name_user_lang,
        user_language=user_language,
        languages=languages, 
        logo=full_filename, 
        style=style,
        script=script
    )

if __name__ == '__main__':
    app.run(debug=False)
