#!/usr/bin/env python
import os, webbrowser
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import flask_chess_manager

UPLOAD_FOLDER = '/home/ron/chessbot/tensorflow_chessbot/uploadfolder'
ALLOWED_EXTENSIONS = set(['txt', 'gif', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

FEN = None
FLIPFEN = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return '''<!DOCTYPE html>
<html>
<head>
<script type="text/javascript">
//Code will go here
window.onload = function() {
    document.getElementById("pasteTarget").
        addEventListener("paste", handlePaste);
};

function handlePaste(e) {
    for (var i = 0 ; i < e.clipboardData.items.length ; i++) {
        var item = e.clipboardData.items[i];
        console.log("Item type: " + item.type);
        if (item.type.indexOf("image") != -1) {
            uploadFile(item.getAsFile());
        } else {
            console.log("Discarding non-image paste data");
        }
    }
}

function uploadFile(file) {
    var xhr = new XMLHttpRequest();

    xhr.upload.onprogress = function(e) {
        var percentComplete = (e.loaded / e.total) * 100;
        console.log("Uploaded: " + percentComplete + "%");
    };

    xhr.onload = function() {
        if (xhr.status == 200) {
            alert("Sucess! Upload completed");
        } else {
            alert("Error! Upload failed");
        }
    };

    xhr.onerror = function() {
        alert("Error! Upload failed. Can not connect to server.");
    };

    xhr.open("POST", "FileUploader", false);
    xhr.setRequestHeader("Content-Type", file.type);
    xhr.send(file);
    window.location.href = "result"
}
</script>
</head>
<body>
<div style="width: 200px; height: 200px; background: grey" id="pasteTarget">
Click and paste here.
</div>
</body>
</html>'''

@app.route('/result', methods=['GET'])
def result():
    "print result"
    return '''<html>
<head>
</head>
<body>
<a href="https://lichess.org/analysis/{}" target="_blank">Fen</a>
<a href="https://lichess.org/analysis/{}_b" target="_blank">Flipfen</a>
</body></html>'''.format(FEN, FLIPFEN)

@app.route('/FileUploader', methods=['POST'])
def fileUploader():
    file('./uploadfolder/image.png', 'w').write(request.data)
    fen, flipfen = flask_chess_manager.run_chessbot_with_image('./uploadfolder/image.png')
    global FEN
    global FLIPFEN
    FEN = fen
    FLIPFEN = flipfen
    return redirect(url_for('result'))

if __name__ == "__main__":
    app.run(host='192.168.138.131', port=5001, debug=True)
