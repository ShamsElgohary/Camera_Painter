# Camera_Painter

Program was done using OpenCV and Numpy libraries.  
• User can choose the color which he'd like to detect using the trackbars.  
• User can then choose the color he'd like to draw with by simply moving the detected object to that color.  
• Finally, the user can draw whatever he wants, and can clear the window by simply moving the detected object to the 'Clear All' tab.  

---------------------------------------------------------------------  

Most important steps done in this project:
- Video Capturing
- HSV Object Detection to identify the color of the target which we'll draw
- Mask of the detected object and noise removal
( Erosion and then Dilation)
- Contour (Sort contours and get the largest contour)
- Appending points in a list then displaying them on the Painting Window

![image](https://user-images.githubusercontent.com/68311964/130693165-7379edbf-aa51-4a0e-8f17-2d45aa5c9440.png)

  
  
  
Link showing the program :
https://youtu.be/VZTToh4xaZc
