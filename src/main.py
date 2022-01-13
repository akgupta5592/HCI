import cv2
import handMediapipe as hm

class cvButtons:
    GAP=60

    #  coordinate of the bottom left of the string : for cv2.puttext
    def __init__(self,image,position: tuple, text: str,gap=60) -> None:
        self.position = position
        self.text= text
        cv2.rectangle(image,position,(position[0]+self.GAP,position[1]+self.GAP),(0, 0, 255),cv2.FILLED)
        cv2.putText(image,text,(position[0]+5,position[1]+40 ),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)

allkeys=[['1','2','3','4','5','6','7','8','9','0'],
    ['q','w',"e","r","t","y","u","i",'o','p'],
    ['a','s','d','f','g','h','j','k','l',';',"'"],
    ['z','x','c','v','b','n','m',' ']]


Buttons=[]
string=''

cap = cv2.VideoCapture(0)

hm.to720p(cap)
var = hm.handTrack(1,min_detection_confidence=0.8)
while 1:
    _, frame = cap.read()
    
    frame = cv2.flip(frame, 1)

    for keys in range(len(allkeys)):
        for i,key in enumerate(allkeys[keys]):
            Buttons.append(cvButtons(frame,(100*i+100,80*keys),key))

    backspace = cvButtons(frame,(700,400),'del') 

    landmarks,img = var.Handinfo(frame)

    if landmarks:
        for i in Buttons:
            x,y=i.position

            depth = abs(landmarks['index'][3][-1])

            if x< landmarks['index'][3][1] < x+i.GAP and y<  landmarks['index'][3][2] <y+i.GAP and depth>300:
                
                cv2.rectangle(img,i.position,(i.position[0]+i.GAP,i.position[1]+i.GAP),(255, 255, 0),cv2.FILLED)
                cv2.putText(img,i.text,(i.position[0]+5,i.position[1]+40 ),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
            
                string = string + i.text
        
        
    cv2.imshow('op',img)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()