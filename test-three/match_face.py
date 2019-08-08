import face_recognition
from PIL import Image, ImageDraw
import os

old_image_path = './img/old/'

for root, dirs, files in  os.walk(old_image_path):
    for i, file in enumerate(files):
        if file.endswith("png") or file.endswith("jpg"):
            print(i)
            print(len(files))


            old_image = face_recognition.load_image_file(old_image_path + file)
            old_image_encodings = face_recognition.face_encodings(old_image)[0]


            new_image = face_recognition.load_image_file('./img/new/filename.jpg')
            new_face_locations = face_recognition.face_locations(new_image)
            new_face_encodings = face_recognition.face_encodings(new_image, new_face_locations)

            # pil format
            pil_image = Image.fromarray(new_image)
            draw = ImageDraw.Draw(pil_image)

            # known_face_encodings = [
            #     bill_face_encoding,
            #     steve_face_encoding
            # ]


            base = os.path.basename(file)
            known_face_names = os.path.splitext(base)[0]

            # return True

            # Loop through faces in test image
            for(top, right, bottom, left), face_encoding in zip(new_face_locations, new_face_encodings):
                matches = face_recognition.compare_faces([old_image_encodings], face_encoding, tolerance=0.5)
                name = "Unknown Person"

                # if match
                if True in matches:
                    name = known_face_names

                    # draw box
                    draw.rectangle(((left, top), (right, bottom)), outline=(0,0,0))

                    # draw label
                    text_width, text_height = draw.textsize(name)
                    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0,0,0), outline=(0,0,0))
                    draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

                    del draw
                    pil_image.show()
                    pil_image.save('identify.jpg')

                    import sys
                    sys.exit()

                elif i == len(files) - 1:
                    # draw box
                    draw.rectangle(((left, top), (right, bottom)), outline=(0,0,0))

                    # draw label
                    text_width, text_height = draw.textsize(name)
                    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0,0,0), outline=(0,0,0))
                    draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

                    del draw
                    pil_image.show()
                    pil_image.save('identify.jpg')

        



