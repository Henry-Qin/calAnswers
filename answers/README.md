Run the Python Flask App from the answers directory:
```python3 pythonFlaskApp.py```
Go to your browser and navigate to
```http://localhost:5000/```

This is a simple web app that queries a MongoDB database using natural language built on Python + Flask, MongoDB, AngularJS, and HTML/CSS.

In a separate bash process, start a MongoDB instance by running:
```mongod```

Edits will need to be made on variable values because they are currently for use on my files and directory structure.

The index.html of this web app contains a search bar and an upload button. A user can upload a .csv file using the upload button, that will then be queried
by whatever is inside the search bar. This is accomplished by addCollection() in the app, which creates a subprocess that calls
mongoimport with the file, and imports the csv file into the database. Search queries are currently being processed as (columnName, value) pairs. 
An example query would be:
```Avg_Age 40 Year 2010```
which would return all rows in the database whose 'Avg_Age' == 40 and 'Year' == 2010

