from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
from pymongo import MongoClient
import json
from werkzeug import secure_filename
import csv
from subprocess import Popen, PIPE

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
            currFileName = filename
            extractColumnNames(currFileName)
            return redirect(url_for('index'))
    return render_template('index.html')


def extractColumnNames(currFileName):
    with open("uploads/" + currFileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        currCols = set(reader.fieldnames)

@app.route("/getRecords", methods=['POST'])
def getRecords():
    # try:
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
            query[currCol] = int(searchEntry[i]) if searchEntry[i].isdigit() else searchEntry[i]
    records = db['sample'].find(query)
    for record in records:
        recordItem = {
            'Calender_Year': str(record['Calender_Year']),
            'Department_desc': record['Department_desc'],
            'Gender_Desc': record['Gender_Desc'],
            'Job_Type': record['Job_Type'],
            'Employee_Count': str(record['Employee_Count']),
            'Avg_Age': str(record['Avg_Age'])
        }
        recordsList.append(recordItem)
    print(recordsList)
    return json.dumps(recordsList)

# @app.route("/addCollection", methods=['POST'])
# def addCollection():
#     mongoimport --db dbString --collection collectionName --type csv --headerline


if __name__ == "__main__":
    app.run()

