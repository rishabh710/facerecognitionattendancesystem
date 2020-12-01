import tkinter as tk
from tkinter import Message , Text
import cv2,os
import csv
import numpy as np
from PIL import  Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.font as font


window = tk.Tk()
window.title("Face Detection Attendance System")
window.geometry('1280x720')
window.iconbitmap('Logo.ico')
dialog_title='QUIT'
dialog_user='Are you sure?'
window.configure(background='snow')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0,weight=1)

message = tk.Label(window, text = "Face Detection Based Attendance Management System" , bg="cyan", fg="black", width=50, height=3, font=('times',30,'italic bold underline'))
message.place(x=100,y=20)

lbl=tk.Label(window, text= "Enter Id", width=20, height = 2, fg="black", bg="deep pink", font=('times',15, 'bold'))
lbl.place(x=200,y=200)
txt= tk.Entry(window,width=20, bg="yellow", fg="red", font=('times', 25, 'bold'))
txt.place(x=550,y=210)

lbl2 =tk.Label(window, text="Enter Name", width= 20, fg="black", bg="deep pink", height=2, font=('times',15, 'bold'))
lbl2.place(x=200, y=300)
txt2= tk.Entry(window,width=20, bg="yellow", fg="red", font=('times', 25, 'bold'))
txt2.place(x=550,y=310)

lbl3 =tk.Label(window, text="Notification", width= 20, fg="white", bg="Green", height=2, font=('times',15, 'bold'))
lbl3.place(x=200, y=400)

message = tk.Label(window, text="", bg="yellow", fg="red", width = 30, height= 2, activebackground = "yellow", font=('times',15, 'bold'))
message.place(x=550,y=400)

lbl3 =tk.Label(window, text="Attendance", width= 20, fg="white", bg="Green", height=2, font=('times',15, 'bold underline'))
lbl3.place(x=200, y=620)

message2= tk.Label(window, text=" ", bg="yellow", fg="red", width = 30, height= 2, activebackground = "yellow", font=('times',15, 'bold'))
message2.place(x=550,y=620)

def clear():
    txt.delete(first=0, last= 22)

def clear2():
    txt2.delete(first=0, last=22)

def TakeImages():
    Id = (txt.get())
    Name = (txt2.get())
    if(Id.isnumeric() and Name.isalpha()):
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImages\ " + Name + "." + Id + '.' + str(sampleNum) + ".jpg",gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 70:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Saved for Id : " + Id + " Name : " + Name
            row = [Id, Name]
            with open('StudentDetails\studentDetails.csv', 'a+',newline='') as csvFile:
                   writer = csv.writer(csvFile)
                   writer.writerow(row)
            csvFile.close()
            message.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    else:
        if(Id.isnumeric()):
            res="Enter Numeric Value Only!!"
            message.configure(text=res)
        elif(Name.isalpha()):
            res="Enter Character Name Only!!"
            message.configure(text=res)
        else:
            res="You have not Enter any Value!!"
            message.configure(text=res)
            
        
            
def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath="haarcascade_frontalface_default.xml"
    detector=cv2.CascadeClassifier(harcascadePath)
    faces,Id= getImagesAndLabels("TrainingImages")
    recognizer.train(faces,np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text=res)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    Ids=[]
    for imagePath in imagePaths:
        pilImage=Image.open(imagePath).convert('L')
        imageNp=np.array(pilImage, 'uint8')
        Id= int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces,Ids
    
def subject():
    global sub
    sub = tk.Tk()
    sub.title("Subject")
    sub.geometry('700x200')
    sub.iconbitmap('Logo.ico')
    sub.configure(background='snow')
    subject=tk.Label(sub, text= "Enter Subject", width=20, height = 2, fg="black", bg="deep pink", font=('times',15, 'bold'))
    subject.place(x=10, y=30)
    global sub1
    sub1= tk.Entry(sub,width=20, bg="yellow", fg="red", font=('times', 25, 'bold'))
    sub1.place(x=310,y=35)
    okbutton=tk.Button(sub, text="Take Attendance", command=TrackImages, fg="white", bg= "blue2", width=20, height=2, activebackground="Red", font=('times',15, 'bold'))
    okbutton.place(x=190,y=110)

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath="haarcascade_frontalface_default.xml"
    facesCascade= cv2.CascadeClassifier(harcascadePath)
    df=pd.read_csv("StudentDetails\studentDetails.csv")
    cam= cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names= ['Id', 'Name', 'Date', 'Time']
    attendance= pd.DataFrame(columns = col_names)
    fps=0
    while True:
        ret,im = cam.read() 
        gray= cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces= facesCascade.detectMultiScale(gray, 1.3, 5)
        for(x,y,w,h) in faces:
            Id,conf=recognizer.predict(gray[y:y+h, x:x+w])
            fps=fps+1
            if (conf<50):
                ts=time.time()
                date=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id) + "-" +aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 4)
                cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)
            else:
                Id='Unknown'
                tt=str(Id)
                if(conf>75):
                    noOfFile=len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image"+str(noOfFile)+".jpg", im[y:y+h,x:x+w])
                cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
        attendance=attendance.drop_duplicates(['Id'],keep='first')
        cv2.imshow('im',im)
        if cv2.waitKey(100) & 0xFF == ord('q'):
                        break
        elif fps > 70:
                  break
    ts = time.time()
    date =datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute ,Second=timeStamp.split(":")
    
    currentSubject=sub1.get()
    fileName="Attendance/Attendance_" +currentSubject+"_"+date+"_" + Hour+ "_"+ Minute+ "_" + Second+ ".csv"
    attendance=attendance.drop_duplicates(['Id'],keep='first')
    attendance.to_csv(fileName, index=False)
    sub.destroy()
    cam.release()
    cv2.destroyAllWindows()
    res=attendance
    message2.configure(text=res)
    
    
    

clearButton= tk.Button(window, text="Clear", command=clear, fg="black", bg="deep pink", width=20, height=2, activebackground="Red", font=('times',15, 'bold'))
clearButton.place(x=950,y=210)

clearButton2= tk.Button(window, text="Clear", command=clear2, fg="black", bg="deep pink", width=20, height=2, activebackground="Red", font=('times',15, 'bold'))
clearButton2.place(x=950,y=310)

takeImg= tk.Button(window, text=" Take Images", command=TakeImages, fg="white", bg= "blue2", width=20, height=2, activebackground="Red", font=('times',15, 'bold'))
takeImg.place(x=90,y=500)

trainImg= tk.Button(window, text=" Train Images", command=TrainImages, fg="black", bg= "lawn green", width=20, height=2, activebackground="Red", font=('times',15, 'bold'))
trainImg.place(x=390,y=500)

trackImg= tk.Button(window, text=" Track Images", command=subject, fg="white", bg= "blue2", width=20, height=2, activebackground="Red", font=('times',15, 'bold'))
trackImg.place(x=690,y=500)

quitWindow= tk.Button(window, text="Quit", command=window.destroy, fg="black", bg= "lawn green", width=20, height=2, activebackground="Red", font=('times',15, 'bold'))
quitWindow.place(x=990,y=500)

window.mainloop()





 
