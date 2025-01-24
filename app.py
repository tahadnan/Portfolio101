import os
from flask import Flask, render_template, url_for
import csv
from datetime import datetime
from flask import request, redirect


app = Flask(__name__)
name_storage = {"current_name": ""}
info_storage = {}
session = {}

LANGUAGE_PATHS = {
    'en': 'English',
    'fr': 'French'
}

def get_template_path(language, template_name):
    return os.path.join(LANGUAGE_PATHS[language],template_name)

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        csv_writer = csv.writer(database,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["\n",timestamp,data['fullname'],data['email'],data['subject'], data['message']])

@app.route("/")
def default_home():
    return redirect(url_for('home', lang='en'))

@app.route("/<string:lang>")
def home(lang):
    if lang in LANGUAGE_PATHS:
        session["current_language"] = lang
        return render_template(get_template_path(lang, 'index.html'))
    return redirect(url_for('home', lang='en'))

@app.route("/<string:lang>/<string:page_name>")
def html_page(lang,page_name):
    if lang in LANGUAGE_PATHS:
        session['current_language'] = lang
        print(render_template(get_template_path(lang,page_name)))
        return render_template(get_template_path(lang,page_name))
    return redirect(url_for('home', lang='en'))

@app.route('/<lang>/submit_form', methods=['POST', 'GET'])
def submit(lang):
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            name_storage["current_name"] = request.form.get("fullname")
            return redirect(url_for('thankyou', lang=lang))
        except Exception as e:
            error_messages = {
                'en': "Failed to save to database.",
                'fr': "Échec de la sauvegarde dans la base de données."
            }
            return error_messages.get(lang, error_messages['en'])
    return redirect(url_for('home', lang=lang))

@app.route('/<lang>/thankyou.html')
def thankyou(lang):
    template_name = 'thankyou.html'
    return render_template(get_template_path(lang, template_name), info=name_storage["current_name"])



