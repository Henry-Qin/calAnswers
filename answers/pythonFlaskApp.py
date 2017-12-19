from flask import Flask, flash, redirect, render_template, request, session, abort
from pymongo import MongoClient
import json

client = MongoClient("localhost:27017")
db = client['CalAnswers']

app = Flask(__name__)

cols = {'Calender_Year', 'Department_desc', 'Gender_Desc',  'Job_Type', 'Employee_Count', 'Avg_Age'}
 
@app.route("/")
def index():
    return render_template('index.html')

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
            if searchEntry[i] not in cols:
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
    # except:
    #     return "ERROR"
    print(recordsList)
    return json.dumps(recordsList)

if __name__ == "__main__":
    app.run()

