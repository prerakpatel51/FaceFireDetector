import cv2
import face_recognition
import pickle
import os

def encode_faces(extract_dir,encoder_name):

    folderPath=f"{extract_dir}"

    PathList = os.listdir(folderPath)
    imgList = []
    empIds = []

    print(PathList)
    for path in PathList:
        imgList.append(cv2.imread(os.path.join(folderPath, path)))
        empIds.append(os.path.splitext(path)[0])

    print(empIds)

    def findencodings(imagesList):
        encodeList = []
        for img in imagesList:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        
        return encodeList

    print("Encoding started")
    encodeListKnown = findencodings(imgList)
    encodeListKnownWithIds = [encodeListKnown, empIds]
    print("Encoding completed")

    file = open(encoder_name, 'wb')
    pickle.dump(encodeListKnownWithIds, file)
    file.close()

    print("File saved")
