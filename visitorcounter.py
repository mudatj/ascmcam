#import required libraries
import cv2
import numpy as np
import dlib
import time
from datetime import date
from datetime import datetime
import pandas as pd
import sqlalchemy
import pymysql

#create engine to connect to aws instance
engine = sqlalchemy.create_engine("mysql+pymysql://user:password@instanceurl/dbname", pool_pre_ping=True, echo=False)

#set df
dfcols = ['date', 'time', 'count']
indexcol = []
datecol = []
timecol = []
countcol = []
 
#connects to your computer's default camera
cap = cv2.VideoCapture(0)
 
 
#detect the coordinates
detector = dlib.get_frontal_face_detector()

today = date.today()
 
#capture frames every second
while True:
    tim.sleep(1)
    #capture each frame
    ret, frame = cap.read()
    #capture one frame per second
    frame = cv2.flip(frame, 1)
 
    #rgb to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
 
    #iterate to count faces
    i = 0
    for face in faces:
 
        #facial recognition of coordinates
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        #creates rectangle w/ coordinates
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
 
        #iterate for each face
        i = i+1
            
        #display the box and faces
        cv2.putText(frame, 'face num'+str(i), (x-10, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
                #display the resulting frame if not commented
        #cv2.imshow('frame', frame)
    #only count data with faces in the frame    
    if i >= 1:
        index = datetime.now()
        time = datetime.now().strftime('%H:%M:%S')
        indexcol_a = index
        datecol_a = today
        timecol_b = time
        countcol_c = i
        indexcol.append(indexcol_a)
        datecol.append(datecol_a)
        timecol.append(timecol_b)
        countcol.append(countcol_c)
    
        df = pd.DataFrame(indexcol, columns=['index'])
        df['date'] = datecol
        df['time'] = timecol
        df['count'] = countcol
        #df.index = pd.to_datetime(df.index)
        df = df.set_index('index')
        df = df.resample('1Min')
        df = df.mean()
     
    else:
        continue
    
    print(df)
    #replaces all existing table versions in the database table
    df.to_sql(name=tablename, con=engine, if_exists='replace')
    

    #this command lets us quit with the "q" button on a keyboard  
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
#release the capture and destroy the windows
cap.release()
cv2.destroyAllWindows()
