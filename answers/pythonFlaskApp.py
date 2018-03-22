from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from pymongo import MongoClient
import json
from werkzeug import secure_filename
import csv
import subprocess

client = MongoClient("localhost:27017")
dbString = 'CalAnswers'
db = client[dbString]

app = Flask(__name__)
UPLOAD_FOLDER = '/Users/henryqin/research/calAnswers/answers/uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
currFileName = None
currCols = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            global currFileName
            currFileName = filename
            extractColumnNames(filename)
            addCollection(filename)
            return redirect(url_for('index'))
    return render_template('index.html')


def extractColumnNames(currFileName):
    with open("/Users/henryqin/research/calAnswers/answers/uploads/" + currFileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        global currCols
        currCols = set(reader.fieldnames)

@app.route("/getRecords", methods=['POST'])
def getRecords():
    recordsList = []
    searchEntry = str(request.data.decode("utf-8")).split(" ")
    length = len(searchEntry)
    if length % 2 != 0:
        return json.dumps(recordsList)
    query = {}
    currCol = None
    for i in range(length):
        if i % 2 == 0:
            if searchEntry[i] not in currCols:
                return json.dumps(recordsList)
            else:
                currCol = searchEntry[i]
        else:
            if searchEntry[i].isdecimal():
                query[currCol] = float(searchEntry[i])
            elif searchEntry[i].isdigit():
                query[currCol] = int(searchEntry[i])
            else:
                query[currCol] = searchEntry[i]
    records = db[currFileName].find(query)
    for record in records:
        recordItem = {}
        for col in currCols:
            recordItem[col] = str(record[col])
        recordsList.append(recordItem)
    return json.dumps(recordsList)

def addCollection(fileName):
    subprocess.call(["mongoimport", "--db", dbString, "--collection", fileName, "--type", "csv", "--headerline", "--drop", "--file", "/Users/henryqin/research/calAnswers/answers/uploads/" + fileName])

if __name__ == "__main__":
    app.run()

