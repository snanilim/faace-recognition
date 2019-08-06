from flask import Flask, request
from face_match import match_algorithm

app = Flask(__name__)

@app.route('/')
def index():
    return "API Start"

@app.route('/face-match', methods=['GET', 'POST'])
def faceMatch():
    if request.method == 'GET':
        return "Its A post request Please use a 'POST' method"
    if request.method == 'POST':
        nid_number = request.form['nid_number']
        static_file = request.files['the_file']
        static_file.save('./img/new/compaer.jpg')

        result = match_algorithm(nid_number)
        print(result)

        return {"nid_number": nid_number, "result": result[0], "matching-percentage": result[1]}