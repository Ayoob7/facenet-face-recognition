from tkinter import *
import os
from datetime import datetime

root = Tk()

root.configure(background="white")

def add_person():
    os.system("py 1_add_person.py")


def train_and_recognise_model():
    os.system("py 2_facenet.py")

def attend():
    #os.startfile(os.getcwd() + "/firebase/attendance_files/attendance" + str(datetime.now().date()) + '.xls')
    pass

def deleteStudents():
    os.system("py 4_delete_users.py")

def exitProgram():
    root.destroy()


root.title("Facial Recognition system from FaceNet")
# stting title for the window

# creating a text label
Label(root, text="FACE RECOGNITION SYSTEM", font=("calibri", 20), fg="white", bg="black", height=2).grid(row=0,
                                                                                                         rowspan=2,
                                                                                                         columnspan=2,
                                                                                                         sticky=N + E + W + S,
                                                                                                         padx=5, pady=5)

# creating first button
Button(root, text="Add Person", font=("sans serif", 20), bg="#587795", fg='white', command=add_person).grid(row=3,
                                                                                                            column=0,
                                                                                                            sticky=W + E + N + S,
                                                                                                            padx=5,
                                                                                                            pady=5)

# creating second button
Button(root, text="Train and Recognise Model", font=("sans serif", 20), bg="#587795", fg='white', command=train_and_recognise_model).grid(row=3,
                                                                                                             column=1,
                                                                                                             sticky=N + E + W + S,
                                                                                                             padx=5,
                                                                                                             pady=5)


# creating attendance button
Button(root, text="Attendance Sheet", font=('calibri', 20), bg="#587795", fg="white", command=attend).grid(row=4,
                                                                                                           column=1,
                                                                                                           sticky=N + E + W + S,
                                                                                                           padx=5,
                                                                                                           pady=5)


Button(root, text="Delete Person", font=('calibri', 20), bg="#587795", fg="white", command=deleteStudents).grid(row=5,
                                                                                                                column=1,
                                                                                                                sticky=N + E + W + S,
                                                                                                                padx=5,
                                                                                                                pady=5)

# exit
Button(root, text="Exit", font=('calibri', 20), bg="#3D003D", fg="white", command=exitProgram).grid(row=9, columnspan=2,
                                                                                                    padx=5, pady=5)

root.mainloop()
