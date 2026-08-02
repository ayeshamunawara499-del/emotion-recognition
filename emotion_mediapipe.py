import cv2
import mediapipe as mp
from deepface import DeepFace
from collections import Counter
import csv
import os
from datetime import datetime
import time

from emoji_utils import get_emoji, draw_emoji
from progressbar import draw_progress_bar
from suggestion_utils import get_suggestion


# ==========================
# Open Camera
# ==========================

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ==========================
# Variables
# ==========================

emotion_history = []
csv_file = "emotion_log.csv"

if not os.path.exists(csv_file):

    with open(csv_file, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Time",
            "Emotion",
            "Confidence"
        ])


emotion_start_time = time.time()
previous_emotion = ""
emotion_counter = Counter()
last_emotion = ""
emotion_count = 0
display_emotion = ""
last_logged_emotion = ""
last_logged_time = 0
suggestion = ""
emoji = ""
stable_emotion = ""
confidence = 0

# ==========================
# MediaPipe Face Detection
# ==========================

mp_face = mp.solutions.face_detection

face = mp_face.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5
)
 

# ==========================
# Main Loop
# ==========================

while True:

    success, frame = camera.read()

    if not success:
        break
    # ==========================
    # Current Time
    # ==========================
    current_time = datetime.now().strftime("%I:%M:%S %p")
    

    # ==========================
    # Dashboard Panel
    # ==========================

    cv2.rectangle(
        frame,
        (0, 0),
        (280, frame.shape[0]),
        (40, 40, 40),
        -1
    )

    # ==========================
    # Dashboard Title
    # ==========================

    cv2.putText(
        frame,
        "Emotion Dashboard",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )
    # ==========================
    # Live Clock
    # ==========================
    cv2.putText(
        frame,
        "Time",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2
    )
    cv2.putText(
        frame,
        current_time,
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2

    )

    # ==========================
    # Dashboard Heading
    # ==========================

    cv2.putText(
        frame,
        "Current Emotion",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # ==========================
    # Convert BGR → RGB
    # ==========================

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    detections = face.process(rgb)

    if detections.detections:

        for detection in detections.detections:

            bbox = detection.location_data.relative_bounding_box

            h, w, c = frame.shape

            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)

            face_w = int(bbox.width * w)
            face_h = int(bbox.height * h)

            padding = 25

            x = max(0, x - padding)
            y = max(0, y - padding)

            face_w += padding * 2
            face_h += padding * 2

            face_crop = frame[y:y + face_h, x:x + face_w]

            if face_crop.size == 0:
                continue
                        # ==========================
            # Emotion Detection
            # ==========================

            analysis = DeepFace.analyze(
                face_crop,
                actions=["emotion"],
                enforce_detection=False
            )

            emotion = analysis[0]["dominant_emotion"]
            confidence = analysis[0]["emotion"][emotion]
            

            

            # ==========================
            # Emotion Lock System
            # ==========================

            if emotion == last_emotion:
                emotion_count += 1
            else:
                last_emotion = emotion
                emotion_count = 1

            # Emotion should appear only after 3 continuous frames
            if emotion_count >= 3:
                display_emotion = emotion

            # ==========================
            # Emotion History
            # ==========================

            if display_emotion != "":
                emotion_history.append(display_emotion)

            if len(emotion_history) > 50:
                emotion_history.pop(0)

            if len(emotion_history) > 0:
                stable_emotion = Counter(
                     emotion_history
                ).most_common(1)[0][0]
            else:
                stable_emotion = ""
               
            


            emotion_counter[stable_emotion] += 1


            # ==========================
            # Emotion Timer
            # ==========================
            if stable_emotion != previous_emotion:
                previous_emotion = stable_emotion
                emotion_start_time = time.time()
            emotion_seconds = int(time.time() - emotion_start_time)
            cv2.putText(
                frame,
                f"Time : {emotion_seconds} sec",
                (20, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            ) 
            draw_progress_bar(
                frame,
                20,
                205,
                200,
                20,
                confidence
            ) 


            current_time = datetime.now().strftime("%I:%M:%S %p")
            if(
                stable_emotion != last_logged_emotion
                or
                time.time() - last_logged_time >= 5
            ):
                with open(csv_file, "a", newline="") as file:
                     writer = csv.writer(file)
                     writer.writerow([
                         current_time,
                         stable_emotion,
                         round(confidence, 1)
            
                     ])
                last_logged_emotion = stable_emotion
                last_logged_time = time.time()

                




               
            suggestion = get_suggestion(stable_emotion)

            
            emoji = get_emoji(stable_emotion)

            # ==========================
            # Emotion Color
            # ==========================

            if stable_emotion == "happy":
                color = (0, 255, 0)

            elif stable_emotion == "angry":
                color = (0, 0, 255)

            elif stable_emotion == "sad":
                color = (255, 0, 0)

            elif stable_emotion == "surprise":
                color = (0, 255, 255)

            elif stable_emotion == "neutral":
                color = (255, 255, 255)

            elif stable_emotion == "fear":
                color = (255, 0, 255)

            elif stable_emotion == "disgust":
                color = (0, 128, 0)

            else:
                color = (255, 255, 255)


            # ==========================
            # Dashboard Current Emotion
            # ==========================
            # Real Emoji
            draw_emoji(
                frame,
                emoji,
                20,
                130

            )
            cv2.putText(
                frame,
                stable_emotion.upper(),
                (65, 155),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color,
                2

            )

            

            # ==========================
            # Face Rectangle
            # ==========================

            cv2.rectangle(
                frame,
                (x, y),
                (x + face_w, y + face_h),
                color,
                2
            )

            # ==========================
            # Face Emotion Name
            # ==========================

            cv2.putText(
                frame,
                stable_emotion.upper(),
                (x + 10, y - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

            # ==========================
            # Confidence Percentage
            # ==========================

            cv2.putText(
                frame,
                f"{confidence:.1f}%",
                (x + 35, y + face_h + 18),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )
    # ==========================
    # Emotion History
    # ==========================

    cv2.putText(
        frame,
        "Recent Emotions",
        (20, 245),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    history = emotion_history[-5:] if len(emotion_history) > 0 else []

    for i, emo in enumerate(reversed(history)):

        cv2.putText(
            frame,
            emo.upper(),
            (20, 275 + i * 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )
# ==========================
# AI Suggestion
# ==========================
    cv2.putText(
        frame,
        "AI Suggestion",
        (20, 430),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2
    )
    cv2.putText(
        frame,
        suggestion if suggestion else "No Suggestion",
        (20, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )
    # ==========================
    # Emotion Statistics Panel
    # ========================== 
    total = sum(emotion_counter.values())
    if total > 0:
        stats_x = frame.shape[1] - 225
        stats_y = 10
        cv2.putText(
            frame,
            "Statistics",
            (stats_x, stats_y + 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2

        )
        top = [(emo, count) for emo, count in emotion_counter.most_common(3) if emo]
        for i, (emo, count) in enumerate(top):
             percent = (count / total) * 100
             cv2.putText(
                frame,
                f"{emo.capitalize()} : {percent:.1f}%",
                (stats_x + 10, stats_y + 55 + i * 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                 0.5,
                (255, 255, 255),
                 2
        )
        

   

    # ==========================
    # Show Camera
    # ==========================
    cv2.putText(
        frame,
        "Press ESC to Exit",
        (10, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (180, 180, 180),
        1
    )
        
    

    cv2.imshow("Emotion Detection", frame)

    # ==========================
    # Press ESC to Exit
    # ==========================

    if cv2.waitKey(1) == 27:
        break

# ==========================
# Release Camera()
# ==========================

camera.release()
cv2.destroyAllWindows()