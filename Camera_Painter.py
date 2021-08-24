import cv2
import numpy as np


# TRACKBARS
def nothing(x):
    pass

cv2.namedWindow("Choose Color")
cv2.createTrackbar("LH", "Choose Color", 0, 179, nothing)
cv2.createTrackbar("LS", "Choose Color", 0, 255, nothing)
cv2.createTrackbar("LV", "Choose Color", 0, 255, nothing)
cv2.createTrackbar("UH", "Choose Color", 179, 179, nothing)
cv2.createTrackbar("US", "Choose Color", 255, 255, nothing)
cv2.createTrackbar("UV", "Choose Color", 255, 255, nothing)

#COLORS
white=(255,255,255)
black=(0,0,0)
gray=(122,122,122)
red = (0,0,255)
blue= (255,0,0)
green=(0,139,0)  
gold=(0,201,238)
pink=(147,20,255)

colors=[blue,green,red,gold,black,pink,white,gray]
colorIndex = None

#List which will store points

blue_points = []
green_points = []
red_points = []
yellow_points = []
black_points = []

#Window We Will Paint On

PaintWindow=np.zeros((490,700,4))+254
RectLength=100
RectWidth=60

Xo=[10,130,230,330,430,530]

PaintWindow=cv2.rectangle(PaintWindow, (Xo[0],1),(30+RectLength,RectWidth),gray, -1 )
PaintWindow=cv2.rectangle(PaintWindow, (Xo[1],1),(Xo[1]+RectLength,RectWidth),colors[0], -1 )
PaintWindow=cv2.rectangle(PaintWindow, (Xo[2],1),(Xo[2]+RectLength,RectWidth),colors[1], -1 )
PaintWindow=cv2.rectangle(PaintWindow, (Xo[3],1),(Xo[3]+RectLength,RectWidth),colors[2], -1 )
PaintWindow=cv2.rectangle(PaintWindow, (Xo[4],1),(Xo[4]+RectLength,RectWidth),colors[3], -1 )
PaintWindow=cv2.rectangle(PaintWindow, (Xo[5],1),(Xo[5]+RectLength,RectWidth),colors[4], -1 )

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
cv2.putText(PaintWindow, 'Clear All', (15,30), font, 1, black, 2)
cv2.putText(PaintWindow, 'Blue', (150,30), font, 1, white, 2)
cv2.putText(PaintWindow, 'Green', (250,30), font, 1, white, 2)
cv2.putText(PaintWindow, 'Red', (350,30), font, 1, white, 2)
cv2.putText(PaintWindow, 'Gold', (450,30), font, 1, white, 2)
cv2.putText(PaintWindow, 'Black', (550,30), font, 1, white, 2)


#CAPTURE VIDEO
cap = cv2.VideoCapture(0)

while True:
    retValue , frame = cap.read()

    if retValue==True:
        frame=cv2.flip(frame,1)   #VideoCapture is inverted
        HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    # If we use this function later on all the rectangles and text will be included in the HSV
        points = [blue_points,green_points,red_points,yellow_points,black_points]
        

        # Rectangles filled with specific colors that we can draw with
        frame=cv2.rectangle(frame, (Xo[0],1),(30+RectLength,RectWidth),colors[-1], -1 )
        frame=cv2.rectangle(frame, (Xo[1],1),(Xo[1]+RectLength,RectWidth),colors[0], -1 )
        frame=cv2.rectangle(frame, (Xo[2],1),(Xo[2]+RectLength,RectWidth),colors[1], -1 )
        frame=cv2.rectangle(frame, (Xo[3],1),(Xo[3]+RectLength,RectWidth),colors[2], -1 )
        frame=cv2.rectangle(frame, (Xo[4],1),(Xo[4]+RectLength,RectWidth),colors[3], -1 )
        frame=cv2.rectangle(frame, (Xo[5],1),(Xo[5]+RectLength,RectWidth),colors[4], -1 )

        # Texts on the rectangles
        frame=cv2.putText(frame, 'Clear All', (15,30), font, 1, white, 2)
        frame=cv2.putText(frame, 'Blue', (150,30), font, 1, white, 2)
        frame=cv2.putText(frame, 'Green', (250,30), font, 1, white, 2)
        frame=cv2.putText(frame, 'Red', (350,30), font, 1, white, 2)
        frame=cv2.putText(frame, 'Gold', (450,30), font, 1, white, 2)
        frame=cv2.putText(frame, 'Black', (550,30), font, 1, white, 2)


        #Trackbars input 
        l_h = cv2.getTrackbarPos("LH", "Choose Color")
        l_s = cv2.getTrackbarPos("LS", "Choose Color")
        l_v = cv2.getTrackbarPos("LV", "Choose Color")
        u_h = cv2.getTrackbarPos("UH", "Choose Color")
        u_s = cv2.getTrackbarPos("US", "Choose Color")
        u_v = cv2.getTrackbarPos("UV", "Choose Color")

        lower = np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])

        # Masking

        mask= cv2.inRange(HSV,lower,upper)

        #Noise Removal
        kernal = np.ones( (5,5), np.uint8 )

        mask = cv2.erode(mask, kernal, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernal)
        mask = cv2.dilate(mask, kernal, iterations=1)
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        center=None
        if len(contours)> 0:
            # contour = Larget detected from contours ( Nearest to the screen )
            contour = sorted( contours , key=cv2.contourArea , reverse=True )[0]
            ((x,y),raduis) = cv2.minEnclosingCircle(contour)

            cv2.circle(frame, (int(x),int(y)) , int(raduis) , colors[-3], 2)
            
            M = cv2.moments(contour)

            center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
            

            # If the Y coordinate goes to one of the options at the top of the window then ..            #RectWidth = Height here
            if center[1] <= RectWidth:                             
            
                if Xo[0] < center[0] < Xo[1]: 
                    #CLEAR ALL POINTS
                    blue_points = []
                    green_points = []
                    red_points = []
                    yellow_points = []
                    black_points = []
                    PaintWindow[60:, :, :] = 255
                    colorIndex= None              #So that user must pick a color before writing instantly after clearing all

                elif Xo[1] < center[0] < Xo[2]: 
                    colorIndex = 0 #Blue
                elif Xo[2] < center[0] < Xo[3]: 
                    colorIndex = 1 #Green
                elif Xo[3] < center[0] < Xo[4]: 
                    colorIndex = 2 #Red
                elif Xo[4] < center[0] < Xo[5]: 
                    colorIndex = 3 #Yellow
                elif Xo[5] < center[0] < (Xo[5]+RectLength) : 
                    colorIndex = 4 #Black     

            else:

                if colorIndex == 0:
                    blue_points.insert(0,center)
                elif colorIndex == 1:
                    green_points.insert(0, center)
                elif colorIndex == 2:
                    red_points.insert(0, center)
                elif colorIndex == 3:
                    yellow_points.insert(0, center)
                elif colorIndex == 4:
                    black_points.insert(0, center)

            for i in range(len(points)):
                for j in range(1, len(points[i])):

                    #cv2.line(frame, points[i][j-1], points[i][j], colors[i],2)
                    cv2.line(PaintWindow, points[i][j - 1], points[i][j], colors[i], 2)


        #STOP HERE

        cv2.imshow('Painter',frame)
        cv2.imshow('PaintWindow',PaintWindow)
        cv2.imshow('Detect',mask)
        
        if( cv2.waitKey(1) == 27):   # 27 ASCII CODE OF Esc
            break
    
    else:
        break
    


cap.release()
cv2.destroyAllWindows()