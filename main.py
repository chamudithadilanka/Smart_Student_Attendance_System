import cv2
import face_recognition as face_rec

def resize(img, size):
    width = int(img.shape[1]*size)
    height = int(img.shape[0]*size)
    dimansion = (width,height)
    return cv2.resize(img, dimansion, interpolation= cv2.INTER_AREA)

chamu = face_rec.load_image_file('sample_image\chamu.jpg')
chamu = cv2.cvtColor(chamu, cv2.COLOR_BGR2RGB)
chamu = resize(chamu, 0.50)

chamu_test = face_rec.load_image_file('sample_image\elonmask.jpeg')
chamu_test = cv2.cvtColor(chamu_test, cv2.COLOR_BGR2RGB)
chamu_test = resize(chamu_test, 0.50)



face_location_chamu = face_rec.face_locations(chamu)[0]
encode_chamu = face_rec.face_encodings(chamu)[0]
cv2.rectangle(chamu, (face_location_chamu[3], face_location_chamu[0]), (face_location_chamu[1], face_location_chamu[2]), (255,0,255))

face_location_chamutest = face_rec.face_locations(chamu_test)[0]
encode_chamutest = face_rec.face_encodings(chamu_test)[0]
cv2.rectangle(chamu_test, (face_location_chamu[3], face_location_chamu[0]), (face_location_chamu[1], face_location_chamu[2]), (255,0,255))

result = face_rec.compare_faces([encode_chamu], encode_chamutest)
print(result)
cv2.putText(chamu_test, f'{result}', (50,50), cv2.FONT_HERSHEY_COMPLEX, 1 ,(0,0,255), 2 )


cv2.imshow('main_img', chamu)
cv2.imshow('test_img', chamu_test)
cv2.waitKey(0)
cv2.destroyAllWindows()
