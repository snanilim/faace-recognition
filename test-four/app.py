import os
from flask import Flask, request, jsonify
from face_match import match_algorithm, find_face
from datetime import datetime

from PIL import Image
from io import BytesIO
import re, time, base64

app = Flask(__name__, static_url_path='', static_folder='./',)

@app.route('/')
def index():
    return jsonify({"message": "API Start"})

@app.route('/upload-nid', methods=['GET', 'POST'])
def uploadNid():
    if request.method == 'GET':
        return jsonify({"result": "Its A post request Please use a 'POST' method"})

    if request.method == 'POST':
        print('body', type(request.data))
        print('body', request.get_json()['nid_number'])
        nid_number = request.get_json()['nid_number']
        base64_image = request.get_json()['img_path']
        img_name = request.get_json()['img_name']

        base64_data = re.sub('^data:image/.+;base64,', '', base64_image)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        static_file = Image.open(image_data)

        now = datetime.now()
        timestamp = datetime.timestamp(now)
        filename = str(timestamp) + '.' + img_name
        

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


                # face and single face check on image
                has_face = find_face(static_file, old_path)
                if has_face[0]:
                    pass
                else:
                    return jsonify({"message":has_face[1]})


                # same face check on image
                isSameFace = match_algorithm(nid_number, old_path, filename)
                print('isSameFace', isSameFace)
                if isSameFace == None:
                    os.remove(old_path)
                    return jsonify({"message": "Some issue on this image please try again or change this image"})
                else:    
                    if isSameFace[0]:
                        pass
                    else:
                        return jsonify({
                            "nid_number": nid_number,
                            "image": filename,
                            "message": isSameFace[3]
                        })


                return jsonify({"nid_number": nid_number, "image": filename, "message": "File save successfully"})
            else:
                print('no dirs')
                os.mkdir('./img/old/' + nid_number)
                os.mkdir('./img/new/' + nid_number)
                static_file.save('./img/old/' + nid_number + '/' + filename)
                return jsonify({
                    "nid_number": nid_number,
                    "image": filename,
                    "message": "Create a folder and image save"
                })
            

        # return 'ok' #{"nid_number": nid_number, "result": result[0], "matching-percentage": result[1]}




@app.route('/face-match', methods=['GET', 'POST'])
def faceMatch():
    if request.method == 'GET':
        return jsonify({"result": "Its A post request Please use a 'POST' method"})
    if request.method == 'POST':
        nid_number = request.get_json()['nid_number']
        base64_image = request.get_json()['img_path']
        img_name = request.get_json()['img_name']

        base64_data = re.sub('^data:image/.+;base64,', '', base64_image)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        static_file = Image.open(image_data)

        filename = img_name

        if filename.endswith("png") or filename.endswith("jpg") or filename.endswith("jpeg"):
            pass
        else:
            return jsonify({"message": "Only jpg or png files are allowed"})

        for root, dirs, files in os.walk("./img/new"):
            if nid_number in dirs:
                static_file.convert('RGB').save('./img/new/' + nid_number + '/compaer.jpg')

                result = match_algorithm(nid_number)
                print('result', result)

                if result == None:
                    return jsonify({"message": "Some issue on this image please try again or change this image"})
                else:
                    return jsonify({
                        "nid_number": nid_number,
                        "result": result[0],
                        "matching_percentage": result[1],
                        "match_image_path": '/img/new/' + nid_number + '/compaer.jpg',
                        "old_image_path": '/img/old/' + nid_number + '/' + result[2],
                        "message": "Compare are done show result below"
                    })
            else:
                return jsonify({ "nid_number": nid_number, "message": "This nid number isn't registerd yet" })


