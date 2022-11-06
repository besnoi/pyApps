
# Python program for face
# comparison
  

from facepplib import FacePP
import numpy as np
import urllib
import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def url_to_image(url):
	resp = urllib.request.urlopen(url)
	img = np.asarray(bytearray(resp.read()), dtype="uint8")
	img = cv2.imdecode(img, cv2.IMREAD_COLOR)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in faces:
		# To draw a rectangle in a face
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,200,0),1)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
	return img


# define global variables
face_detection = ""
faceset_initialize = ""
face_search = ""
face_landmarks = ""
dense_facial_landmarks = ""
face_attributes = ""
beauty_score_and_emotion_recognition = ""
   
# define face comparing function
def face_comparing(app, Image1, Image2):
      
    print()
    print('-'*30)
    print('Comparing Pics...')
    print('-'*30)
  
   
    cmp_ = app.compare.get(image_url1 = Image1,
                           image_url2 = Image2)
   
    print('Pic1', '=', cmp_.image1)
    print('Pic2', '=', cmp_.image2)
   
    # Comparing Photos
    # if cmp_.confidence > 80:
        # print('\nBoth pics are of the same person!!!')
    # else:
    print(f'\nConfidence Number : {cmp_.confidence}')
    print('\nBoth pics are of the same person!!!')
  
          
# Driver Code 
if __name__ == '__main__':
   
    # api details
    api_key ='xQLsTmMyqp1L2MIt7M3l0h-cQiy0Dwhl'
    api_secret ='TyBSGw8NBEP9Tbhv_JbQM18mIlorY6-D'
            
        # call api
    app_ = FacePP(api_key = api_key, 
                    api_secret = api_secret)

        
    # Pair 1
    image1 = 'https://i.imgur.com/Yydp02V.png'
    image2 = 'https://i.imgur.com/FZNtGRS.png'
    # image2 = 'https://i.imgur.com/CnOSZgK.png'

    face_comparing(app_, image1, image2)
    img1 = url_to_image(image1)
    img2 = url_to_image(image2)
    
    while 1:
        cv2.imshow('Image 1',img1)
        cv2.imshow('Image 2',img2)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        
    # # Pair2
    # image1 = 'https://media.geeksforgeeks.org/wp-content/uploads/20200216230843/img45.jpg'
    # image2 = 'https://media.geeksforgeeks.org/wp-content/uploads/20200216230640/img44.jpg'
    # face_comparing(app_, image1, image2)        

