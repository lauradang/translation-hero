from flask import *
import os
import io

from api_processing import detect_image
from languagedictionary import languages

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    return render_template("uploadPage.html", languages=languages)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    target = os.path.join(APP_ROOT, "images/")

    if not os.path.isdir(target):
        os.mkdir(target)
    
    for upload in request.files.getlist("file"):
        filename = upload.filename
        ext = os.path.splitext(filename)[1]
        destination = "/".join([target, filename])

        upload.save(destination)
        user_language = request.form.get("userLanguage", None)

        obj_name_english = detect_image(user_language)['obj_name']
        obj_name_user_lang = detect_image(user_language)['translation']

        os.remove(destination) 

    return render_template (
        "process.html", 
        image_name=filename, 
        obj_name_english=obj_name_english, 
        obj_name_user_lang=obj_name_user_lang,
        user_language=user_language
    )

if __name__ == '__main__':
    app.run()
