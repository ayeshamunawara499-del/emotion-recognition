import cv2
import mediapipe as mp

camera = cv2.VideoCapture(0)

mp_face = mp.solutions.face_detection
face = mp_face.FaceDetection()

while True:
    success, frame = camera.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = face.process(rgb)

    if result.detections:
        print("Face Detected")

        for detection in result.detections:

            bbox = detection.location_data.relative_bounding_box

            h, w, c = frame.shape

            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            face_w = int(bbox.width * w)
            face_h = int(bbox.height * h)

            print(x, y, face_w, face_h)

            cv2.rectangle(frame, (x, y), (x + face_w, y + face_h), (0, 255, 0), 2)

            
            face_crop = frame[y:y + face_h, x:x + face_w]

            
            if face_crop.size != 0:

                face_resize = cv2.resize(face_crop, (48, 48))

                
                face_gray = cv2.cvtColor(face_resize, cv2.COLOR_BGR2GRAY)

                # Show windows
                cv2.imshow("Face Crop", face_crop)
                cv2.imshow("Face Resize", face_resize)
                cv2.imshow("Gray Face", face_gray)

    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()