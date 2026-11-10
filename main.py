from flask import Flask, render_template,request
import uuid
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# CHANGE 1: make sure the folders exist (static/reels was missing, which broke the gallery)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static/reels", exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()
    if request.method == "POST":
        print(request.files.keys())
        rec_id = request.form.get("myid")
        desc = request.form.get("text")
        input_files = []
        for key, value in request.files.items():
            print(key, value)
            # Upload the file
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                if(not(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], rec_id)))):
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], rec_id))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], rec_id,  filename))
                input_files.append(filename)  # CHANGE 2: was file.filename, but the saved name is the cleaned one
                print(file.filename)
            # Capture the description and save it to a file
            # CHANGE 3: file name is now description.txt, because generate_process.py reads that name
            with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "description.txt"), "w") as f:
                f.write(desc)
        for fl in input_files:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id,  "input.txt"), "a") as f:
                f.write(f"file '{fl}'\nduration 1\n")
        # CHANGE 4: tell the worker the upload is complete, so it doesn't pick up a half-saved folder
        open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "ready.txt"), "w").close()

    return render_template("create.html", myid=myid)
@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    return render_template("gallery.html",reels=reels)

app.run(debug=True)