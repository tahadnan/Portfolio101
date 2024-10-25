from flask import Flask, render_template, url_for
import csv
from datetime import datetime
from flask import request, redirect
app = Flask(__name__)
email_storage = {"current_email": ""}
info_storage = {}
@app.route("/")
def Home():
    return render_template('index.html')
@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        csv_writer = csv.writer(database,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([timestamp, data['email'],data['subject'], data['message']])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data=data)
            email_storage["current_email"] = request.form.get("email")
            print(email_storage["current_email"])
            print(data)
            return redirect('thankyou.html')
        except:
            return 'Did not save to database.'
    else:
        return "Something went wrong, try again buddy."
@app.route('/thankyou.html')
def thankyou():
    with open('database.txt','w') as file:
        # for k,v in info_storage.items():
        #     file.write(f"{k}:{v}")
        file.write(str(info_storage))
    return render_template("thankyou.html", info=email_storage["current_email"])

