import os
import subprocess
from datetime import datetime
from tkinter import *
from tkinter import messagebox, simpledialog
import cv2
import face_recognition as face_rec
import numpy as np
import pyttsx3 as textSpeach
from PIL import Image, ImageTk
from ttkbootstrap import Style


# Initialize the ttkbootstrap style
style = Style(theme="darkly")
root = style.master
root.geometry("900x780")
root.title("Smart Attendance System")
style.theme_use("darkly")
image_icon = PhotoImage(file="logo.png")

root.iconphoto(False, image_icon)
Label(root, text="SMART STUDENT ATTENDANCE SYSTEM", font=("tims new roman", 30, "bold"), bg="black", fg="white").pack(
    ipady=20)
Button(root, text="EXIT", fg="white", bg="#AE2321", font="15", command=root.destroy).place(x=760, y=720)


def open_file_with_password():
    password = simpledialog.askstring("Password", "Only for Teacher: ", show='*')

    if password == "12345":
        open_file('attendance.csv')
    else:
        messagebox.showerror("Invalid Password", "Incorrect password. Please try again.")


Button(root, text="OPEN ATTENDANCE FILE", fg="black", bg="yellow", font="15",
       command=open_file_with_password).place(x=50, y=720)


def open_file(file_path):
    try:
        subprocess.Popen(['start', 'excel', file_path], shell=True)
    except Exception as e:
        print(f"Error opening file: {e}")


engine = textSpeach.init()


# Function to resize an image
def resize(img, size):
    width = int(img.shape[1] * size)
    height = int(img.shape[0] * size)
    dimension = (width, height)
    return cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)


# Function to save an image
def save_image(image, file_name):
    cv2.imwrite(file_name, image)



