# Import required libraries
import cv2
import numpy as np
import dlib
import time as t
from datetime import date
from datetime import datetime
import pandas as pd
import sqlalchemy
import pymysql
#create engine to connect to aws instance
engine = sqlalchemy.create_engine("mysql+pymysql://Manager:detroit123!@ascmconference-mariadb.c8kgwuuup0za.us-east-2.rds.amazonaws.com/ascmdb", pool_pre_ping=True, echo=False)

#tab = sqlalchemy.Table(name='ascmfeed',  mysql_engine='InnoDB', mariadb_engine='InnoDB')
#tab.create()
#set df
dfcols = ['date', 'time', 'count']
indexcol = []
datecol = []
timecol = []
countcol = []
 
# Connects to your computer's default camera
cap = cv2.VideoCapture(0)
 
 
# Detect the coordinates
detector = dlib.get_frontal_face_detector()

today = date.today()
 
# Capture frames continuously
while True:
    t.sleep(1)
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 30)
 
    # RGB to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
 
    # Iterator to count faces
    i = 0
    for face in faces:
 
        # Get the coordinates of faces
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
 
        # Increment iterator for each face in faces
        i = i+1
            
        # Display the box and faces
        cv2.putText(frame, 'face num'+str(i), (x-10, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
                # Display the resulting frame
        #cv2.imshow('frame', frame)
        
    if i >= 1:
        
        #print(face, i)
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
     
        # This command let's us quit with the "q" button on a keyboard.
    else:
        continue
    
    print(df)
    
    df.to_sql(name='ascmfeed_v2', con=engine, if_exists='append')
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
# Release the capture and destroy the windows
cap.release()
cv2.destroyAllWindows()
