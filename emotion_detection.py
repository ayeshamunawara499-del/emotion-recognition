from deepface import DeepFace
import cv2

camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()

    if not success:
        break

    # Emotion analyze
    result = DeepFace.analyze(
        frame,
        actions=["emotion"],
        enforce_detection=False
    )

    # Get dominant emotion
    emotion = result[0]["dominant_emotion"]
    confidence = result[0]["emotion"][emotion]

    # Draw emotion text on frame
    print(emotion, confidence)
    cv2.putText(
        frame,
        f"{emotion} ({confidence:.1f}%)",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Draw face rectangle
    region = result[0]["region"]

    x = region["x"]
    y = region["y"]
    w = region["w"]
    h = region["h"]

    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()