def detect_and_take_photo(frame, student_name):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the color range for detecting a mobile phone screen
    lower_color = np.array([0, 60, 148], dtype=np.uint8)
    upper_color = np.array([0, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_color, upper_color)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mobile_phone_detected = False

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Check if the contour matches the aspect ratio of a mobile phone screen
        aspect_ratio = w / h
        print(f"Aspect Ratio: {aspect_ratio}")
        if 0.5 < aspect_ratio < 2.0:
            mobile_phone_detected = True
            break

    if mobile_phone_detected:
        # Save the cheating photo with student name
        cheating_photo_name = f"cheating_{student_name}_photo.jpg"
        save_image(frame, cheating_photo_name)

        # Display a message box indicating cheating is detected
        messagebox.showinfo("Cheating Detected", f"Cheating student {student_name} detected! Mobile phone screen detected.")
        print(f"Cheating student {student_name} detected! Cheating photo saved as {cheating_photo_name}")

        return cheating_photo_name


    return None





# Path to the directory containing student images
path = 'student_image'
student_image = []
studentName = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    student_image.append(curImg)
    studentName.append(os.path.splitext(cl)[0])


# Function to encode student images
def finEncoding(images):
    encoding_list = []
    for img in images:
        img = resize(img, 0.50)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeimg = face_rec.face_encodings(img)[0]
        encoding_list.append(encodeimg)
    return encoding_list


# Function to mark attendance for known students
def MarkAttendance(name, file_name='attendance.csv'):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write('Name,Time,Date')

    with open(file_name, 'r+') as f:
        myDataList = f.readlines()
        nameList = [entry.split(',')[0] for entry in myDataList]

        if name not in nameList:
            now = datetime.now()
            timestr = now.strftime('%H:%M:%S  %p')
            datestr = now.strftime('%x')
            f.writelines(f'\n{name}, {timestr},{datestr}')
            engine.say('Thank you for your Attendance')
            engine.runAndWait()

            welcome_message = f"Thank You!, {name}"
            messagebox.showinfo("Attendance Marked", welcome_message)


# Function to mark attendance for unknown people
def MarkAttendance(name, file_name='attendance.csv'):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write('Name,Time,Date')

    with open(file_name, 'r+') as f:
        myDataList = f.readlines()
        nameList = [entry.split(',')[0] for entry in myDataList]

        if name not in nameList:
            now = datetime.now()
            timestr = now.strftime('%H:%M:%S  %p')
            datestr = now.strftime('%x')
            f.writelines(f'\n{name}, {timestr},{datestr}')
            engine.say('Thank you your Attendance')
            engine.runAndWait()

            welcome_message = f"Thank You!, {name}"
            messagebox.showinfo("Attendance Marked", welcome_message)

# Function to mark attendance for unknown people
def MarkUnknownAttendance(name, file_name='unknown_people.csv'):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            f.write('Name,Time,Date')

    now = datetime.now()
    timestr = now.strftime('%H:%M  %p')
    datestr = now.strftime('%x')
    with open(file_name, 'a') as f:
        f.writelines(f'\n{name}, {timestr},{datestr}')
        engine.say('Unknown person detected')
      # engine.runAndWait()


encode_list = finEncoding(student_image)

vid = cv2.VideoCapture(0)


# Create a button to capture photo of unknown student
capture_button = Button(root, text="ADD NEW STUDENT PHOTO", fg="black", bg="orange", font="15",
                        command=lambda: capture_unknown_student_photo(name))
capture_button.place(x=380, y=720)

# Function to capture and save photo of unknown student
def capture_unknown_student_photo(student_name):
    _, frame = vid.read()

    # Display a message box for manual renaming
    new_name = simpledialog.askstring("Capture Photo", "Enter a name for the unknown student:")
    if new_name is None or new_name == "":
        messagebox.showwarning("Invalid Name", "Please enter a valid name.")
        return

    unknown_photo_name = f"{new_name}.jpg"
    save_image(frame, f"student_image/{unknown_photo_name}")

    success_message = f"Photo of unknown student captured and saved as {unknown_photo_name}"
    messagebox.showinfo("Photo Captured", success_message)


# Create labels to display name
name_label = Label(root, text="", font=("tims new roman", 14, "bold"), bg="white", fg="black")
name_label.pack(pady=10)

time_label = Label(root, text="", font=("tims new roman", 10, "bold"), bg="yellow", fg="black")
time_label.pack(pady=10)

video_label = Label(root, background="black")
video_label.pack(pady="5")

# Initialize video capture
vid = cv2.VideoCapture(0)

name = ""


def update_video():
    global name
    success, frame = vid.read()

    if not success or frame is None:
        print("Error reading frame from video capture.")
        return

    frames = cv2.resize(frame, (0, 0), None, 0.5, 0.5)
    frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)

    faces_in_frame = face_rec.face_locations(frames)
    encode_in_frame = face_rec.face_encodings(frames, faces_in_frame)

    for encodFace, facloc in zip(encode_in_frame, faces_in_frame):
        matches = face_rec.compare_faces(encode_list, encodFace)
        facdis = face_rec.face_distance(encode_list, encodFace)
        matchIndex = np.argmin(facdis)

        if matches[matchIndex]:
            name = studentName[matchIndex].upper()
            y1, x2, y2, x1 = facloc
            y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 25), (x1, y1), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 - 10, y2 + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            MarkAttendance(name)

            name_label.config(text=f"Name & RE No: {name}")
        else:
            unknown_people = "Unknown Person"
            y1, x2, y2, x1 = facloc
            y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 25), (x1, y1), (255, 0, 0), cv2.FILLED)
            cv2.putText(frame, unknown_people, (x1 - 10, y2 + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
            MarkUnknownAttendance(unknown_people)
            name_label.config(text=f"Name: {unknown_people}")

    detect_and_take_photo(frames, name)

    now = datetime.now()
    current_time = now.strftime('%H:%M:%S %p \n %A \n %x')
    time_label.config(text=f"Time: {current_time}")

    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.config(image=imgtk)
    video_label.after(10, update_video)


update_video()
root.mainloop()
