import os
from flask import Flask, request, jsonify
from face_match import match_algorithm, find_face

app = Flask(__name__, static_url_path='', static_folder='./',)

@app.route('/')
def index():
    return jsonify({"message": "API Start"})

@app.route('/upload-nid', methods=['GET', 'POST'])
def uploadNid():
    if request.method == 'GET':
        return jsonify({"result": "Its A post request Please use a 'POST' method"})

    if request.method == 'POST':
        nid_number = request.form['nid_number']
        static_file = request.files['the_file']
        filename = static_file.filename
        
        # file formate check
        if filename.endswith("png") or filename.endswith("jpg") or filename.endswith("jpeg"):
            pass
        else:
            return jsonify({"message": "Only jpg or png files are allowed"})




        # Match face with others faces
        # result = match_algorithm(nid_number, static_file)
        # print('result', result)
        

        for root, dirs, files in os.walk("./img/old"):
            if nid_number in dirs:
                print('dirs', dirs)
                old_path = './img/old/' + nid_number + '/' + filename
                static_file.save(old_path)


                # face check on image
                has_face = find_face(static_file, old_path)
                if has_face[0]:
                    pass
                else:
                    return jsonify({"message":has_face[1]})

                return jsonify({"nid_number": nid_number, "image": filename, "message": "File save successfully"})
            else:
                os.mkdir('./img/old/' + nid_number)
                os.mkdir('./img/new/' + nid_number)
                static_file.save('./img/old/' + nid_number + '/' + filename)
                return jsonify({
                    "nid_number": nid_number,
                    "image": filename,
                    "message": "Creat a folder and File save"
                })
            

        # return 'ok' #{"nid_number": nid_number, "result": result[0], "matching-percentage": result[1]}




@app.route('/face-match', methods=['GET', 'POST'])
def faceMatch():
    if request.method == 'GET':
        return jsonify({"result": "Its A post request Please use a 'POST' method"})
    if request.method == 'POST':
        nid_number = request.form['nid_number']
        static_file = request.files['the_file']
        filename = static_file.filename

        if filename.endswith("png") or filename.endswith("jpg") or filename.endswith("jpeg"):
            pass
        else:
            return jsonify({"message": "Only jpg or png files are allowed"})

        for root, dirs, files in os.walk("./img/new"):
            if nid_number in dirs:
                static_file.save('./img/new/' + nid_number + '/compaer.jpg')

                result = match_algorithm(nid_number)
                print(result)

                return jsonify({
                    "nid_number": nid_number,
                    "result": result[0],
                    "matching-percentage": result[1],
                    "match_image_path": '/img/new/' + nid_number + '/compaer.jpg',
                    "old_image_path": '/img/old/' + nid_number + '/' + result[2]
                })
            else:
                return jsonify({ "nid_number": nid_number, "message": "This nid number isn't registerd yet" })


