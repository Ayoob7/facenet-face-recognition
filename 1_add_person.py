# Import OpenCV2 for image processing
import cv2
import os
import re
import sqlite3
from tkinter import messagebox


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


from tkinter import *

window = Tk()
window.title("Registration")
window.configure(bg='#ADD8E6')

var1 = StringVar()
l1 = Label(window, textvariable=var1, bg="#ADD8E6", fg='black', relief=RAISED)
var1.set("Person ID:")
l1.grid(row=2, column=3, sticky=N + E + W + S)

var2 = StringVar()
l2 = Label(window, textvariable=var2, bg="#ADD8E6", fg='black', relief=RAISED)
var2.set("Name:")
l2.grid(row=3, column=3, sticky=N + E + W + S)

var3 = StringVar()
l3 = Label(window, textvariable=var3, bg="#ADD8E6", fg='black', relief=RAISED)
var3.set("Date of Birth:")
l3.grid(row=4, column=3, sticky=N + E + W + S)

var4 = StringVar()
l4 = Label(window, textvariable=var4, bg="#ADD8E6", fg='black', relief=RAISED)
var4.set("Email:")
l4.grid(row=5, column=3, sticky=N + E + W + S)

var5 = StringVar()
l5 = Label(window, textvariable=var5, bg="#ADD8E6", fg='black', relief=RAISED)
var5.set("Address:")
l5.grid(row=6, column=3, sticky=N + E + W + S)


e1Val = StringVar()
e1 = Entry(window, textvariable=e1Val, bg="#ADD8E6", fg='black')
e1.grid(row=2, column=5)

e2Val = StringVar()
e2 = Entry(window, textvariable=e2Val, bg="#ADD8E6", fg='black')
e2.grid(row=3, column=5)

e3Val = StringVar()
e3 = Entry(window, textvariable=e3Val, bg="#ADD8E6", fg='black')
e3.grid(row=4, column=5)

e4Val = StringVar()
e4 = Entry(window, textvariable=e4Val, bg="#ADD8E6", fg='black')
e4.grid(row=5, column=5)

e5Val = StringVar()
e5 = Entry(window, textvariable=e5Val, bg="#ADD8E6", fg='black')
e5.grid(row=6, column=5)




def ok():
    return e1Val.get(), e2Val.get(), e3Val.get(), e4Val.get(), e5Val.get()


def endIt():
    window.destroy()


b1 = Button(window, text="OK", bg="#ADD8E6", fg='black', command=endIt)
b1.grid(row=10, column=5)

window.mainloop()

# get face id into program
id, name, age, email, address = ok()
params = (int(id), name, age, email, address)
#######


conn = sqlite3.connect('database/persons.db')
conn.cursor()
conn.execute('''CREATE TABLE IF NOT EXISTS Persons
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         DOB            TEXT     NOT NULL,
         EMAIL        CHAR(50),
         ADDRESS    TEXT    CHAR(50));''')

sql = "INSERT INTO Persons (ID,NAME,DOB,EMAIL,ADDRESS) VALUES (?, ?, ?, ?,?)"
conn.execute(sql, params)
print(conn.execute("SELECT * from Persons"))
conn.commit()
conn.close()


face_id = int(id)
name_id = name

# Start capturing video
vid_cam = cv2.VideoCapture(0)

# Detect object in video stream using Haarcascade Frontal Face
face_detector = cv2.CascadeClassifier('dir_util/haarcascade_frontalface_default.xml')

# Initialize sample face image
count = 0

assure_path_exists("images/")

font = cv2.FONT_HERSHEY_SIMPLEX

# Start looping
while (True):

    # Capture video frame
    _, image_frame = vid_cam.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    # Detect frames of different sizes, list of faces rectangles
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # Loops for each faces
    for (x, y, w, h) in faces:
        # Crop the image frame into rectangle
        cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(image_frame, "Rotate your face Clockwise", (x, y - 10), font, 0.5, (120, 255, 120), 2, 1)

        # Increment sample face image
        count += 1

        if count == 1:
            # Save the captured image into the datasets folder
            cv2.imwrite("images/"+name_id +"_"+str(face_id) +".jpg", gray[y:y + h, x:x + w])

        # Display the video frame, with bounded rectangle on the person's face
        cv2.imshow('frame', image_frame)

    # To stop taking video, press 'q' for at least 100ms
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # If image taken reach 30, stop taking video
    elif count >= 30:
        print("Successfully Captured")
        break

# Stop video
vid_cam.release()

# Close all started windows
cv2.destroyAllWindows()
