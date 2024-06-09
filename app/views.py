from distutils.log import error
import mimetypes
from re import template
from app import app
from flask import render_template, request, send_file
from app.tts import syn
import io

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/call/project1", methods = ["POST"])
def call_project1(): 
    if (request.form['text']):
        text = request.form['text']
        outputs = syn.tts(text)
        out = io.BytesIO()
        syn.save_wav(outputs, out)
        return send_file(out, mimetype="audio/wav")
    else:
        return "Please enter text! :)", 400