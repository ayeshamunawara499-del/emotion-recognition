import cv2
from deepface import DeepFace
import threading
import sqlite3
from datetime import datetime

# ----------------------------------
# CAMERA INITIALIZATION
# ----------------------------------

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not camera.isOpened():
    raise Exception("Camera not found!")

# ----------------------------------
# GLOBAL VARIABLES
# ----------------------------------

emotion = "Waiting..."
confidence = 0.0

face_x = 0
face_y = 0
face_w = 0
face_h = 0

processing = False
frame_counter = 0

# ----------------------------------
# EMOTION DETECTION
# ----------------------------------

def detect_emotion(frame):

    global emotion
    global confidence
    global face_x
    global face_y
    global face_w
    global face_h
    global processing

    try:

        result = DeepFace.analyze(
            img_path=frame,
            actions=["emotion"],
            detector_backend="opencv",
            enforce_detection=False,
            silent=True
        )

        emotion = str(result[0]["dominant_emotion"])

        confidence = float(
            result[0]["emotion"][emotion]
        )

        region = result[0]["region"]

        face_x = int(region["x"])
        face_y = int(region["y"])
        face_w = int(region["w"])
        face_h = int(region["h"])

        # --------------------------
        # SAVE DATABASE
        # --------------------------

        connection = sqlite3.connect("emotion.db")

        cursor = connection.cursor()

        now = datetime.now()

        cursor.execute(

            """
            INSERT INTO history
            (emotion, confidence, date, time)

            VALUES (?, ?, ?, ?)
            """,

            (

                emotion,

                confidence,

                now.strftime("%d-%m-%Y"),

                now.strftime("%H:%M:%S")

            )

        )

        connection.commit()

        connection.close()

        print(
            f"Detected : {emotion} ({confidence:.1f}%)"
        )

    except Exception as e:

        print("DeepFace Error :", e)

    processing = False
    # ----------------------------------
# VIDEO STREAM
# ----------------------------------

def generate_frames():

    global processing
    global frame_counter

    print("Camera Streaming Started")

    while True:

        success, frame = camera.read()

        if not success:
            break

        frame_counter += 1

        # Run DeepFace every 15 frames
        if frame_counter % 15 == 0 and not processing:

            processing = True

            threading.Thread(
                target=detect_emotion,
                args=(frame.copy(),),
                daemon=True
            ).start()

        # Draw face rectangle
        if face_w > 0 and face_h > 0:

            cv2.rectangle(

                frame,

                (face_x, face_y),

                (face_x + face_w,
                 face_y + face_h),

                (0, 255, 0),

                2

            )

            cv2.putText(

                frame,

                f"{emotion} ({confidence:.1f}%)",

                (face_x, face_y - 10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.8,

                (0, 255, 0),

                2

            )

        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        yield (

            b'--frame\r\n'

            b'Content-Type: image/jpeg\r\n\r\n'

            + frame_bytes +

            b'\r\n'

        )


# ----------------------------------
# RELEASE CAMERA
# ----------------------------------

def release_camera():

    global camera

    if camera is not None:

        camera.release()

        cv2.destroyAllWindows()