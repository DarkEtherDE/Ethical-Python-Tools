import cv2
import os

Home = 'C:\Users\User\Pictures'#source
FACES = 'C:\Users\User\Pictures\Test'#target
TRAIN = 'C:\Users\User\Pictures\Practice'#training

def detect(srcdir=Home, tgtdir=FACES, train_dir=TRAIN):
    for fname in os.listdir(srcdir):
        if not fname.upper().endswith('.JPG'):#check for JPG images
            continue
        fullname = os.path.join(srcdir, fname)
        newname = os.path.join(tgtdir, fname)
        img = cv2.imread(fullname)#Read the image with openCV library
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        training = os.path.join(train_dir, 'haarcascade_frontalface_alt.xml')
        cascade = cv2.CascadeClassifier(training)#use xml file to create a detection object
        rects = cascade.detectMultiScale(gray, 1.3, 5)#see if cascade detects any faces
        try:
            if rects.any():
                print('Got a face')
                rects[:, 2:] += rects[:, :2]
        except AttributeError:
            print(f'No faces found in {fname}.')
            continue
        # highlight the faces in the image
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)#draw a box
            cv2.imwrite(newname, img)#write to output directory
if __name__ == '__main__':
    detect()