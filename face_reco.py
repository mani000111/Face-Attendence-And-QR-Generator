print("\t\t\tInitializing Face Recognition ....")

import face_recognition
import os,math,cv2,time,sys,frs_api
import numpy as np
from users_database import make_qr
print("\t\t\tOpening Attendance Book ....")
import attendance_system

#variable 

face_locations = []
face_encodings = []
face_names = []
known_face_encodings = []
known_face_names = []
process_current_frame = True
generated_qr_list = []
users_present_level = {}
users_conf_level = []
attendance_list = []
conf_int = 0

#reset switch

def reset_switch_checker():
    #reset users present conf level
    if frs_api.reset_present_conf_level:
        for user in users_present_level:
            users_present_level[user]=0
        frs_api.reset_present_conf_level=False
    
    #reset attendance list
    if frs_api.reset_attendance_switch:
        global attendance_list
        attendance_list=[]
        frs_api.reset_attendance_switch=False
    
    #reset generated qr list
    if frs_api.reset_qr_gena_list_switch:
        global generated_qr_list
        generated_qr_list = []
        frs_api.reset_qr_gena_list_switch=False



#mark attendance func
def mark_attendance(username):
    #make attendance
    attendance_system.make_attendance(username)

#calculate face accuracy
def calculate_accuracy(face_distance,face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

#face training ------------------------------------------------------------------------
print("\t\t\tTrainning the faces....\n")

train_time = time.time()
for image in os.listdir("users_datasets"):

    try:
        start_time = time.time()
        face_image = face_recognition.load_image_file(f"users_datasets\\{image}")
        face_encoding = face_recognition.face_encodings(face_image)[0]

        known_face_encodings.append(face_encoding)
        image_file_name = image.split(".")[0] #image file name
        known_face_names.append(image_file_name)
        users_present_level[image_file_name]=0
        print(f"{image_file_name} face data, trainned successful = {str(time.time()-start_time)[:4]} s")
    except:
        print(f"Unable to find faces in '{image}' !")
print(f"Total time taken to train faces : {time.time()-train_time} s")
print(f"\nTrained Faces : {known_face_names}")
#face training ------------------------------------------------------------------------

cv2.namedWindow("MANI", cv2.WINDOW_NORMAL)
cv2.resizeWindow("MANI", 450,800)

#input source -------------------------------------------------------------------------
cam = cv2.VideoCapture(0)
# cam = cv2.VideoCapture("elon.mp4")
#cam = cv2.VideoCapture("http://192.168.43.99:8080/video")
# cam = cv2.imread("test.jpg")
# frame = cam
#input source -------------------------------------------------------------------------

while True:

    #read cam
    ret, frame = cam.read()
    
    #a default condition
    if process_current_frame:
        #resize the cam frame
        small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        #convert resized frame to RGB frame
        rgb_small_frame = small_frame[:, :, ::-1]

        #find all faces in the cam
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        users_conf_level=[]
        for face_encoding in face_encodings:
            #if there is no faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            detected_user_name = "Unknown !"
            conf = "0 %"

            #if there is faces present
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                detected_user_name = known_face_names[best_match_index]
                conf = calculate_accuracy(face_distances[best_match_index])
                conf_int = round(float(conf.split("%")[0]))
                
                #face intelligent code
                if conf_int>=90:
                    #add conf level who are detected in frame
                    users_present_level[detected_user_name]+=conf_int
                    print(detected_user_name," : ",conf,"\nTotal present : ",users_present_level[detected_user_name])

                    #mark attendance condition
                    if detected_user_name not in attendance_list:
                        if users_present_level[detected_user_name]>700:
                            mark_attendance(detected_user_name)
                            attendance_list.append(detected_user_name)


                    #generate qr condition
                    if detected_user_name not in generated_qr_list:
                        #whoes has conf level more than 1000 ,they elligible to generate qr code and mark attendance
                        if users_present_level[detected_user_name]>700:
                            #make qr code for detected user
                            sta_code = make_qr(detected_user_name)
                            if sta_code==0:
                                generated_qr_list.append(detected_user_name)
                                print("qr code generated successfull for "+detected_user_name)
                                os.system(f'users_qrcode\\"{detected_user_name}.png"')
                            else:
                                print("! No Data's About "+detected_user_name)
                    

            face_names.append(f"{detected_user_name}")#append detected face
            users_conf_level.append(f"{conf}") #append detected face accuracy

    print("How manys detected : ",face_names,users_conf_level)
    process_current_frame = not process_current_frame

    # display labels on faces
    for (top, right, bottom, left), name, conf_level in zip(face_locations, face_names,users_conf_level):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        label_conf_int = round(float(conf_level.split("%")[0]))

        #putting label on face when accuracy is more than 92 %
        if label_conf_int>=90:
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 3)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0,255,0), -1)
            cv2.putText(frame, f"{name} [{conf_level}]", (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0,0), 2)
        elif conf_int<90:
            cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 3)
            cv2.putText(frame, f"Unknown !", (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2)

    #shows result in window
    cv2.imshow("MANI", frame)

    #interupt action
    if cv2.waitKey(1) == ord('q'):
        break

    #reset checker
    reset_switch_checker()

#release camera
try:cam.release()
except:pass

#destroy all windows
cv2.destroyAllWindows()
# attendance_system.frs.destroy()
sys.exit()





