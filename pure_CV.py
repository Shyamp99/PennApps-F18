import face_recognition as fr
import cv2 as cv
import pymongo
from pymongo import MongoClient
import base64

# client = MongoClient('')
#
# db = client["medar"]
# collection = db.test_collection
#
# faces_col = db["faces"]
# patient_col = db["patients"]
#
# users_col = db["users"]
# profile_col = db["profile"]

face_encodings = []
face_locations = []
face_names = []
known_face_encodings = []
known_face_names = []
encoded = ""

# the actual training and encoding
def addPerson(name):
    # train cv to recognize face after it construct a set of vectors and then encodes it
    # id = users_col.find(name)
    # patient = profile_col.find(id)
    # picture_link = patient.img
    # picture = base64.decodestring(picture_link)

    new_person_image = fr.load_image_file('shyam_pic.jpg')
    new_person_encoding = fr.face_encodings(new_person_image)[0]
    known_face_encodings.append(new_person_encoding)
    encoded = new_person_encoding
    known_face_names.append(name)


    initialize_camera()


def initialize_camera():
    found_name = ""
    # this enables the video feed
    vid_cap = cv.VideoCapture(0)
    process_this_frame = True
    name = "Unknown"
    while True:
        # take a single frame from the feed and then resize it to 1/4 off the size for faster processing
        ret, frame = vid_cap.read()
        small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # a small frame to easily show that the computer recognizes someone
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = fr.face_locations(rgb_small_frame)
            face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            # for face_encoding in face_encodings:
            #     # See if the face is a match for the known face(s)
            #     matches = fr.compare_faces(known_face_encodings, face_encoding)
            #     name = "Unknown"
            #     medical_info = "N/A"
            #
            #     counter = 0
            #     temp = False
            #     for i in matches:
            #         for j in i:
            #             if j == True:
            #                 temp = True
            #                 first_match = j
            #                 break
            #             counter += 1
            #
            #     # If a match was found within encoded_faces, just use the first one.
            #     if temp:
            #         first_match_index = counter
            #         name = known_face_names[first_match_index]
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = fr.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)
            process_this_frame = not process_this_frame  # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
                font = cv.FONT_HERSHEY_DUPLEX
                cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv.imshow('Video', frame)
        # exut by pressing 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # terminating the final processes
    vid_cap.release()
    cv.destroyAllWindows()
    #id = users_col.find(name)
    #patient = profile_col.find(id)
    #return patient;
    print(name)




def start():
    # REGULAR VERSION WITHOUT THE POPUP#

    print("Welcome to Medi-Vision")
    print("Type in 1 if you'd like to add someone to the database or Type 2 initialize the camera: ")
    func = int(input(""))
    print(func)
    if func == 1:
        addPerson(input("Provide a name: "))
    else:
        initialize_camera()

        # NOW WITH POPUP THAT INCLUDES THE BUTTONS
        # tk = Tk()
        # var = StringVar()
        # label = Label(tk, textvariable=var, relief=RAISED)
        #
        # var.set("Welcome to Medi-Vision \n"+"Would you like to add someone or"
        #                                     "launch Medi-Vision", )  # What you want the text to be
        # label.pack()
        #
        # tk.geometry("100x150")  # The size of the box
        # tk.wm_title("Insight")  # The name of it
        # b1 = Button(master, text="Starup Camera", command=initialize_camera())
        # b2 = Button(master, text="Add New Person", command=addPerson())
        # b1.pack(side = LEFT)
        # b2.pack(side = RIGHT)
        # tk.mainloop()

start()


#face_landmarks_list = fr.face_landmarks(image)
